
import sys, time, json
from types import SimpleNamespace

from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtGui import QResizeEvent, QFontMetrics
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel

import hyundai_bot, slack_client


class HyundaiProgress(QMainWindow):
    def __init__(self, parent=None):
        super(HyundaiProgress, self).__init__(parent)

        with open('config.json') as f:
            self.config = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
        self.bot = hyundai_bot.HyundaiBot(self.config)
        if self.config.enable_slack_dm:
            self.slack_client = slack_client.SlackClient(self.config.slack_oauth_token, self.config.slack_ids)

        self.setStyleSheet("QMainWindow {background: 'black';} QLabel {color: 'white';}")
        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        self.layout = QVBoxLayout()
        self.labels = []

        # self.name_label = QLabel()
        # self.name_label.setMinimumSize(1, 1)
        # self.layout.addWidget(self.name_label)
        # self.labels.append(self.name_label)

        # self.color_label = QLabel()
        # self.color_label.setMinimumSize(1, 1)
        # self.layout.addWidget(self.color_label)
        # self.labels.append(self.color_label)

        self.state_label = QLabel()
        self.state_label.setMinimumSize(1, 1)
        self.labels.append(self.state_label)
        self.layout.addWidget(self.state_label)

        self.last_update_time_label = QLabel()
        self.last_update_time_label.setMinimumSize(1, 1)
        self.labels.append(self.last_update_time_label)
        self.layout.addWidget(self.last_update_time_label)

        self.widget.setLayout(self.layout)


        self.update_info()
        
        self.update_timer = QTimer(self)   
        self.update_timer.start(900000)
        self.update_timer.timeout.connect(self.update_info) 


    def resizeEvent(self, resize_event: QResizeEvent) -> None:
        super().resizeEvent(resize_event)
        self.update_font_size()
        

    def update_font_size(self):
        current_font = self.font()
        font_metrics = QFontMetrics(current_font)
        max_ratio = sys.maxsize

        for label in self.labels:
            label_text = label.text()
            label_size = label.size()

            label_width, label_height = label_size.width(), label_size.height()            
            label_text_width = font_metrics.width(label_text + '    ')
            label_text_height = font_metrics.height()

            max_ratio = min(label_width / label_text_width, max_ratio)
            max_ratio = min(label_height / label_text_height, max_ratio)

        new_font_size = current_font.pointSizeF() * max_ratio
        current_font.setPointSizeF(new_font_size)
        for label in self.labels:
            label.setFont(current_font)



    @pyqtSlot()
    def update_info(self):
        self.info = None
        while not self.info:
            self.info = self.bot.get_info()

        result = self.info.data.resultList[0]

        # self.name_label.setText(result.saleCarCtyNm)
        # self.color_label.setText(f'{result.xrclCtyNm} - {result.ieclCtyNm}')

        old_state_text = self.state_label.text()
        new_state_text = f'{result.cnttStNm} - {result.contractStateDetailName}'
        self.state_label.setText(new_state_text)

        if self.slack_client and old_state_text != new_state_text:
            self.slack_client.send_message(new_state_text)
        
        tiemstamp = time.strftime('%m/%d %H:%M:%S', time.localtime())
        self.last_update_time_label.setText(f'Last Update: {tiemstamp}')

        self.update_font_size()