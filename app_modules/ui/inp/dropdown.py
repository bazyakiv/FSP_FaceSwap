from PySide6 import QtCore, QtWidgets, QtGui

class Dropdown_item():
    def __init__(self, text, icon = None):
        self.text = text;
    
        self.icon = QtGui.QIcon(icon);
    


class Dropdown(QtWidgets.QWidget):
    def __init__(self, items = [], title = "Dropdown:"):
        super().__init__();

        self.__layout = QtWidgets.QHBoxLayout(self);

        self.label = QtWidgets.QLabel();
        self.dropdown = QtWidgets.QComboBox();

        self.label.setText(title);

        for item in items:

            self.dropdown.addItem(item.text);

        self.__layout.addWidget(self.label);
        self.__layout.addWidget(self.dropdown);

   
    def selected_item(self):
        text= self.dropdown.currentText();
        index = self.dropdown.currentIndex();
        if text is None:
            text = "";
        if index is None:
            index = 0;
        return [text,index];


        



