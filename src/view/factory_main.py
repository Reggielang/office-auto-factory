# coding:utf-8
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout, QMessageBox
from qfluentwidgets import FluentIcon as FIF, NavigationItemPosition
from qfluentwidgets import (MSFluentWindow,
                            SubtitleLabel, setFont)

from assets.images.logo_png import img as logo_png
from src.checks.utils.log_utils import log
from src.checks.utils.pic2_utils import save_base64_image, images_dir
from src.gui.interface.handlers_interface import HandlersInterface
from src.gui.interface.home_interface import HomeInterface
from src.gui.interface.likes_interface import LikeInterface


class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class Window(MSFluentWindow):
    def __init__(self):
        super().__init__()

        # create sub interface
        # 使用 AppInterface 替代 Widget
        self.homeInterface = HomeInterface()
        self.handlersInterface = HandlersInterface()
        self.handlersInterface2 = LikeInterface()

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.homeInterface, FIF.HOME, '主页', FIF.HOME_FILL)
        self.addSubInterface(self.handlersInterface, FIF.APPLICATION, '应用')
        # self.addSubInterface(self.handlersInterface2, FIF.APPLICATION, '应用2')

        # self.navigationInterface.addItem(
        #     self.handlersInterface2, FluentIcon.SETTING, "设置", position=NavigationItemPosition.BOTTOM)
        #
        self.addSubInterface(self.handlersInterface2, FIF.HEART, '点赞', position=NavigationItemPosition.BOTTOM)
        # self.navigationInterface.addItem(
        #     routeKey='Help',
        #     icon=FIF.HELP,
        #     text='点赞',
        #     # onClick=self.showMessageBox,
        #     selectable=False,
        #     position=NavigationItemPosition.BOTTOM,
        # )
        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())

    def initWindow(self):
        self.resize(1000, 800)  # 调整窗口大小
        self.setWindowIcon(QIcon(save_base64_image(logo_png, images_dir, "logo.png")))
        self.setWindowTitle('办公自动化工厂')

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)



# 定义一个全局异常捕获器
def excepthook(exc_type, exc_value, exc_traceback):
    # 记录异常信息
    log.error("系统发生严重错误，请联系开发者", exc_info=(exc_type, exc_value, exc_traceback))

    # 显示错误对话框
    error_msg = f"一个无法处理的错误发生(请联系开发者):\n{exc_type.__name__}: {exc_value}"
    QMessageBox.critical(None, "严重错误", error_msg)


# 替换默认的异常处理器
sys.excepthook = excepthook

if __name__ == '__main__':
    # setTheme(Theme.DARK)
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())
