from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import (
    QComboBox,
    QGroupBox,
    QLabel,
    QPushButton,
    QHBoxLayout,
)


def on_btn_toggle(btn: object) -> None:
    btn_text = 'OFF' if btn.text() == 'ON' else 'ON'
    btn.setText(btn_text)


def on_combo_box_choice(state: bool):
    print(state)


def ui_quit_btn(instance: object) -> None:
    btn = QPushButton('Quit', instance)
    btn.setToolTip('This is a <b>QPushButton</b> widget')
    btn.move(50, 50)
    btn.resize(btn.sizeHint())
    btn.clicked.connect(QCoreApplication.instance().quit)


def ui_groupbox(title: str, qrect: object, flat=False) -> object:
    groupbox = QGroupBox(title.upper())
    groupbox.setGeometry(qrect)
    if flat:
        groupbox.setFlat(True)
    return groupbox


def ui_hbox_label_combobox_btn(instance: object, label: str, combo_options: list) -> object:
    label = QLabel('/hideout <name>', instance)

    combo_box = QComboBox(instance)
    for i in combo_options:
        combo_box.addItem(i)
    combo_box.activated[str].connect(on_combo_box_choice)

    btn = QPushButton('ON', instance)
    btn.setCheckable(True)
    btn.toggle()
    btn.toggled.connect(lambda: on_btn_toggle(btn))

    hbox = QHBoxLayout()
    hbox.addWidget(label)
    hbox.addStretch(3)
    hbox.addWidget(combo_box)
    hbox.addWidget(btn)
    return hbox
