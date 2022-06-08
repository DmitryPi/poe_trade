from PyQt5.QtCore import Qt, QCoreApplication, QRect
from PyQt5.QtWidgets import (
    QComboBox,
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
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


def ui_groupbox(title: str, rect: list, flat=False) -> object:
    """Build group box with title and rectangle points"""
    groupbox = QGroupBox(title.upper())
    groupbox.setGeometry(QRect(*rect))
    if flat:
        groupbox.setFlat(True)
    return groupbox


def ui_hbox() -> object:
    hbox = QHBoxLayout()
    return hbox


def ui_vbox(align='top') -> object:
    """Build vertical box with alignment"""
    alignments = {
        'top': Qt.AlignTop,
        'center': Qt.AlignCenter,
        'bottom': Qt.AlignBottom,
    }
    vbox = QVBoxLayout()
    vbox.setAlignment(alignments[align])
    return vbox


def ui_hbox_label_combobox_btn(instance: object, label: str, combo_options: list) -> object:
    """Build horizontal box row with: label, combobox, toggle btn"""
    # label
    label = QLabel(label, instance)
    # combobox
    combo_box = QComboBox(instance)
    for i in combo_options:
        combo_box.addItem(i)
    combo_box.activated[str].connect(on_combo_box_choice)
    # btn
    btn = QPushButton('ON', instance)
    btn.setCheckable(True)
    btn.toggle()
    btn.toggled.connect(lambda: on_btn_toggle(btn))
    # horizonal box
    hbox = ui_hbox()
    hbox.addWidget(label)
    hbox.addWidget(combo_box)
    hbox.addWidget(btn)
    return hbox


def ui_vbox_label_input(instance: object, label: str, input_default='') -> object:
    """Build vertical box with: label, input field(line-edit)"""
    # label
    label = QLabel(label, instance)
    # input field
    line_edit = QLineEdit(instance)
    line_edit.setText(str(input_default))
    # line_edit.textChanged[str].connect(self.onChanged)
    # horizonal box
    vbox = ui_vbox()
    vbox.addWidget(label)
    vbox.addWidget(line_edit)
    return vbox
