from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QMessageBox
from ...misc.relative_path import resource_path
class MessageBox():
    def __init__(self):
        
        self.msg_box = QMessageBox();
        self.msg_box.setWindowIcon(QtGui.QIcon(resource_path("app_modules/ui/style/msgbox.ico")));
       

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