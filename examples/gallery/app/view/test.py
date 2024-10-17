import os
import sys

import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, \
    QVBoxLayout, QHBoxLayout, QWidget
from qfluentwidgets import (ImageLabel, SimpleCardWidget, ScrollArea, PushSettingCard, FluentIcon, SettingCardGroup,
                            TableWidget)

from src.checks.utils.i18_utils import gt
from src.checks.utils.log_utils import log


class HandlersCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.iconLabel = ImageLabel(":/qfluentwidgets/images/logo.png", self)
        self.iconLabel.setBorderRadius(20, 20, 20, 20)
        self.iconLabel.scaledToWidth(120)
        self.setObjectName("HandlersCard")

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        # 加载格式
        self.initLayout()
        self.setBorderRadius(8)

    def initLayout(self):
        # 加载布局
        self.hBoxLayout.setSpacing(30)
        self.hBoxLayout.setContentsMargins(34, 24, 24, 24)
        self.hBoxLayout.addWidget(self.iconLabel)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)

        # 创建卡片
        basic_group = SettingCardGroup('校验文件')
        self.file_path_opt = PushSettingCard(icon=FluentIcon.FOLDER, title='文件路径', text='选择')
        self.file_path_opt.clicked.connect(self._on_file_path_clicked)
        basic_group.addSettingCard(self.file_path_opt)
        self.vBoxLayout.addWidget(basic_group)

    def _on_file_path_clicked(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, gt('选择你的校验文件'),
                                                   filter="Excel and CSV Files (*.xlsx *.xls *.csv)")
        if file_path is not None and file_path.endswith(('.xlsx', '.xls', '.csv')):
            log.info('选择路径 %s', file_path)
            self._on_file_path_chosen(os.path.normpath(file_path))
            try:
                # 获取 TableCard 实例并调用 load_data 方法
                table_card_instance = TableCard()
                if table_card_instance is not None:
                    table_card_instance.load_data(file_path)
            except Exception as e:
                # 设置详细错误信息
                msg_box = QMessageBox()
                msg_box.setIcon(QMessageBox.Icon.Warning)
                msg_box.setWindowTitle("错误")
                msg_box.setText("文件读取失败，请检查文件格式或路径是否正确")
                msg_box.setDetailedText(f"详细错误信息: {str(e)}")
                log.info(f"文件读取失败: {str(e)}")
                msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                msg_box.exec()

    def _on_file_path_chosen(self, file_path) -> None:
        # self.ctx.game_config.game_path = file_path
        self.file_path_opt.setContent(file_path)


class TableCard(TableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)
        self.data = None  # 存储数据

        # 初始化空表格
        self.setColumnCount(0)
        self.setHorizontalHeaderLabels([])
        self.setFixedSize(625, 440)
        self.resizeColumnsToContents()

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
            self.display_data()
        except Exception as e:
            # 设置详细错误信息
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("错误")
            msg_box.setText("文件读取失败，请检查文件格式或路径是否正确")
            msg_box.setDetailedText(f"详细错误信息: {str(e)}")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec()
            self.clear_data()

    def display_data(self):
        if self.data is not None:
            # 动态调整列数
            self.setColumnCount(len(self.data.columns))
            self.setHorizontalHeaderLabels(self.data.columns)

            # 展示前五行的数据
            self.setRowCount(min(5, len(self.data)))
            for i, row in self.data.head(5).iterrows():
                for j, value in enumerate(row):
                    self.setItem(i, j, QTableWidgetItem(str(value)))

    def clear_data(self):
        # 清空表格内容
        self.setColumnCount(0)
        self.setHorizontalHeaderLabels([])
        self.setRowCount(0)


class HandlersInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        # 初始化卡片
        self.handlersCard = HandlersCard(self)
        self.tableCard = TableCard(self)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("appPage")

        # 加载卡片
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(0, 0, 10, 30)
        self.vBoxLayout.addWidget(self.handlersCard, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.tableCard, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.enableTransparentBackground()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.resize(800, 600)
        self.interface = HandlersInterface(self)
        self.setCentralWidget(self.interface)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
