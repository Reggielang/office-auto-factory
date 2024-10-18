import base64
import os

import pandas as pd
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QLabel, QGridLayout
from qfluentwidgets import (ImageLabel, SimpleCardWidget, ScrollArea, PushSettingCard, FluentIcon,
                            SettingCardGroup, ComboBox, PrimaryPushButton, PushButton, LineEdit, TextEdit, ProgressBar,
                            HeaderCardWidget)

from assets.comments import description
from src.checks.handlers.process_parmas import process_params
from src.checks.utils.i18_utils import gt
from src.checks.utils.log_utils import log, log_message
from src.checks.utils.messagebox_utils import MessageBoxUtils
from assets.images.excel_png import img as excel_png
from src.checks.utils.pic2_utils import save_base64_image, images_dir

# tmp = open('/images/excel.png', 'wb')  #创建临时的文件
# tmp.write(base64.b64decode(excel_png))  ##把这个one图片解码出来，写入文件中去。
# tmp.close()

file_path_global = None


class DescriptionCard(HeaderCardWidget):
    """ Description card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DescriptionCard")
        self.funcMarkDown = TextEdit(self)
        self.funcMarkDown.setMarkdown(description.funcMarkDown)
        self.funcMarkDown.setFixedHeight(200)
        self.viewLayout.setSpacing(2)
        self.viewLayout.setContentsMargins(0, 0, 5, 5)
        self.viewLayout.addWidget(self.funcMarkDown)


class HandlersCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.table_card = None  # 存储 TableCard 的实例
        self.iconLabel = ImageLabel(save_base64_image(excel_png, images_dir, "excel.png"),self)
        self.iconLabel.setBorderRadius(20, 20, 20, 20)
        self.iconLabel.scaledToWidth(100)
        self.setObjectName("HandlersCard")
        self.messageBox = MessageBoxUtils()
        self.hBoxLayout = QHBoxLayout(self)
        # 加载格式
        self.initLayout()
        self.setBorderRadius(2)

    def initLayout(self):
        # 加载布局
        self.hBoxLayout.setSpacing(8)
        self.hBoxLayout.setContentsMargins(34, 24, 24, 24)
        self.hBoxLayout.addWidget(self.iconLabel)

        # 创建卡片
        basic_group = SettingCardGroup('需要进行校验的文件')
        self.file_path_opt = PushSettingCard(icon=FluentIcon.FOLDER, title='文件路径', text='选择')
        self.file_path_opt.clicked.connect(self._on_file_path_clicked)
        basic_group.addSettingCard(self.file_path_opt)
        self.hBoxLayout.addWidget(basic_group)

    def set_table_card(self, table_card):
        # 设置 TableCard 的实例
        self.table_card = table_card

    def _on_file_path_clicked(self) -> None:
        global file_path_global
        file_path, _ = QFileDialog.getOpenFileName(self, gt('选择你的校验文件'),
                                                   filter="Excel and CSV Files (*.xlsx *.xls *.csv)")
        if file_path is not None and file_path.endswith(('.xlsx', '.xls', '.csv')):
            log.info('选择路径 %s', file_path)
            self._on_file_path_chosen(os.path.normpath(file_path))
            file_path_global = os.path.normpath(file_path)  # 保存文件路径
            try:
                # 调用已存在的 TableCard 实例的 load_data 方法
                if self.table_card is not None:
                    self.table_card.load_data(file_path)
            except Exception as e:
                self.messageBox.createErrorBar(self, "文件读取失败，请检查文件格式或路径是否正确",
                                               f"详细错误信息: {str(e)}")

                # # 设置详细错误信息
                # msg_box = QMessageBox()
                # msg_box.setIcon(QMessageBox.Icon.Warning)
                # msg_box.setWindowTitle("错误")
                # msg_box.setText("文件读取失败，请检查文件格式或路径是否正确")
                # msg_box.setDetailedText(f"详细错误信息: {str(e)}")
                # log.info(f"文件读取失败: {str(e)}")
                # msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                # msg_box.exec()

    def _on_file_path_chosen(self, file_path) -> None:
        # self.ctx.game_config.game_path = file_path
        self.file_path_opt.setContent(file_path)


class TableCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TableCard")
        self.messageBox = MessageBoxUtils()

        self.data = None  # 存储数据
        self.vBoxLayout = QVBoxLayout(self)
        self.gridLayout = QGridLayout(self)

        self.gridLayout.setSpacing(10)
        self.gridLayout.setContentsMargins(34, 24, 24, 24)
        self.setBorderRadius(8)

        # 日志显示文本框
        self.logTextEdit = TextEdit(self)
        self.logTextEdit.setReadOnly(True)
        self.logTextEdit.setFixedHeight(150)  # 可以调整高度
        # 设置日志文本框的背景颜色为浅灰色
        self.logTextEdit.setStyleSheet(
            "background-color: lightgray; color: black; border: 1px solid #ccc; border-radius: 10px;")  # 设置背景颜色和文字颜色
        self.vBoxLayout.addWidget(self.logTextEdit)

        # 进度条
        self.progressBar = ProgressBar(self)
        self.progressBar.setVisible(False)  # 默认隐藏
        self.vBoxLayout.addWidget(self.progressBar)

        # 按钮块
        btn_row_widget = QWidget()
        btn_row_layout = QHBoxLayout(btn_row_widget)
        self.vBoxLayout.addWidget(btn_row_widget, 0, Qt.AlignmentFlag.AlignTop)

        self.start_btn = PrimaryPushButton(text='开始', icon=FluentIcon.PLAY)
        self.start_btn.clicked.connect(self._on_start_clicked)
        btn_row_layout.addWidget(self.start_btn)

        self.stop_btn = PushButton(text='停止', icon=FluentIcon.CLOSE)
        self.stop_btn.clicked.connect(self._on_stop_clicked)
        btn_row_layout.addWidget(self.stop_btn)

        # 卡片标题块
        titleLabel = QLabel("标准校验列表")
        titleLabel.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.gridLayout.addWidget(titleLabel, 0, 0)

        # 标准校验部分
        self.standardContentLayout = QVBoxLayout()
        self.gridLayout.addLayout(self.standardContentLayout, 1, 0)

        # 高阶校验部分
        advancedTitleLabel = QLabel("高阶校验列表")
        advancedTitleLabel.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.gridLayout.addWidget(advancedTitleLabel, 2, 0)

        self.advancedContentLayout = QVBoxLayout()
        self.gridLayout.addLayout(self.advancedContentLayout, 3, 0)

        self.addStandardColButton = PrimaryPushButton(FluentIcon.ADD, '添加标准校验', self)
        self.addStandardColButton.clicked.connect(self.add_standard_row)
        self.gridLayout.addWidget(self.addStandardColButton, 0, 1)

        self.addAdvancedColButton = PrimaryPushButton(FluentIcon.ADD, '添加高阶校验', self)
        self.addAdvancedColButton.clicked.connect(self.add_advanced_row)
        self.gridLayout.addWidget(self.addAdvancedColButton, 2, 1)

        self.vBoxLayout.addLayout(self.gridLayout)

        # 初始化各类容器
        self.standard_column_ComboBoxes = []  # 保存所有标准列选择框
        self.standard_function_ComboBoxes = []  # 保存所有标准函数选择框
        self.standard_empty_checks = []  # 保存所有标准复选框
        self.advanced_column_ComboBoxes = []  # 保存所有高阶列选择框
        self.advanced_function_ComboBoxes = []  # 保存所有高阶函数选择框
        self.advanced_empty_checks = []  # 保存所有高阶复选框
        self.advanced_textEdits = []  # 保存所有高阶文本框
        self.is_running = False  # 用于标记是否正在运行

        self.timer = QTimer(self)  # 用于定时更新进度条
        self.timer.timeout.connect(self.update_progress)

    def log(self, message):
        log_message(message, self.logTextEdit)

    def add_standard_row(self):
        if self.data is None:
            self.log("数据无法加载或出现错误,请重新选择其他文件或检查并修改文件后再次加载")
            log.error("数据无法加载或出现错误,请重新选择其他文件或检查并修改文件后再次加载")
            self.messageBox.createErrorBar(self, "请先添加需要进行校验的文件", "")
            return

        rowLayout = QHBoxLayout()
        columnComboBox = ComboBox()
        if self.data is not None:
            for column in self.data.columns:
                columnComboBox.addItem(column)

        functionComboBox = ComboBox()
        verification_functions = ["空值校验", "身份证校验", "手机校验", "数值校验"]
        for function in verification_functions:
            functionComboBox.addItem(function)

        # emptyCheck = CheckBox("非空校验")
        removeButton = PrimaryPushButton("删除")
        removeButton.setFixedWidth(60)
        removeButton.clicked.connect(lambda: self.remove_standard_row(rowLayout))

        rowLayout.addWidget(columnComboBox, Qt.AlignmentFlag.AlignTop)
        rowLayout.addWidget(functionComboBox, Qt.AlignmentFlag.AlignTop)
        rowLayout.addWidget(removeButton, Qt.AlignmentFlag.AlignTop)

        self.standardContentLayout.addLayout(rowLayout)
        self.standard_column_ComboBoxes.append(columnComboBox)
        self.standard_function_ComboBoxes.append(functionComboBox)

    # 添加高阶校验列
    def add_advanced_row(self):
        if self.data is None:
            self.log("数据无法加载或出现错误,请重新选择其他文件或检查并修改文件后再次加载")
            log.error("数据无法加载或出现错误,请重新选择其他文件或检查并修改文件后再次加载")
            self.messageBox.createErrorBar(self, "请先添加需要进行校验的文件", "")
            return

        rowLayout = QHBoxLayout()
        columnComboBox = ComboBox()

        if self.data is not None:
            for column in self.data.columns:
                columnComboBox.addItem(column)

        functionComboBox = ComboBox()
        verification_functions = ["长度校验", "枚举值校验"]
        for function in verification_functions:
            functionComboBox.addItem(function)

        # emptyCheck = CheckBox("非空校验")
        textEdit = LineEdit()
        textEdit.setPlaceholderText("请输入一个数值")

        removeButton = PrimaryPushButton("删除")
        removeButton.setFixedWidth(60)
        removeButton.clicked.connect(lambda: self.remove_advanced_row(rowLayout))

        # 更新文本框的占位符文本
        def update_placeholder_text():
            selected_function = functionComboBox.currentText()
            if selected_function == "长度校验":
                textEdit.setPlaceholderText("请输入一个数值")
            elif selected_function == "枚举值校验":
                textEdit.setPlaceholderText("a,b,c")

        # 当选择函数变化时更新占位符文本
        functionComboBox.currentTextChanged.connect(update_placeholder_text)

        rowLayout.addWidget(columnComboBox, Qt.AlignmentFlag.AlignTop)
        rowLayout.addWidget(functionComboBox, Qt.AlignmentFlag.AlignTop)
        rowLayout.addWidget(textEdit, Qt.AlignmentFlag.AlignTop)
        rowLayout.addWidget(removeButton, Qt.AlignmentFlag.AlignTop)

        self.advancedContentLayout.addLayout(rowLayout)
        self.advanced_column_ComboBoxes.append(columnComboBox)
        self.advanced_function_ComboBoxes.append(functionComboBox)
        self.advanced_textEdits.append(textEdit)

    def get_row_values(self):
        """ 获取所有行的选择值 """
        standard_values = []
        advanced_values = []

        # 获取标准校验部分的数据
        for i in range(len(self.standard_column_ComboBoxes)):
            column = self.standard_column_ComboBoxes[i].currentText()
            function = self.standard_function_ComboBoxes[i].currentText()
            standard_values.append((column, function))

        # 获取高阶校验部分的数据
        for i in range(len(self.advanced_column_ComboBoxes)):
            column = self.advanced_column_ComboBoxes[i].currentText()
            function = self.advanced_function_ComboBoxes[i].currentText()
            text_input = self.advanced_textEdits[i].text()
            advanced_values.append((column, function, text_input))
        self.log(f"'standard': {standard_values}, 'advanced': {advanced_values}")
        return {'standard': standard_values, 'advanced': advanced_values}

    # 加载数据和清空数据
    def load_data(self, file_path):
        try:
            # 根据文件扩展名选择读取方法
            _, file_extension = os.path.splitext(file_path)
            if file_extension.lower() in ('.xlsx', '.xls'):
                self.data = pd.read_excel(file_path)
            elif file_extension.lower() == '.csv':
                self.data = pd.read_csv(file_path)
            else:
                raise ValueError("不支持该文件格式！")
        except Exception as e:
            self.messageBox.createErrorBar(self, "文件读取失败!", f"详细错误信息: {str(e)}")
            self.clear_data()
        # # 加载新文件后，清空之前的行
        self.clear_data()

    def clear_data(self):
        self.clear_standard_data()
        self.clear_advanced_data()

    def clear_standard_data(self):
        # 清空标准校验部分
        while self.standardContentLayout.count():
            item = self.standardContentLayout.takeAt(0)
            if item.layout():
                while item.layout().count():
                    widget = item.layout().takeAt(0).widget()
                    if widget:
                        widget.deleteLater()
                item.layout().deleteLater()
            else:
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        # 清空标准校验控件列表
        self.standard_column_ComboBoxes.clear()
        self.standard_function_ComboBoxes.clear()

    def clear_advanced_data(self):
        # 清空高阶校验部分
        while self.advancedContentLayout.count():
            item = self.advancedContentLayout.takeAt(0)
            if item.layout():
                while item.layout().count():
                    widget = item.layout().takeAt(0).widget()
                    if widget:
                        widget.deleteLater()
                item.layout().deleteLater()
            else:
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        # 清空高阶校验控件列表
        self.advanced_column_ComboBoxes.clear()
        self.advanced_function_ComboBoxes.clear()
        self.advanced_empty_checks.clear()
        self.advanced_textEdits.clear()

    def remove_standard_row(self, layout):
        index = self.standardContentLayout.indexOf(layout)
        if index >= 0:
            current_layout = self.standardContentLayout.takeAt(index)
            while current_layout.count():
                item = current_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            del current_layout

            if index < len(self.standard_column_ComboBoxes):
                del self.standard_column_ComboBoxes[index]
            if index < len(self.standard_function_ComboBoxes):
                del self.standard_function_ComboBoxes[index]

    def remove_advanced_row(self, layout):
        index = self.advancedContentLayout.indexOf(layout)
        if index >= 0:
            current_layout = self.advancedContentLayout.takeAt(index)
            while current_layout.count():
                item = current_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
            del current_layout

            if index < len(self.advanced_column_ComboBoxes):
                del self.advanced_column_ComboBoxes[index]
            if index < len(self.advanced_function_ComboBoxes):
                del self.advanced_function_ComboBoxes[index]
            if index < len(self.advanced_textEdits):
                del self.advanced_textEdits[index]

    # 鼠标点击触发操作
    def _on_start_clicked(self) -> None:
        self.log("开始校验数据~")
        if self.data is None:
            self.messageBox.createErrorBar(self, "请先添加需要进行校验的文件", "")
            return
        # 在开始前进行数值校验
        try:
            self.validate_advanced_inputs()
        except Exception:
            self.messageBox.createErrorBar(self, "高阶校验的参数不合法", "")
            return

        if len(self.standard_column_ComboBoxes) > 0 or len(self.advanced_column_ComboBoxes) > 0:
            self.is_running = True  # 标记开始运行
            self.progressBar.setVisible(True)  # 显示进度条
            self.progressBar.setValue(0)  # 设置初始值为0

            # 创建一份数据的副本
            data_copy = self.data.copy()
            # 获取所有行的选择值
            values = self.get_row_values()
            # 使用副本进行处理
            process_params(values, data_copy, self.log, file_path_global)
            self.messageBox.createSuccessBar(self, "数据校验已完成 校验文件已保存至工作目录")
        else:
            self.messageBox.createErrorBar(self, "请至少添加一行校验规则")
            return

    def update_progress(self, value):
        if self.is_running:
            self.progressBar.setValue(value)
        else:
            self.timer.stop()
            self.progressBar.setValue(0)
            self.progressBar.setVisible(False)

    def validate_advanced_inputs(self):
        for comboBox, functionComboBox, editText in zip(
                self.advanced_column_ComboBoxes,
                self.advanced_function_ComboBoxes,
                self.advanced_textEdits
        ):
            if functionComboBox.currentText() == "长度校验":
                value = editText.text()
                if not value.isdigit():
                    raise ValueError()
            if functionComboBox.currentText() == "枚举值校验":
                values = editText.text().split(',')
                if not all(value.strip() for value in values):
                    raise ValueError()

    def _on_stop_clicked(self) -> None:
        self.log("已停止校验~")
        self.is_running = False
        self.timer.stop()
        self.update_progress(0)


class HandlersInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        # 初始化卡片
        self.handlersCard = HandlersCard(self)
        self.tableCard = TableCard(self)
        self.descriptionCard = DescriptionCard(self)

        # 设置 handlersCard 中的 table_card
        self.handlersCard.set_table_card(self.tableCard)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("appPage—Excel")

        # 加载卡片
        self.vBoxLayout.setSpacing(5)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 10)
        self.vBoxLayout.addWidget(self.descriptionCard, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.handlersCard, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.tableCard, 1, Qt.AlignmentFlag.AlignTop)

        self.enableTransparentBackground()
