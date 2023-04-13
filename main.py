import datetime
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QTextEdit, QWidget, QLabel


class TimeTransform(QWidget):
    """实现日期字符串与时间戳之间的转换
    """

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.date_str_line = QLineEdit(self)
        self.ts_line = QLineEdit(self)
        self.te_line = QLineEdit(self)
        transform_button = QPushButton("transform")
        transform_button.clicked.connect(self.transform)

        hbox = QHBoxLayout()
        hbox.addWidget(self.date_str_line)
        hbox.addWidget(self.ts_line)
        hbox.addWidget(self.te_line)
        hbox.addWidget(transform_button)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        #vbox.addStretch(1)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('toys')
        self.show()
    
    def transform(self):
        value = self.date_str_line.text()
        self.ts_line.setText(value)
        self.te_line.setText(value)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    time_tf = TimeTransform()
    sys.exit(app.exec_())
