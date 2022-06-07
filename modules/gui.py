import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (
    QApplication,
    QAction,
    qApp,
    QDesktopWidget,
    QMainWindow,
    QPushButton,
    QToolTip,
    QWidget,
)
from PyQt5.QtGui import QIcon, QFont


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.app_title = 'App title'
        self.app_icon = 'assets/gui/logo.png'

        self.init_ui()

    def init_ui(self) -> None:
        QToolTip.setFont(QFont('Roboto', 10))
        # window
        self.set_window()
        # ui
        self.ui_quit_btn()
        # toolbar
        self.set_toolbar()
        # status
        self.set_statusbar()
        # show
        self.show()

    def set_window(self, size=[550, 500]) -> None:
        """Set window default title/icon/size/position"""
        self.setWindowTitle(self.app_title)
        self.setWindowIcon(QIcon(self.app_icon))
        # position/size
        self.resize(*size)
        window_rect = self.frameGeometry()  # app window rect
        window_coords = QDesktopWidget().availableGeometry().center()  # screen center x,y
        window_rect.moveCenter(window_coords)
        self.move(window_rect.topLeft())  # move app rect to screen center

    def set_toolbar(self) -> None:
        exitAction = QAction(QIcon('assets/gui/exit.png'), 'Exit', self)
        exitAction.setShortcut('HOME')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('')
        self.toolbar.addAction(exitAction)

    def set_statusbar(self, msg='Ready') -> None:
        self.statusBar().showMessage(msg)

    def ui_quit_btn(self) -> None:
        btn = QPushButton('Quit', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)


if __name__ == '__main__':
    qt_app = QApplication(sys.argv)
    ex = MainApp()
    sys.exit(qt_app.exec_())
