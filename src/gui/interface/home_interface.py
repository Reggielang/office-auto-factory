# coding:utf-8
import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import (BodyLabel, CaptionLabel, ImageLabel, SimpleCardWidget,
                            HeaderCardWidget, InfoBarIcon, HyperlinkLabel,
                            PrimaryPushButton, TitleLabel, setFont, ScrollArea,
                            VerticalSeparator, Flyout)

from assets.comments import description


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


if isWin11():
    pass
else:
    pass


class StatisticsWidget(QWidget):
    """ Statistics widget """

    def __init__(self, title: str, value: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = CaptionLabel(title, self)
        self.valueLabel = BodyLabel(value, self)
        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.setContentsMargins(16, 0, 16, 0)
        self.vBoxLayout.addWidget(self.valueLabel, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignmentFlag.AlignBottom)

        setFont(self.valueLabel, 18, QFont.Weight.DemiBold)
        self.titleLabel.setTextColor(QColor(96, 96, 96), QColor(206, 206, 206))


class AppInfoCard(SimpleCardWidget):
    """ App information card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.iconLabel = ImageLabel("../../assets/images/main.png", self)
        self.iconLabel.setBorderRadius(20, 20, 20, 20)
        self.iconLabel.scaledToWidth(120)
        self.setObjectName("AppInfoCard")

        self.nameLabel = TitleLabel(description.TitleLabel, self)
        self.installButton = PrimaryPushButton('欢迎使用', self)
        self.companyLabel = HyperlinkLabel(QUrl('https://github.com/Reggielang'), 'Design By @HONGLANG LUO', self)
        self.installButton.setFixedWidth(100)

        self.scoreWidget = StatisticsWidget('平均', '5.0', self)
        self.separator = VerticalSeparator(self)
        self.commentWidget = StatisticsWidget('评论数', '999K', self)

        self.descriptionLabel = BodyLabel(description.AppInfoComment, self)
        self.descriptionLabel.setWordWrap(True)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.statisticsLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()

        # 加载格式
        self.initLayout()
        self.setBorderRadius(8)

    def initLayout(self):
        self.hBoxLayout.setSpacing(30)
        self.hBoxLayout.setContentsMargins(34, 24, 24, 24)
        self.hBoxLayout.addWidget(self.iconLabel)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)

        # 名字和描述
        self.vBoxLayout.addLayout(self.topLayout)
        self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.addWidget(self.nameLabel)

        self.vBoxLayout.addSpacing(20)
        self.vBoxLayout.addWidget(self.descriptionLabel)
        self.descriptionLabel.setFixedWidth(580)
        self.descriptionLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # company label
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addWidget(self.companyLabel)

        # statistics widgets
        self.vBoxLayout.addSpacing(5)
        self.vBoxLayout.addLayout(self.statisticsLayout)
        self.statisticsLayout.setContentsMargins(0, 0, 0, 0)
        self.statisticsLayout.setSpacing(50)
        self.statisticsLayout.addWidget(self.scoreWidget)
        self.statisticsLayout.addWidget(self.separator)
        self.statisticsLayout.addWidget(self.commentWidget)
        self.statisticsLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # button
        self.vBoxLayout.addSpacing(12)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.buttonLayout.addWidget(self.installButton, 0, Qt.AlignmentFlag.AlignBottom)


class FunctionCard(HeaderCardWidget):
    """ Function card """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("FunctionCard")
        self.setTitle("程序特点")

        self.settingFlyoutButton = PrimaryPushButton(self.tr("实用小工具"))
        self.settingFlyoutButton.clicked.connect(self.showSettingFlyout)
        self.settingFlyoutButton.setFixedWidth(120)
        self.viewLayout.addWidget(self.settingFlyoutButton, 0, Qt.AlignmentFlag.AlignTop)

        self.reportFlyoutButton = PrimaryPushButton(self.tr("快速响应"))
        self.reportFlyoutButton.clicked.connect(self.showReportFlyout)
        self.reportFlyoutButton.setFixedWidth(120)
        self.viewLayout.addWidget(self.reportFlyoutButton, 0, Qt.AlignmentFlag.AlignTop)

        self.styleFlyoutButton = PrimaryPushButton(self.tr("天马行空"))
        self.styleFlyoutButton.clicked.connect(self.showStyleFlyout)
        self.styleFlyoutButton.setFixedWidth(120)
        self.viewLayout.addWidget(self.styleFlyoutButton, 0, Qt.AlignmentFlag.AlignTop)

    def showSettingFlyout(self):
        Flyout.create(
            icon=InfoBarIcon.INFORMATION,
            title='***',
            content=self.tr("用户可以左侧导航栏选择需要实用的工具，并指定相应的校验参数!"),
            target=self.settingFlyoutButton,
            parent=self.window()
        )

    def showReportFlyout(self):
        Flyout.create(
            icon=InfoBarIcon.INFORMATION,
            title='***',
            content=self.tr("进行简单配置后，程序将立即执行，并得到相应结果 !"),
            target=self.reportFlyoutButton,
            parent=self.window()
        )

    def showStyleFlyout(self):
        Flyout.create(
            icon=InfoBarIcon.INFORMATION,
            title='***',
            content=self.tr("各种工具只有想不到,没有用不到!"),
            target=self.styleFlyoutButton,
            parent=self.window()
        )


class HomeInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        # 初始化卡片
        self.appCard = AppInfoCard(self)
        self.functionCard = FunctionCard(self)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("HomeMainInfo")

        # 加载卡片
        self.vBoxLayout.setSpacing(2)
        self.vBoxLayout.setContentsMargins(8, 0, 10, 10)
        self.vBoxLayout.addWidget(self.appCard, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.functionCard, 0, Qt.AlignmentFlag.AlignTop)
        # 设置样式表

        self.enableTransparentBackground()
