import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (
    QApplication,
    QPushButton,
    QWidget,
)
from PyQt5.QtGui import QIcon


class MainApp(QWidget):
    def __init__(self):
        super().__init__()

        self.app_title = 'App title'
        self.app_icon = 'assets/gui/logo.png'

        self.init_ui()

    def init_ui(self) -> None:
        # window params
        self.setWindowTitle(self.app_title)
        self.setWindowIcon(QIcon(self.app_icon))
        self.setGeometry(900, 350, 551, 500)  # location x,y and size x,y
        # ui elements
        self.ui_quit_btn()
        # show
        self.show()

    def ui_quit_btn(self) -> None:
        btn = QPushButton('Quit', self)
        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)


if __name__ == '__main__':
    qt_app = QApplication(sys.argv)
    ex = MainApp()
    sys.exit(qt_app.exec_())
