import datetime
import sys

from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QPushButton, QTextEdit, QVBoxLayout,
                             QWidget)
from utils.time_util import ts_range_by_date


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
        date = self.date_str_line.text()
        ts, te = ts_range_by_date(date)
        self.ts_line.setText(str(ts))
        self.te_line.setText(str(te))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    time_tf = TimeTransform()
    sys.exit(app.exec_())
