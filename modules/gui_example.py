import sys

from abc import ABC
from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread

from main import KeyPresser


class PyQTUtility(ABC):
    def add_tab(self, id=''):
        tab = QtWidgets.QWidget()
        tab.setObjectName(id)
        self.tabWidget.addTab(tab, '')
        return tab

    def add_label(self, obj, id='', geo=True):
        label = QtWidgets.QLabel(obj)
        if geo:
            label.setGeometry(QtCore.QRect(210, 90, 47, 13))
        label.setObjectName(id)
        return label

    def cb_state(self, cb):
        cb_id = cb.sender().objectName()
        if cb.isChecked():
            print('Checked')
        else:
            print('UnChecked')


class Ui_MainWindow(PyQTUtility):
    def __init__(self):
        self.window_name = 'POEsugar'
        self.statusbar_msg = 'Ready'

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(548, 542)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.InitTabs(self.centralwidget, id='tabWidget')
        self.tab_keypresser = self.add_tab(id='tab_keypresser')
        self.tab_autoflask = self.add_tab(id='tab_autoflask')
        self.tab_trader = self.add_tab(id='tab_trader')

        self.tab_keypresser_ui()
        self.tab_autoflask_ui()
        self.tab_trader_ui()

        self.main_ui()

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def InitTabs(self, obj, id=''):
        self.tabWidget = QtWidgets.QTabWidget(obj)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 531, 331))
        self.tabWidget.setObjectName(id)

    def main_ui(self):
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 510, 551, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.showMessage(self.statusbar_msg)
        MainWindow.setStatusBar(self.statusbar)

    def tab_keypresser_ui(self):
        self.groupBox = QtWidgets.QGroupBox(self.tab_keypresser)
        self.groupBox.setGeometry(QtCore.QRect(270, 10, 251, 291))
        self.groupBox.setObjectName("groupBox")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_keypresser)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 10, 261, 291))
        self.groupBox_2.setObjectName("groupBox_2")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupBox_2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 241, 22))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.stateChanged.connect(lambda:self.cb_state(self.checkBox))
        self.horizontalLayout.addWidget(self.checkBox)

        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setMouseTracking(False)
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setReadOnly(True)
        self.lineEdit.textChanged.connect(lambda:self.input_state(self.lineEdit))
        self.horizontalLayout.addWidget(self.lineEdit, 0, QtCore.Qt.AlignRight)

        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(9, 50, 241, 21))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox_2 = QtWidgets.QCheckBox(self.horizontalLayoutWidget_2)
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_2.addWidget(self.checkBox_2)
        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget_2)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout_2.addWidget(self.comboBox)

    def input_state(self, input):
        print(input)

    def tab_autoflask_ui(self):
        self.label_2 = self.add_label(self.tab_autoflask, "label_2")

    def tab_trader_ui(self):
        self.label = self.add_label(self.tab_trader, id='label')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(self.window_name)

        self.groupBox.setTitle(_translate("MainWindow", "Settings"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Commands"))
        self.checkBox.setText(_translate("MainWindow", "Hideout <name>"))
        self.lineEdit.setText(_translate("MainWindow", "F5"))

        self.checkBox_2.setText(_translate("MainWindow", "CheckBox"))
        self.comboBox.setItemText(0, _translate("MainWindow", "test1"))
        self.comboBox.setItemText(1, _translate("MainWindow", "test2"))
        self.comboBox.setItemText(2, _translate("MainWindow", "New Item"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_keypresser), _translate("MainWindow", "KeyPresser"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_autoflask), _translate("MainWindow", "AutoFlask"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_trader), _translate("MainWindow", "Trader"))


if __name__ == "__main__":
    key_presser = KeyPresser()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    # t_key_presser = Thread(target=key_presser.run)
    # t_key_presser.daemon = True
    # t_key_presser.start()

    sys.exit(app.exec_())
