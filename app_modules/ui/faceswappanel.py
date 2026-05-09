from PySide6 import QtCore, QtWidgets, QtGui
from .inp.button import Button;
from .interface.preview import Preview
import cv2 as cv

class FaceSwapPanel(QtWidgets.QWidget):
    def __init__(self, processor):
        super().__init__();
        
        self.fp = processor;
        self.timer = QtCore.QTimer();

        layout = QtWidgets.QVBoxLayout();
        
        self.widgets = {}

        start_button = Button(title="Start faceswapping", method=self.start);
        stop_button = Button(title="Stop", method=self.stop)
        stop_button.setEnabled(False);
        preview = Preview();
        
        self.widgets['startB'] = start_button
        self.widgets['stopB'] = stop_button
        self.widgets['preview'] = preview

        for widget in self.widgets.values():
            layout.addWidget(widget);
        self.setLayout(layout);
        self.timer.timeout.connect(self.on_tick)

    def start(self):
        self.fp.start();
        self.timer.start(1);

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


