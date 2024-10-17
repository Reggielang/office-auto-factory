from PyQt6.QtCore import Qt
from qfluentwidgets import InfoBarPosition, InfoBar


class MessageBoxUtils:
    @staticmethod
    def createErrorBar(parent, content, err_detail=""):
        InfoBar.error(
            title='警告',
            content=content + err_detail,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_LEFT,
            duration=2000,
            parent=parent
        )

    @staticmethod
    def createSuccessBar(parent, content):
        InfoBar.success(
            title='信息',
            content=content,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_LEFT,
            duration=2000,
            parent=parent
        )
