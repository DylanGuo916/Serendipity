# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QVBoxLayout
from qfluentwidgets import AvatarWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import PrimaryPushButton, ProgressBar
from qframelesswindow import AcrylicWindow, StandardTitleBar


class SerendipityView(AcrylicWindow):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet("ButtonView{background: rgb(255,255,255)}")

        Standardtitlebar = StandardTitleBar(self)
        Standardtitlebar.setTitle("情侣头像生成器-天降祁媛(serendipity)")
        self.setTitleBar(Standardtitlebar)

        leftPic = QPixmap('')
        rightPic = QPixmap('')
        self.leftAvatar = AvatarWidget(leftPic, self)
        self.rightAvatar = AvatarWidget(rightPic, self)
        self.leftAvatar.setRadius(128)
        self.rightAvatar.setRadius(128)

        self.progressBar = ProgressBar(self)
        self.progressBar.setValue(0)
        self.progressBar.setFixedHeight(6)

        self.generateButton = PrimaryPushButton('开始生成', self)
        self.saveButton = PrimaryPushButton('保存图片', self)

        self.generateButton.clicked.connect(self.on_generate_button_clicked)
        self.saveButton.clicked.connect(self.on_save_button_clicked)
        self.refCount = 0

        self.label = QLabel('')
        font = self.label.font()
        font.setPointSize(20)  # 设置字体大小为 20
        self.label.setFont(font)
        self.label.setStyleSheet("QLabel { color: red; }")
        self.label.setAlignment(Qt.AlignCenter)

        vBoxLayout = QVBoxLayout()

        hBoxLayout1 = QHBoxLayout()
        hBoxLayout1.addWidget(self.leftAvatar)
        hBoxLayout1.addWidget(self.rightAvatar)

        hBoxLayout2 = QHBoxLayout()
        hBoxLayout2.addWidget(self.progressBar)

        hBoxLayout3 = QHBoxLayout()
        hBoxLayout3.addWidget(self.generateButton)
        hBoxLayout3.addWidget(self.saveButton)

        vBoxLayout.addLayout(hBoxLayout1)
        vBoxLayout.addLayout(hBoxLayout2)
        vBoxLayout.addLayout(hBoxLayout3)
        vBoxLayout.addWidget(self.label)
        vBoxLayout.setContentsMargins(30, 30, 30, 30)

        self.setLayout(vBoxLayout)
        self.resize(600, 700)

    def on_generate_button_clicked(self):
        if self.progressBar.value() != 0:
            return

        if self.refCount == 0:
            self.generateButton.setText("换一组")
        self.refCount += 1

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)  # 设置timer超时时间为 100 ms

        print("generate Button has been clicked ", self.refCount)

    def on_save_button_clicked(self):
        print("Button was clicked!")

    def update_progress(self):
        value = self.progressBar.value()
        value = min(value + 6, 100)
        self.progressBar.setValue(value)
        # 如果进度条已满，停止计时器
        if value == 100:
            self.timer.stop()
            self.progressBar.setValue(0)

            if self.refCount == 1:
                self.label.setText("恭喜您！成功为您生成了一组情侣头像！")
            elif self.refCount == 2:
                self.label.setText("恭喜您！成功为您更换了一组情侣头像！")
            elif self.refCount == 3:
                self.label.setText("恭喜您！成功又为您更换了一组情侣头像！")
            else:
                self.label.setText("恭喜您！成功又又为您更换了一组情侣头像！")

            leftPic = QPixmap('resource/{}_left.jpg'.format(self.refCount % 4))
            rightPic = QPixmap(
                'resource/{}_right.jpg'.format(self.refCount % 4))
            self.leftAvatar.setPixmap(leftPic)
            self.rightAvatar.setPixmap(rightPic)
            self.leftAvatar.setRadius(128)
            self.rightAvatar.setRadius(128)


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    w = SerendipityView()
    w.show()
    app.exec_()
