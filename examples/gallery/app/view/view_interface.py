# coding:utf-8
import os

import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QTreeWidgetItem, QHBoxLayout, QTreeWidgetItemIterator, QTableWidgetItem, \
    QListWidgetItem, QMessageBox
from qfluentwidgets import TreeWidget, TableWidget, ListWidget, HorizontalFlipView

from .gallery_interface import GalleryInterface
from ..common.style_sheet import StyleSheet
from ..common.translator import Translator


class ViewInterface(GalleryInterface):
    """ View interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.view,
            subtitle="qfluentwidgets.components.widgets",
            parent=parent
        )
        self.setObjectName('viewInterface')

        # list view
        self.addExampleCard(
            title=self.tr('A simple ListView'),
            widget=ListFrame(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PyQt6/examples/view/list_view/demo.py'
        )

        # table view
        self.addExampleCard(
            title=self.tr('A simple TableView'),
            widget=TableFrame(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PyQt6/examples/view/table_view/demo.py'
        )

        # tree view
        frame = TreeFrame(self)
        self.addExampleCard(
            title=self.tr('A simple TreeView'),
            widget=frame,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PyQt6/examples/view/tree_view/demo.py'
        )

        frame = TreeFrame(self, True)
        self.addExampleCard(
            title=self.tr('A TreeView with Multi-selection enabled'),
            widget=frame,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PyQt6/examples/view/tree_view/demo.py'
        )

        # flip view
        w = HorizontalFlipView(self)
        w.addImages([
            ":/gallery/images/Shoko1.jpg",
            ":/gallery/images/Shoko2.jpg",
            ":/gallery/images/Shoko3.jpg",
            ":/gallery/images/Shoko4.jpg",
        ])
        self.addExampleCard(
            title=self.tr('Flip view'),
            widget=w,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PyQt6/examples/view/flip_view/demo.py'
        )


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)

        self.setObjectName('frame')
        StyleSheet.VIEW_INTERFACE.apply(self)

    def addWidget(self, widget):
        self.hBoxLayout.addWidget(widget)


class ListFrame(Frame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.listWidget = ListWidget(self)
        self.addWidget(self.listWidget)

        stands = [
            self.tr("Star Platinum"), self.tr("Hierophant Green"),
            self.tr("Made in Haven"), self.tr("King Crimson"),
            self.tr("Silver Chariot"), self.tr("Crazy diamond"),
            self.tr("Metallica"), self.tr("Another One Bites The Dust"),
            self.tr("Heaven's Door"), self.tr("Killer Queen"),
            self.tr("The Grateful Dead"), self.tr("Stone Free"),
            self.tr("The World"), self.tr("Sticky Fingers"),
            self.tr("Ozone Baby"), self.tr("Love Love Deluxe"),
            self.tr("Hermit Purple"), self.tr("Gold Experience"),
            self.tr("King Nothing"), self.tr("Paper Moon King"),
            self.tr("Scary Monster"), self.tr("Mandom"),
            self.tr("20th Century Boy"), self.tr("Tusk Act 4"),
            self.tr("Ball Breaker"), self.tr("Sex Pistols"),
            self.tr("D4C • Love Train"), self.tr("Born This Way"),
            self.tr("SOFT & WET"), self.tr("Paisley Park"),
            self.tr("Wonder of U"), self.tr("Walking Heart"),
            self.tr("Cream Starter"), self.tr("November Rain"),
            self.tr("Smooth Operators"), self.tr("The Matte Kudasai")
        ]
        for stand in stands:
            self.listWidget.addItem(QListWidgetItem(stand))

        self.setFixedSize(300, 380)


class TreeFrame(Frame):

    def __init__(self, parent=None, enableCheck=False):
        super().__init__(parent)
        self.tree = TreeWidget(self)
        self.addWidget(self.tree)

        item1 = QTreeWidgetItem([self.tr('JoJo 1 - Phantom Blood')])
        item1.addChildren([
            QTreeWidgetItem([self.tr('Jonathan Joestar')]),
            QTreeWidgetItem([self.tr('Dio Brando')]),
            QTreeWidgetItem([self.tr('Will A. Zeppeli')]),
        ])
        self.tree.addTopLevelItem(item1)

        item2 = QTreeWidgetItem([self.tr('JoJo 3 - Stardust Crusaders')])
        item21 = QTreeWidgetItem([self.tr('Jotaro Kujo')])
        item21.addChildren([
            QTreeWidgetItem(['空条承太郎']),
            QTreeWidgetItem(['空条蕉太狼']),
            QTreeWidgetItem(['阿强']),
            QTreeWidgetItem(['卖鱼强']),
            QTreeWidgetItem(['那个无敌的男人']),
        ])
        item2.addChild(item21)
        self.tree.addTopLevelItem(item2)
        self.tree.expandAll()
        self.tree.setHeaderHidden(True)

        self.setFixedSize(300, 380)

        if enableCheck:
            it = QTreeWidgetItemIterator(self.tree)
            while it.value():
                it.value().setCheckState(0, Qt.CheckState.Unchecked)
                it += 1


class TableFrame(TableWidget):

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
            QMessageBox.warning(self, "错误", f"文件读取失败: {e}")
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
