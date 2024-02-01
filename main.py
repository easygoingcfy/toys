import datetime
import re
import sys
import traceback
from enum import Enum

from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow, QComboBox,
                             QMessageBox, QPushButton, QTextEdit, QVBoxLayout,
                             QWidget)
from PyQt5.QtGui import QIcon

from model.refactor import QLineEdit, QLineEditTs, TsUnit, QLineEditDate
from tools import box_add_layout, generate_hbox
from utils.time_util import (extract_date, extract_time, str2timestamp,
                             timestamp2str, ts_range_by_date)


class TimeTransform(QWidget):
    """实现日期字符串与时间戳之间的转换
    """

    def __init__(self):
        super().__init__()
        self.ts_unit = TsUnit.SECOND
        self.init_ui()
        sys._excepthook = sys.excepthook
        sys.excepthook = self.exception_hook

    def exception_hook(self, exctype, value, traceback_info):
        """捕获异常并弹窗显示

        Args:
            exctype (_type_): 异常类型
            value (_type_): 异常值
            traceback (_type_): 异常的traceback
        """
        traceback_format = traceback.format_exception(exctype, value,
                                                      traceback_info)
        traceback_string = "".join(traceback_format)
        QMessageBox.critical(None, "Error", traceback_string)
        self._excepthook(exctype, value, traceback_info)

    def init_ui(self):
        """时间变换行:将日期数据与时间戳相互转换 fmt:%Y-%m-%d"""
        #显示栏
        self.date_str_line = QLineEditDate(self)
        self.ts_line = QLineEditTs(self, self.ts_unit)
        self.te_line = QLineEditTs(self, self.ts_unit)
        self.unit_line = QLineEdit(self)
        self.unit_line.setReadOnly(True)
        self.unit_line.setText(self.ts_unit.value)
        #按钮
        date_button = QPushButton("日期")
        date_button.clicked.connect(self.date_button_implement)
        ts_button = QPushButton("开始时间戳")
        ts_button.clicked.connect(lambda: self.ts2date(self.ts_line.text()))
        te_button = QPushButton("结束时间戳")
        te_button.clicked.connect(lambda: self.ts2date(self.te_line.text()))
        unit_button = QPushButton("单位")
        unit_button.clicked.connect(self.unit_transform)
        hbox_edit_line = generate_hbox(
            [self.date_str_line, self.ts_line, self.te_line, self.unit_line])
        hbox_buttion_line = generate_hbox(
            [date_button, ts_button, te_button, unit_button])
        #时间变换行: 详细数据的时间戳转换 fmt:%Y-%m-%d %H:%M:%S
        self.datetime_line = QLineEditDate(self)
        self.timestamp_line = QLineEditTs(self, self.ts_unit)

        datetime_button = QPushButton("时间")
        datetime_button.clicked.connect(self.datetime_button_implement)
        timestamp_button = QPushButton("时间戳")
        timestamp_button.clicked.connect(self.timestamp_button_implement)
        hbox_time_transform_line = generate_hbox(
            [self.datetime_line, self.timestamp_line])
        hbox_time_transform_button = generate_hbox(
            [datetime_button, timestamp_button])

        #set layout

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        box_add_layout(vbox, [
            hbox_buttion_line, hbox_edit_line, hbox_time_transform_button,
            hbox_time_transform_line
        ])
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('toys')
        self.setWindowIcon(QIcon('source/image/cat.jpg'))
        self.show()

    def date_button_implement(self):
        date = self.date_str_line.text()
        date = extract_date(date)
        ts, te = ts_range_by_date(date)
        self.ts_line.setText(ts)
        self.te_line.setText(te)

    def ts2date(self, timestamp):
        date = timestamp2str(timestamp)
        self.date_str_line.setText(date)

    def unit_transform(self):
        if self.ts_unit == TsUnit.SECOND:
            self.ts_unit = TsUnit.MILLISECOND
        else:
            self.ts_unit = TsUnit.SECOND
        self.ts_line.setUnit(self.ts_unit)
        self.te_line.setUnit(self.ts_unit)
        self.timestamp_line.setUnit(self.ts_unit)
        self.unit_line.setText(self.ts_unit.value)

    def datetime_button_implement(self):
        time_str = extract_time(self.datetime_line.text())
        timestamp = str2timestamp(time_str, fmt="%Y%m%d%H%M%S")
        self.timestamp_line.setText(timestamp)

    def timestamp_button_implement(self):
        time_str = timestamp2str(int(self.timestamp_line.text()))
        self.datetime_line.setText(time_str)

