from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import config
from game import run_game


class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置GUI窗口的位置和尺寸
        self.setGeometry(510, 140, 960, 720)
        self.setWindowTitle(config.WIN_NAME)

        # 载入背景图片
        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap("image/ui/main.png")))
        self.setPalette(window_pale)

        # 应用图标
        self.setWindowIcon(QIcon('image/icon.png'))

        # 创建三个按钮
        self.bt1 = QPushButton('', self)
        self.bt1.setGeometry(QRect(575, 280, 211, 67))
        self.bt2 = QPushButton('', self)
        self.bt2.setGeometry(QRect(575, 400, 211, 67))
        self.bt3 = QPushButton('', self)
        self.bt3.setGeometry(QRect(575, 520, 211, 67))

        # 按钮图像
        self.bt1.setStyleSheet("QPushButton{border-image: url(image/ui/button1.png)}"
                               "QPushButton:hover{border-image: url(image/ui/button1_1.png)}"
                               "QPushButton:pressed{border-image: url(image/ui/button1_2.png)}")
        self.bt2.setStyleSheet("QPushButton{border-image: url(image/ui/button2.png)}"
                               "QPushButton:hover{border-image: url(image/ui/button2_1.png)}"
                               "QPushButton:pressed{border-image: url(image/ui/button2_2.png)}")
        self.bt3.setStyleSheet("QPushButton{border-image: url(image/ui/button3.png)}"
                               "QPushButton:hover{border-image: url(image/ui/button3_1.png)}"
                               "QPushButton:pressed{border-image: url(image/ui/button3_2.png)}")

        # 点击“开始游戏”
        self.bt1.clicked.connect(self.begin)

        # 点击“游戏说明”
        self.bt2.clicked.connect(self.introduction)

        # 点击“关于我们”
        self.bt3.clicked.connect(self.about)

    windowList = []

    def begin(self):
        tag = run_game()
        qwin = queryWindow(tag)
        self.windowList.append(qwin)
        self.close()
        qwin.show()

    def introduction(self):
        child = childWindow('Introduction', 'image/introduction.png')
        self.windowList.append(child)
        self.close()
        child.show()

    def about(self):
        child = childWindow('About', 'image/introduction.png')
        self.windowList.append(child)
        self.close()
        child.show()


class childWindow(QWidget):

    def __init__(self, name, src):
        super().__init__()
        self.initUI(name, src)

    def initUI(self, name, src):
        # 设置GUI窗口的位置和尺寸
        self.setGeometry(710, 140, 534, 720)
        self.center()
        self.setWindowTitle(name)

        # 应用图标
        self.setWindowIcon(QIcon('image/icon.png'))

        # 载入背景图片
        window_pale = QPalette()
        window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap(src)))
        self.setPalette(window_pale)

    windowList = []

    def closeEvent(self, event):
        the_window = mainWindow()
        self.windowList.append(the_window)
        the_window.show()
        event.accept()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)


class queryWindow(QWidget):

    def __init__(self, tag):
        super().__init__()
        self.initUI(tag)

    def initUI(self, tag):
        # 设置GUI窗口的位置和尺寸
        self.resize(421, 360)
        self.center()
        name = 'You Win!' if tag == 0 else 'You Lose.'
        self.setWindowTitle(name)

        # 应用图标
        self.setWindowIcon(QIcon('image/icon.png'))

        # 载入背景图片
        window_pale = QPalette()
        if tag == 0:
            window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap('image/ui/inform_s.jpg')))
        else:
            window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap('image/ui/inform_f.jpg')))
        self.setPalette(window_pale)

        # 按钮
        self.bt1 = QPushButton('', self)
        self.bt1.setGeometry(QRect(50, 240, 136, 63))
        self.bt2 = QPushButton('', self)
        self.bt2.setGeometry(QRect(240, 240, 136, 63))

        self.bt1.setStyleSheet("QPushButton{border-image: url(image/ui/return.png)}"
                               "QPushButton:hover{border-image: url(image/ui/return_1.png)}"
                               "QPushButton:pressed{border-image: url(image/ui/return_2.png)}")
        if tag == 0:
            self.bt2.setStyleSheet("QPushButton{border-image: url(image/ui/continue.png)}"
                                   "QPushButton:hover{border-image: url(image/ui/continue_1.png)}"
                                   "QPushButton:pressed{border-image: url(image/ui/continue_2.png)}")
        else:
            self.bt2.setStyleSheet("QPushButton{border-image: url(image/ui/restart.png)}"
                                   "QPushButton:hover{border-image: url(image/ui/restart_1.png)}"
                                   "QPushButton:pressed{border-image: url(image/ui/restart_2.png)}")

        # 点击“返回”
        self.bt1.clicked.connect(self.tomain)
        # 点击“继续”
        self.bt2.clicked.connect(self.begin)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    windowList = []

    def tomain(self, event):
        the_window = mainWindow()
        self.windowList.append(the_window)
        self.close()
        the_window.show()

    def begin(self):
        tag = run_game()
        the_window = queryWindow(tag)
        self.windowList.append(the_window)
        self.close()
        the_window.show()
