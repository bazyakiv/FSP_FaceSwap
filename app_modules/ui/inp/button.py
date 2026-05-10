from PySide6 import QtCore, QtWidgets, QtGui

class Button(QtWidgets.QPushButton):
    def __init__(self, title, method = None):
        super().__init__();
        self.setText(title);
 
        self.setMinimumHeight(15)
        if(method is None):
            self.clicked.connect(self.onclick);
        else:
            self.clicked.connect(method);
    def onclick(self):
        print("No onclicked method set!");

