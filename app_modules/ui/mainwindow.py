from PySide6 import QtCore, QtWidgets, QtGui




class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, title = "Default Title", pos = (100,100), size = (800,600), centralwidget = None):
        super().__init__();

        self.setWindowTitle(title);
        self.setGeometry(pos[0], pos[1], size[0], size[1])
        if centralwidget is None:
            centralwidget = QtWidgets.QWidget();
        self.setCentralWidget(centralwidget);

        





