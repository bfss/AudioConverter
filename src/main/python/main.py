from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QApplication, QFileDialog, QLabel,
    QMessageBox, QDesktopWidget)

import sys, os

from progress8 import Progress8

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.input_path = ''
        self.output_path = ''
        
    def initUI(self):
        
        self.input_button = QPushButton("选择mp3文件夹")
        self.output_button = QPushButton("选择输出文件夹")
        self.start_button = QPushButton('开始')

        self.input_button.clicked.connect(self.choose_input_directory)
        self.output_button.clicked.connect(self.choose_output_directory)
        self.start_button.clicked.connect(self.start)

        self.input_label = QLabel('还未选择MP3文件夹')
        self.output_label = QLabel('还未选择输出文件夹')

        self.input_hbox = QHBoxLayout()
        self.input_hbox.addWidget(self.input_button)
        self.input_hbox.addWidget(self.input_label)

        self.output_hbox = QHBoxLayout()
        self.output_hbox.addWidget(self.output_button)
        self.output_hbox.addWidget(self.output_label)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.input_hbox)
        self.vbox.addLayout(self.output_hbox)
        self.vbox.addWidget(self.start_button)
        
        self.setLayout(self.vbox)  

        self.resize(300, 300)
        self.setWindowTitle('MP3转wav小工具')  

        rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())
          
        self.show()

    def choose_input_directory(self):
        self.input_path = str(QFileDialog.getExistingDirectory(self, "选择MP3文件夹"))
        self.input_label.setText(self.input_path)

    def choose_output_directory(self):
        self.output_path = str(QFileDialog.getExistingDirectory(self, "选择输出文件夹"))
        self.output_label.setText(self.output_path)

    def start(self):
        if not self.input_path or not self.output_path:
            message_box = QMessageBox(self)
            message_box.setText('请选择对应的文件夹')
            message_box.show()
        else:
            Progress8(self, self.input_path, self.output_path)

if __name__ == '__main__':
    
    os.environ['PATH'] += ";"+os.getcwd()+"\\ffmpeg\\bin"
    appctxt = ApplicationContext()
    window = MainWindow()
   
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)