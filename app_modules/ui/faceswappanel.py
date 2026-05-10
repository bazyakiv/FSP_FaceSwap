from PySide6 import QtCore, QtWidgets, QtGui
from ..face.processing import FaceProcessor


from .inp.button import Button;
from .inp.filepicker import FilePicker;

from .interface.messagebox import MessageBox
from .interface.preview import Preview;

import cv2 as cv

class FaceSwapPanel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__();
        
        self.fp = FaceProcessor();
        self.timer = QtCore.QTimer();

        self.mb = MessageBox();
        
        layout = QtWidgets.QVBoxLayout();
        

        self.widgets = {}

        start_button = Button(title="Start faceswapping", method=self.start);
        start_button.setObjectName("start-button");
        stop_button = Button(title="Stop", method=self.stop)
        stop_button.setObjectName("stop-button");
        stop_button.setEnabled(False);

        file_picker = FilePicker("Pick the target face:");

        preview = Preview();
        
        self.widgets['startB'] = start_button
        self.widgets['stopB'] = stop_button
        self.widgets['fpicker'] = file_picker;
        self.widgets['preview'] = preview
        

        for widget in self.widgets.values():
            layout.addWidget(widget);
        self.setLayout(layout);
        self.timer.timeout.connect(self.on_tick)

    def start(self):
        target_face = self.widgets['fpicker'].last_value;
        if target_face is None:
            self.mb.error("No file has been selected!");
            return
        self.fp.start(target_face=target_face);
        self.timer.start(1);

        self.widgets['startB'].setEnabled(False);
        self.widgets['startB'].setEnabled(False);
        self.widgets['stopB'].setEnabled(True);

    def stop(self):
        self.timer.stop();
        self.fp.stop();
        cv.destroyAllWindows()
        self.widgets['startB'].setEnabled(True);
        self.widgets['stopB'].setEnabled(False);
        self.widgets['preview'].reset();
        

    def on_tick(self):
        frame = self.fp.read();
        if frame is not None:
            self.widgets['preview'].update(frame);


