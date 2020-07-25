from PySide2.QtWidgets import (QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QApplication, QFileDialog, QLabel,
    QMessageBox, QDesktopWidget, QProgressBar, QCheckBox)
from PySide2.QtCore import QThread, Signal

import sys, os

from threads import ConvertThread

class MainWindow(QWidget):
    """主界面"""
    def __init__(self):
        super().__init__()
        self.initUI()
        self.input_path = ''
        self.output_path = ''
        
    
    def initUI(self):
        """初始化UI"""
        self.input_button = QPushButton("选择MP3文件夹")
        self.output_button = QPushButton("选择输出文件夹")
        self.start_button = QPushButton('开始')

        self.input_button.clicked.connect(self.choose_input_directory)
        self.output_button.clicked.connect(self.choose_output_directory)
        self.start_button.clicked.connect(self.start)

        self.input_label = QLabel('还未选择MP3文件夹')
        self.output_label = QLabel('还未选择输出文件夹')
        self.progress_label = QLabel('当前进度：')

        self.progress = QProgressBar(self)
        self.progress.setMaximum(100)

        self.is_contain_subdir_checkbox = QCheckBox('包含子文件夹')

        self.progress_hbox = QHBoxLayout()
        self.progress_hbox.addWidget(self.progress_label)
        self.progress_hbox.addWidget(self.progress)

        self.input_hbox = QHBoxLayout()
        self.input_hbox.addWidget(self.input_button)
        self.input_hbox.addWidget(self.input_label)

        self.output_hbox = QHBoxLayout()
        self.output_hbox.addWidget(self.output_button)
        self.output_hbox.addWidget(self.output_label)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.progress_hbox)
        self.vbox.addWidget(self.is_contain_subdir_checkbox)
        self.vbox.addLayout(self.input_hbox)
        self.vbox.addLayout(self.output_hbox)
        self.vbox.addWidget(self.start_button)
        
        self.setLayout(self.vbox)  

        self.resize(500, 300)
        self.setWindowTitle('MP3转WAV小工具')  

        rectangle = self.frameGeometry()
        center_point = QApplication.primaryScreen().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())
          
        self.show()


    def choose_input_directory(self):
        self.input_path = str(QFileDialog.getExistingDirectory(self, "选择MP3文件夹"))
        if self.input_path:
            self.input_label.setText(self.input_path)


    def choose_output_directory(self):
        self.output_path = str(QFileDialog.getExistingDirectory(self, "选择输出文件夹"))
        if self.output_path:
            self.output_label.setText(self.output_path)


    def start(self):
        print(self.output_path)
        if not self.input_path or not self.output_path:
            message_box = QMessageBox(self)
            message_box.setText('请选择对应的文件夹')
            message_box.show()
  
        else:
            self.converter = ConvertThread(self.input_path, self.output_path, self.is_contain_subdir_checkbox.isChecked())
            self.converter.countChanged.connect(self.onCountChanged)
            self.converter.start()

            self.input_button.setEnabled(False)
            self.output_button.setEnabled(False)
            self.start_button.setEnabled(False)
            self.is_contain_subdir_checkbox.setEnabled(False)


    def onCountChanged(self, value):
        self.progress.setValue(value)
        if value == 100:
            message_box = QMessageBox(self)
            message_box.setText('转换完成')
            message_box.show()

            self.input_button.setEnabled(True)
            self.output_button.setEnabled(True)
            self.start_button.setEnabled(True)
            self.is_contain_subdir_checkbox.setEnabled(True)
        elif value == 0:
            message_box = QMessageBox(self)
            message_box.setText('没有需要转换的音频')
            message_box.show()

            self.input_button.setEnabled(True)
            self.output_button.setEnabled(True)
            self.start_button.setEnabled(True)
            self.is_contain_subdir_checkbox.setEnabled(True)

    
if __name__ == '__main__':
    
    os.environ['PATH'] += ";"+os.getcwd()
    app = QApplication()
    window = MainWindow()
   
    exit_code = app.exec_()
    sys.exit(exit_code)