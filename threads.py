import sys
import time
import os
import logging
from PySide2.QtCore import QThread, Signal
from PySide2.QtWidgets import (QApplication, QDialog,
                             QProgressBar, QPushButton)

from utils import mp32wav

class ConvertThread(QThread):
    countChanged = Signal(int)

    def __init__(self, input_path, output_path, is_contain_subdir):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.is_contain_subdir = is_contain_subdir


    def run(self):
        """线程执行"""
        need_convert = []
        # 获取所有需要转换的文件列表
        if self.is_contain_subdir:
            for subdir, dirs, files in os.walk(self.input_path):
                for audio in files:
                    if audio.endswith('.mp3'):
                        need_convert.append(os.path.join(subdir, audio))
        else:
            dirs = os.listdir(self.input_path)
            for audio in dirs:
                input_audio = os.path.join(self.input_path, audio)
                if os.path.isfile(input_audio) and input_audio.endswith('.mp3'):
                    need_convert.append(input_audio)
            
        self.convert(need_convert)


    def convert(self, need_convert):
        """转换列表内所有音频"""
        success_count = 0
        all_count = len(need_convert)
        if all_count == 0:
            self.countChanged.emit(0)
        else:
            for audio in need_convert:
                src = audio
                
                dst = os.path.join(self.output_path, audio.split(os.path.sep)[-1].split('.')[0] + '.wav')
                
                mp32wav(src, dst)
                success_count+=1
                self.countChanged.emit(success_count/all_count*100)
        

