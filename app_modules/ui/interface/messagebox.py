from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QMessageBox

class MessageBox():
    def __init__(self):
        
        self.msg_box = QMessageBox();
       

    def warn(self, message):
        self.msg_box.setIcon(QMessageBox.Icon.Warning);
        self.msg_box.setWindowTitle("Warning")
        self.msg_box.setText(message);
        self.msg_box.exec();

    def error(self, message):
        self.msg_box.setIcon(QMessageBox.Icon.Critical);
        self.msg_box.setWindowTitle("Error")
        self.msg_box.setText(message);
        self.msg_box.exec();