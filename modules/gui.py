import sys
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (
    QApplication,
    QAction,
    qApp,
    QDesktopWidget,
    QLabel,
    QMainWindow,
    QPushButton,
    QToolTip,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QIcon, QFont


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app_title = 'App title'
        self.app_icon = 'assets/gui/logo.png'
        self.app_window_size = [550, 500]
        self.init_ui()

    def init_ui(self) -> None:
        # window
        self.set_window(size=self.app_window_size)
        # ui
        self.ui_quit_btn()
        # toolbar
        self.set_toolbar()
        # status
        self.set_statusbar()
        # styles
        self.set_main_styles()
        # show
        self.show()

    def set_main_styles(self) -> None:
        """Set styles for main frame/bars"""
        # self.setStyleSheet('background-color: #121212; color: white;')
        self.statusBar().setStyleSheet("""
            background-color: #181818;
            color: white;
        """)

    def set_window(self, size=[550, 500]) -> None:
        """Set window default title/icon/size/position"""
        self.setWindowTitle(self.app_title)
        self.setWindowIcon(QIcon(self.app_icon))
        self.set_window_size(size=size)
        self.set_window_center()

    def set_window_size(self, size=[550, 500]) -> None:
        self.resize(*size)
        self.setFixedSize(self.size())

    def set_window_center(self) -> None:
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
