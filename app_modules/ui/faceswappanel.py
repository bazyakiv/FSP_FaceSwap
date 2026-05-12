from PySide6 import QtCore, QtWidgets, QtGui
from ..face.processing import FaceProcessor


from .inp.button import Button;
from .inp.filepicker import FilePicker;
from .inp.dropdown import Dropdown, Dropdown_item;

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
        layout.setSpacing(0)

        self.widgets = {}

        start_button = Button(title="Start faceswapping", method=self.start);
        start_button.setObjectName("start-button");
        stop_button = Button(title="Stop", method=self.stop)
        stop_button.setObjectName("stop-button");
        stop_button.setEnabled(False);
        items = [];
        for x in range(1,6):
            item = Dropdown_item("Camera Num." + str(x));
            items.append(item);
        dropdown = Dropdown(items, title="Camera index:");

        file_picker = FilePicker("Pick the target face:");

        preview = Preview();
        
        self.widgets['startB'] = start_button
        self.widgets['stopB'] = stop_button
        self.widgets['dropdown'] = dropdown;
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
        
        target_text, target_index = self.widgets['dropdown'].selected_item()
        
        self.fp.start(target_face=target_face, target_src=target_index);
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


