import sys
from PyQt5.QtCore import QCoreApplication, QRect
from PyQt5.QtWidgets import (
    QApplication,
    QAction,
    qApp,
    QDesktopWidget,
    QComboBox,
    QGroupBox,
    QGridLayout,
    QLabel,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QToolTip,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QLineEdit,
    QTextEdit,
)
from PyQt5.QtGui import QIcon, QFont


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app_title = 'App title'
        self.app_icon = 'assets/gui/logo.png'
        self.app_window_size = [550, 500]
        self.bind_options = [f'F{i}' for i in range(1, 13)]
        self.init_ui()

    def init_ui(self) -> None:
        # window
        self.set_window(size=self.app_window_size)
        # toolbar
        self.set_toolbar()
        # status
        self.set_statusbar()
        # styles
        self.set_main_styles()
        # layout
        self.set_layout()
        # show
        self.show()

    def set_layout(self) -> None:
        # set central widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        # set layout
        hbox = self.layout_hbox_row()
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addStretch(3)

        # render widget
        groupbox_1 = QGroupBox('Macros')
        groupbox_1.setGeometry(QRect(270, 10, 251, 291))
        groupbox_1.setLayout(vbox)
        groupbox_1.setFlat(True)
        groupbox_2 = QGroupBox('Options')
        groupbox_2.setGeometry(QRect(0, 10, 261, 291))
        grid = QGridLayout()
        grid.addWidget(groupbox_1, 0, 0)
        grid.addWidget(groupbox_2, 0, 1)
        main_widget.setLayout(grid)

    def layout_hbox_row(self) -> object:
        label = QLabel('/hideout <name>', self)

        combo_box = QComboBox(self)
        for i in self.bind_options:
            combo_box.addItem(i)
        combo_box.activated[str].connect(self.on_dropdown_choice)

        btn = QPushButton('ON', self)
        btn.setCheckable(True)
        btn.toggle()
        btn.toggled.connect(lambda: self.on_btn_toggle(btn))

        hbox = QHBoxLayout()
        hbox.addWidget(label)
        hbox.addStretch(3)
        hbox.addWidget(combo_box)
        hbox.addWidget(btn)
        return hbox

    def on_btn_toggle(self, btn: object) -> None:
        btn_text = 'OFF' if btn.text() == 'ON' else 'ON'
        btn.setText(btn_text)

    def on_dropdown_choice(self, state):
        print(state)

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
