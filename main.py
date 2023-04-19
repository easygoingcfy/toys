import datetime
import sys

from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QPushButton, QTextEdit, QVBoxLayout,
                             QWidget)
from utils.time_util import ts_range_by_date, timestamp2str
from tools import generate_hbox, box_add_layout


class TimeTransform(QWidget):
    """实现日期字符串与时间戳之间的转换
    """

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """时间变换行"""
        #显示栏
        self.date_str_line = QLineEdit(self)
        self.ts_line = QLineEdit(self)
        self.te_line = QLineEdit(self)
        #按钮
        date_button = QPushButton("日期")
        ts_button = QPushButton("开始时间戳")
        te_button = QPushButton("结束时间戳")
        date_button.clicked.connect(self.date2ts)
        ts_button.clicked.connect(lambda: self.ts2date(self.ts_line.text()))
        te_button.clicked.connect(lambda: self.ts2date(self.te_line.text()))

        hbox_edit_line = generate_hbox(
            [self.date_str_line, self.ts_line, self.te_line])
        hbox_buttion_line = generate_hbox([date_button, ts_button, te_button])

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        box_add_layout(vbox, [hbox_buttion_line, hbox_edit_line])
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('toys')
        self.show()

    def date2ts(self):
        date = self.date_str_line.text()
        ts, te = ts_range_by_date(date)
        self.ts_line.setText(str(ts))
        self.te_line.setText(str(te))

    def ts2date(self, timestamp):
        if isinstance(timestamp, str):
            timestamp = float(timestamp)
        date = timestamp2str(timestamp)
        self.date_str_line.setText(date)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    time_tf = TimeTransform()
    sys.exit(app.exec_())
