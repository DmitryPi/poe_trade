import logging
import sys

from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QTabWidget,
    QPushButton)


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.window_w = 540
        self.window_h = 480
        self.title = 'POEReality'
        self.status_msg = 'Ready'
        # main ui
        self.initUI()
        # init tabs
        self.tab_widget = TabWidget(self)
        self.setCentralWidget(self.tab_widget)

    def initUI(self):
        self.setFixedSize(self.window_w, self.window_h)
        self.setWindowTitle(self.title)
        self.status_bar = self.statusBar()
        self.status_bar.showMessage(self.status_msg)


class TabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("PyQt5 button")
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(name)-24s: %(levelname)-8s %(message)s')
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    start = datetime.now()

    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

    finish = datetime.now() - start
    logging.info(f'Done in: {finish}')
