"""继承PyQt5某些Widgets类, 提供支持特定格式的widget
"""
#from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
#                             QMainWindow, QPushButton, QTextEdit, QVBoxLayout,
#                             QWidget, QMessageBox)
import PyQt5.QtWidgets
from enum import Enum


class TsUnit(Enum):
    SECOND = "s"
    MILLISECOND = "ms"


class QLineEdit(PyQt5.QtWidgets.QLineEdit):

    def __init__(self, parent=None):
        super().__init__()

    def setText(self, text):
        if not isinstance(text, str):
            text = str(text)
        super().setText(text)


class QLineEditFloat(QLineEdit):
    """用于显示Float的QLineEdit"""

    def __init__(self, parent=None):
        super().__init__()

    def text(self):
        value = float(super().text())
        return value


class QLineEditTs(QLineEditFloat):
    """用于显示时间戳的QLineEdit

    约定所有的时间戳计算单位采用s
    参数:
    unit: 单位， "s" or "ms"
    """

    def __init__(self, parent=None, unit=TsUnit.SECOND):
        super().__init__()
        self.unit = unit

    def text(self):
        value = super().text()
        if self.unit == TsUnit.MILLISECOND:
            value = value / 1000
        return value

    def setText(self, value):
        if not isinstance(value, float):
            value = float(value)
        if self.unit == TsUnit.MILLISECOND:
            value = value * 1000
        super().setText(value)

    def setUnit(self, unit):
        value = self.text()
        self.unit = unit
        self.setText(value)
