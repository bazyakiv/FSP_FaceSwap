import sys
from PySide6 import QtCore, QtWidgets, QtGui
class Application:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        

    def run(self, window):
        window.show();
        sys.exit(self.app.exec());

        