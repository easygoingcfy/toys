from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QPushButton, QTextEdit, QVBoxLayout,
                             QWidget, QMessageBox)


class QLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__()
    
    def setText(self, text):
        if not isinstance(text, str):
            text = str(text)
        super().setText(text)