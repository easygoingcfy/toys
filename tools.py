"""放置PyQt5有关的函数
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


def generate_hbox(widgets: list, strech=1):
    hbox = QHBoxLayout()
    for widget in widgets:
        if hasattr(widget, "setAlignment"):
            widget.setAlignment(Qt.AlignCenter)
        hbox.addWidget(widget, strech)
    return hbox


def box_add_layout(box, layouts: list):
    for layout in layouts:
        if isinstance(layout, QHBoxLayout):
            box.addLayout(layout)
        else:
            box.addWidget(layout)
