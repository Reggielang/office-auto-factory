from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout
from qfluentwidgets import HyperlinkCard, FluentIcon, ImageLabel, SimpleCardWidget

from assets.images.likes_png import img as likes_png
from src.checks.utils.pic2_utils import save_base64_image, images_dir

# tmp = open('/images/excel.png', 'wb')  #创建临时的文件
# tmp.write(base64.b64decode(excel_png))  ##把这个one图片解码出来，写入文件中去。
# tmp.close()

class LikeInterface(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("LikeInterface")
        self.setBorderRadius(8)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(2)  # 减少间距，可以根据实际需要调整这个值
        self.vBoxLayout.setContentsMargins(20, 10, 5, 5)
        self.content1 = HyperlinkCard(icon=FluentIcon.GITHUB, title='Star', text='前往',
                                      content='Github主页右上角点一个星星是最简单直接的',
                                      url='https://github.com/Reggielang/office-auto-factory')

        self.content2 = HyperlinkCard(icon=FluentIcon.DOCUMENT, title='Star', text='前往',
                                      content='访问Github可以查看帮助文档',
                                      url='https://github.com/Reggielang/office-auto-factory/blob/main/README.md')

        self.content3 = HyperlinkCard(icon=FluentIcon.HEART, title='赞赏', text='前往',
                                      content='如果喜欢本项目，你也可以为作者赞助一点维护费用~',
                                      url='')

        self.vBoxLayout.addWidget(self.content1, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.content2, 0, Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.addWidget(self.content3, 0, Qt.AlignmentFlag.AlignTop)

        self.likeLabel = ImageLabel(save_base64_image(likes_png, images_dir, "likes.png"))
        self.likeLabel.setBorderRadius(8, 8, 8, 8)
        self.likeLabel.scaledToWidth(360)

        self.vBoxLayout.addWidget(self.likeLabel)

        # 设置窗口的大小
        self.setFixedSize(1000, 550)  # 设置固定大小以适应所有控件
