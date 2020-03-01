import sys
import time
import os
import logging
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QDialog,
                             QProgressBar, QPushButton)

from utils import mp32wav

class ConvertThread(QThread):
    
    countChanged = pyqtSignal(int)

    def __init__(self, input_path, output_path, is_contain_subdir):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.is_contain_subdir = is_contain_subdir

    def run(self):
        all_count = 0
        success_count = 0
        if self.is_contain_subdir:
            for subdir, dirs, files in os.walk(self.input_path):
                for audio in files:
                    if audio.endswith('.mp3'):
                        all_count+=1

            for subdir, dirs, files in os.walk(self.input_path):
                for audio in files:
                    if audio.endswith('.mp3'):
                        src = os.path.join(subdir, audio)
                        dst = os.path.join(self.output_path, audio.split('.')[0] + '.wav')
                    
                        mp32wav(src, dst)
                        success_count+=1
                        self.countChanged.emit(success_count/all_count*100)
        else:
            dirs = os.listdir(self.input_path)
            for audio in dirs:
                input_audio = os.path.join(self.input_path, audio)
                if os.path.isfile(input_audio) and input_audio.endswith('.mp3'):
                    all_count+=1
            
            for audio in dirs:
                input_audio = os.path.join(self.input_path, audio)
                if os.path.isfile(input_audio) and input_audio.endswith('.mp3'):
                    src = os.path.join(self.input_path, audio)
                    dst = os.path.join(self.output_path, audio.split('.')[0] + '.wav')
                    
                    mp32wav(src, dst)
                    success_count+=1
                    self.countChanged.emit(success_count/all_count*100)