class longitude_latitude_transform(QWidget):
    """经纬度转换

    Args:
        QWidget (_type_): _description_
    """
    def __init__(self):
        super().__init__()
        self.direction = None
        self.init_ui()
        sys._excepthook = sys.excepthook
        sys.excepthook = self.exception_hook

    def exception_hook(self, exctype, value, traceback_info):
        """捕获异常并弹窗显示

        Args:
            exctype (_type_): 异常类型
            value (_type_): 异常值
            traceback (_type_): 异常的traceback
        """
        traceback_format = traceback.format_exception(exctype, value,
                                                      traceback_info)
        traceback_string = "".join(traceback_format)
        QMessageBox.critical(None, "Error", traceback_string)
        self._excepthook(exctype, value, traceback_info)

    def init_ui(self):
        #显示栏
        # prompt
        self.longitude_prompt = QLabel("经度", self)
        self.latitude_prompt = QLabel("纬度", self)
        self.direction_prompt = QLabel("方向", self)
        self.distance_prompt = QLabel("距离", self)

        # edit line
        self.longitude_line = QLineEdit(self)
        self.latitude_line = QLineEdit(self)
        self.direction_combo = QComboBox(self)
        self.direction_combo.addItem("东")
        self.direction_combo.addItem("南")
        self.direction_combo.addItem("西")
        self.direction_combo.addItem("北")
        self.direction_combo.activated[str].connect(self.dir_combo_on_activated)
        self.distance_line = QLineEdit(self)

        self.longitude_result_line = QLineEdit(self)
        self.longitude_result_line.setReadOnly(True)
        self.latitude_result_line = QLineEdit(self)
        self.latitude_result_line.setReadOnly(True)
        #self.longitude_result_line.setText(self.ts_unit.value)
        #按钮
        cal_button = QPushButton("计算")
        cal_button.clicked.connect(self.cal_button_implement)
        # ts_button = QPushButton("开始时间戳")
        # ts_button.clicked.connect(lambda: self.ts2date(self.ts_line.text()))
        # te_button = QPushButton("结束时间戳")
        # te_button.clicked.connect(lambda: self.ts2date(self.te_line.text()))
        # unit_button = QPushButton("单位")
        # unit_button.clicked.connect(self.unit_transform)
        hbox_prompt_line = generate_hbox([
            self.longitude_prompt,
            self.latitude_prompt,
            self.direction_prompt,
            self.distance_prompt,
        ])
        hbox_edit_line = generate_hbox([
            self.longitude_line,
            self.latitude_line,
            self.distance_line,
            self.direction_combo,
        ])
        hbox_buttion_line = generate_hbox(
            [cal_button])
        result_line = generate_hbox([
            self.longitude_result_line,
            self.latitude_result_line
        ])
        #时间变换行: 详细数据的时间戳转换 fmt:%Y-%m-%d %H:%M:%S
        # self.datetime_line = QLineEditDate(self)
        # self.timestamp_line = QLineEditTs(self, self.ts_unit)

        # datetime_button = QPushButton("时间")
        # datetime_button.clicked.connect(self.datetime_button_implement)
        # timestamp_button = QPushButton("时间戳")
        # timestamp_button.clicked.connect(self.timestamp_button_implement)
        # hbox_time_transform_line = generate_hbox(
        #     [self.datetime_line, self.timestamp_line])
        # hbox_time_transform_button = generate_hbox(
        #     [datetime_button, timestamp_button])

        #set layout

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        box_add_layout(vbox, [
            hbox_prompt_line,
            hbox_edit_line,
            hbox_buttion_line,
            result_line,
            #hbox_time_transform_button,
            #hbox_time_transform_line
        ])
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('toys')
        self.setWindowIcon(QIcon('source/image/cat.jpg'))
        self.show()
    
    def cal_button_implement(self):
        print("cal button")
    
    def dir_combo_on_activated(self, text):
        if (text == "东"):
            self.direction = Direction.East
        if (text == "南"):
            self.direction = Direction.South
        if (text == "西"):
            self.direction = Direction.West
        if (text == "北"):
            self.direction = Direction.North


def cal_lng(lng, lat, distance, dir):
    interval = 0.000001 # °
    gap = 1.    # 1 meters
    degrees = distance / gap * interval
    degrees = degrees if dir == Direction.East else (-1 * degrees)
    return lng + degrees, lat

def cal_lat(lng, lat, distance, dir):
    interval = 0.000001 # °
    gap = 1.1    # 1.1 meters
    degrees = distance / gap * interval
    degrees = degrees if dir == Direction.North else (-1 * degrees)
    return lng, lat + degrees

class Direction(Enum):
    North =1
    South = 2
    East = 3
    West = 4

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #time_tf = TimeTransform()
    tf = longitude_latitude_transform()
    sys.exit(app.exec_())
