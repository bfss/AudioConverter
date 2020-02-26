import sys
import time
import os
import logging
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QDialog,
                             QProgressBar, QPushButton)

from utils import mp32wav

class External(QThread):
    
    countChanged = pyqtSignal(int)

    def __init__(self, input_path, output_path):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        all_count = 0
        for subdir, dirs, files in os.walk(self.input_path):
            for file in files:
                if file.endswith('.mp3'):
                    all_count+=1

        success_count = 0
        for subdir, dirs, files in os.walk(self.input_path):
            for file in files:
                if file.endswith('.mp3'):
                    src = os.path.join(subdir, file)
                    dst = os.path.join(self.output_path, file.split('.')[0] + '.wav')
                    
                    mp32wav(src, dst)
                    success_count+=1
                    self.countChanged.emit(success_count/all_count*100)

class Progress8(QDialog):
    
    def __init__(self, parent, input_path, output_path):
        super().__init__(parent)
        self.input_path = input_path
        self.output_path = output_path
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Progress Bar')
        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 0, 300, 25)
        self.progress.setMaximum(100)
        self.show()

        self.calc = External(self.input_path, self.output_path)
        self.calc.countChanged.connect(self.onCountChanged)
        self.calc.start()

    def onCountChanged(self, value):
        self.progress.setValue(value)
