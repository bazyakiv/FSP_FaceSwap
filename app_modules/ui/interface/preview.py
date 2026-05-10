from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt
class Preview(QtWidgets.QWidget):
    def __init__(self):
        super().__init__();
        self.frame = QtWidgets.QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        self.frame.setObjectName("preview-text")
        
        self.frame.setText("No preview");

        self.layout = QtWidgets.QHBoxLayout(self);
        self.layout.addWidget(self.frame);
    

    def update(self, frame):
        convert = QtGui.QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QtGui.QImage.Format.Format_BGR888)
        self.frame.setPixmap(QtGui.QPixmap.fromImage(convert));

    def reset(self):
        self.frame.setText("No preview");



