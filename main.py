import datetime
import re
import sys
import math
import traceback
from enum import Enum

from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QComboBox,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QIcon

from model.refactor import QLineEdit, QLineEditTs, TsUnit, QLineEditDate, QLineEditFloat
from tools import box_add_layout, generate_hbox
from utils.time_util import (
    extract_date,
    extract_time,
    str2timestamp,
    timestamp2str,
    ts_range_by_date,
)


class TimeTransform(QWidget):
    """实现日期字符串与时间戳之间的转换"""

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
        traceback_format = traceback.format_exception(exctype, value, traceback_info)
        traceback_string = "".join(traceback_format)
        QMessageBox.critical(None, "Error", traceback_string)
        self._excepthook(exctype, value, traceback_info)

    def init_ui(self):
        """时间变换行:将日期数据与时间戳相互转换 fmt:%Y-%m-%d"""
        # 显示栏
        self.date_str_line = QLineEditDate(self)
        self.ts_line = QLineEditTs(self, self.ts_unit)
        self.te_line = QLineEditTs(self, self.ts_unit)
        self.unit_line = QLineEdit(self)
        self.unit_line.setReadOnly(True)
        self.unit_line.setText(self.ts_unit.value)
        # 按钮
        date_button = QPushButton("日期")
        date_button.clicked.connect(self.date_button_implement)
        ts_button = QPushButton("开始时间戳")
        ts_button.clicked.connect(lambda: self.ts2date(self.ts_line.text()))
        te_button = QPushButton("结束时间戳")
        te_button.clicked.connect(lambda: self.ts2date(self.te_line.text()))
        unit_button = QPushButton("单位")
        unit_button.clicked.connect(self.unit_transform)
        hbox_edit_line = generate_hbox(
            [self.date_str_line, self.ts_line, self.te_line, self.unit_line]
        )
        hbox_buttion_line = generate_hbox(
            [date_button, ts_button, te_button, unit_button]
        )
        # 时间变换行: 详细数据的时间戳转换 fmt:%Y-%m-%d %H:%M:%S
        self.datetime_line = QLineEditDate(self)
        self.timestamp_line = QLineEditTs(self, self.ts_unit)

        datetime_button = QPushButton("时间")
        datetime_button.clicked.connect(self.datetime_button_implement)
        timestamp_button = QPushButton("时间戳")
        timestamp_button.clicked.connect(self.timestamp_button_implement)
        hbox_time_transform_line = generate_hbox(
            [self.datetime_line, self.timestamp_line]
        )
        hbox_time_transform_button = generate_hbox([datetime_button, timestamp_button])

        # set layout

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        box_add_layout(
            vbox,
            [
                hbox_buttion_line,
                hbox_edit_line,
                hbox_time_transform_button,
                hbox_time_transform_line,
            ],
        )
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("toys")
        self.setWindowIcon(QIcon("source/image/cat.jpg"))
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
        traceback_format = traceback.format_exception(exctype, value, traceback_info)
        traceback_string = "".join(traceback_format)
        QMessageBox.critical(None, "Error", traceback_string)
        self._excepthook(exctype, value, traceback_info)

    def init_ui(self):
        # 显示栏
        # prompt
        self.longitude_prompt = QLabel("经度", self)
        self.latitude_prompt = QLabel("纬度", self)
        self.direction_prompt = QLabel("东西(东+)", self)
        self.distance_prompt = QLabel("南北(北+)", self)

        # edit line
        self.longitude_line = QLineEditFloat(self)
        self.latitude_line = QLineEditFloat(self)
        self.lng_distance_line = QLineEditFloat(self)
        self.lat_distance_line = QLineEditFloat(self)
        self.lng_distance_line.setText(0.0)
        self.lat_distance_line.setText(0.0)

        self.longitude_result_line = QLineEdit(self)
        self.longitude_result_line.setReadOnly(True)
        self.latitude_result_line = QLineEdit(self)
        self.latitude_result_line.setReadOnly(True)

        # 按钮
        cal_button = QPushButton("计算")
        cal_button.clicked.connect(self.cal_button_implement)
        hbox_prompt_line = generate_hbox(
            [
                self.longitude_prompt,
                self.latitude_prompt,
                self.direction_prompt,
                self.distance_prompt,
            ]
        )
        hbox_edit_line = generate_hbox(
            [
                self.longitude_line,
                self.latitude_line,
                self.lng_distance_line,
                self.lat_distance_line,
            ]
        )
        hbox_button_line = generate_hbox(
            [
                cal_button,
            ]
        )
        # hbox_button_line.addStretch(1)
        result_line = generate_hbox(
            [self.longitude_result_line, self.latitude_result_line]
        )
        # 时间变换行: 详细数据的时间戳转换 fmt:%Y-%m-%d %H:%M:%S
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

        # set layout

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        box_add_layout(
            vbox,
            [
                hbox_prompt_line,
                hbox_edit_line,
                hbox_button_line,
                result_line,
                # hbox_time_transform_button,
                # hbox_time_transform_line
            ],
        )
        vbox.addStretch(1)

        self.setLayout(vbox)
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("toys")
        self.setWindowIcon(QIcon("source/image/cat.jpg"))
        self.show()

    def cal_button_implement(self):
        lng = self.longitude_line.text()
        lat = self.latitude_line.text()
        print("cal button")
        lng_distance = self.lng_distance_line.text()
        lat_distance = self.lat_distance_line.text()
        distance = math.sqrt(lng_distance**2 + lat_distance**2) / 1000
        bearing = self.calculate_bearing(lng_distance, lat_distance)
        lat, lng = self.haversine(lat, lng, distance, bearing)
        self.longitude_result_line.setText(lng)
        self.latitude_result_line.setText(lat)

    def calculate_bearing(self, east, north):
        # 使用反正切函数计算方向角
        bearing_rad = math.atan2(east, north)
        # 将弧度转换为角度
        bearing_deg = math.degrees(bearing_rad)
        # 调整角度范围为 0 到 360 度
        bearing_deg = (bearing_deg + 360) % 360

        return bearing_deg

    def haversine(self, lat1, lon1, distance, bearing):
        # 地球半径，单位：千米
        R = 6371.0
        # 将角度转换为弧度
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        bearing_rad = math.radians(bearing)
        # 计算新点的纬度
        lat2_rad = math.asin(
            math.sin(lat1_rad) * math.cos(distance / R)
            + math.cos(lat1_rad) * math.sin(distance / R) * math.cos(bearing_rad)
        )
        # 计算新点的经度
        lon2_rad = lon1_rad + math.atan2(
            math.sin(bearing_rad) * math.sin(distance / R) * math.cos(lat1_rad),
            math.cos(distance / R) - math.sin(lat1_rad) * math.sin(lat2_rad),
        )
        # 将弧度转换为角度
        lat2 = math.degrees(lat2_rad)
        lon2 = math.degrees(lon2_rad)

        return lat2, lon2


def calculate_lng_and_lat(lng, lat, lng_distance, lat_distance):
    lng_interval = 0.000001  # °
    lng_gap = 1.0  # 1 meters
    lat_interval = 0.000001  # °
    lat_gap = 1.1  # 1.1 meters

    lng_degree = lng_distance / lng_gap * lng_interval
    lat_degree = lat_distance / lat_gap * lat_interval
    return lng + lng_degree, lat + lat_degree


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Main Window")

        self.time_tf = TimeTransform()
        self.tf = longitude_latitude_transform()

        self.button = QPushButton("Switch")
        self.button.clicked.connect(self.switch)

        layout = QVBoxLayout()
        layout.addWidget(self.time_tf)
        layout.addWidget(self.tf)
        layout.addWidget(self.button)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.current_widget = self.time_tf

    def switch(self):
        if self.current_widget == self.time_tf:
            self.time_tf.hide()
            self.tf.show()
            self.current_widget = self.tf
        else:
            self.tf.hide()
            self.time_tf.show()
            self.current_widget = self.time_tf


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())