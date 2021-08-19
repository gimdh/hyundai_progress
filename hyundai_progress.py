
import sys, time

from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtGui import QResizeEvent, QFontMetrics
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel

import hyundai_bot


class HyundaiProgress(QMainWindow):
    def __init__(self, parent=None):
        super(HyundaiProgress, self).__init__(parent)

        self.setStyleSheet("QMainWindow {background: 'black';} QLabel {color: 'white';}")
        
        self.bot = hyundai_bot.HyundaiBot()

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        self.layout = QVBoxLayout()
        self.labels = []

        # self.name_label = QLabel()
        # self.layout.addWidget(self.name_label)
        # self.labels.append(self.name_label)

        # self.color_label = QLabel()
        # self.layout.addWidget(self.color_label)
        # self.labels.append(self.color_label)

        self.state_label = QLabel()
        self.labels.append(self.state_label)
        self.layout.addWidget(self.state_label)

        self.last_update_time_label = QLabel()
        self.labels.append(self.last_update_time_label)
        self.layout.addWidget(self.last_update_time_label)

        self.widget.setLayout(self.layout)


        self.update_info()
        
        self.update_timer = QTimer(self)   
        self.update_timer.start(300000)
        self.update_timer.timeout.connect(self.update_info) 


    def resizeEvent(self, resize_event: QResizeEvent) -> None:
        super().resizeEvent(resize_event)
        
        current_font = self.font()
        font_metrics = QFontMetrics(current_font)
        max_ratio = sys.maxsize

        for label in self.labels:
            label_text = label.text()
            label_size = label.size()

            label_width, label_height = label_size.width(), label_size.height()            
            label_text_width = font_metrics.width(label_text)
            label_text_height = font_metrics.height()

            max_ratio = min(label_width / label_text_width, max_ratio)
            max_ratio = min(label_height / label_text_height, max_ratio)

        new_font_size = current_font.pointSizeF() * max_ratio

        current_font.setPointSizeF(new_font_size)
        for label in self.labels:
            label.setFont(current_font)



    @pyqtSlot()
    def update_info(self):
        self.info = self.bot.get_info()

        result = self.info.data.resultList[0]

        # self.name_label.setText(result.saleCarCtyNm)
        # self.color_label.setText(f'{result.xrclCtyNm} - {result.ieclCtyNm}')
        self.state_label.setText(f'{result.cnttStNm} - {result.contractStateDetailName}')
        
        tiemstamp = time.strftime('%m/%d %H:%M:%S', time.localtime())
        self.last_update_time_label.setText(f'Last Update: {tiemstamp}')

