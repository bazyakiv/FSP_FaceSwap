from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt;
from .button import Button;
class FilePicker(QtWidgets.QWidget):
    def __init__(self, title="Default title:"):
        super().__init__();
        self.dialog = QtWidgets.QFileDialog();
        self.dialog.setMimeTypeFilters({"image/png"})
        
        self.last_value = None;

        label = QtWidgets.QLabel(alignment=Qt.AlignmentFlag.AlignTop);
        label.setText(title);
        upload_button = Button("Pick a file", self.pick_file)

        mainlayout = QtWidgets.QVBoxLayout();

        hLayout = QtWidgets.QHBoxLayout();
       
        hLayout.addWidget(label);
        hLayout.addWidget(upload_button);
        
        self.value_label = QtWidgets.QLabel(alignment=Qt.AlignmentFlag.AlignTop);
        self.value_label.setObjectName("filevalue")
        self.value_label.setMaximumHeight(25)
        self.value_label.setText("You haven't picked a file yet.");
        mainlayout.addSpacing(1)
        mainlayout.setContentsMargins(0,0,0,0)
        hLayout.addSpacing(1)
        hLayout.setContentsMargins(0,0,0,0)
        mainlayout.addLayout(hLayout);
        mainlayout.addWidget(self.value_label)
        
        self.setLayout(mainlayout)

    def pick_file(self):
        if(self.dialog.exec()):
            fileNames = self.dialog.selectedFiles();
            self.last_value = fileNames[0];            
            result = "Selected file: " + fileNames[0];
            self.value_label.setText(result)
            
     
        