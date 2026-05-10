import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QFile
class Application:
    
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.load_fonts()
        self.load_stylesheet()
        
    
    def load_fonts(self):
        fonts = ["app_modules/ui/style/fonts/JosefinSans-VariableFont_wght.ttf"];
        print("Loading fonts:....")
        for font in fonts:
            
            id = QtGui.QFontDatabase.addApplicationFont(font);


            families = QtGui.QFontDatabase.applicationFontFamilies(id);
            print("Available font families:", families)

        
        

    def load_stylesheet(self):
        qss_file = QFile("app_modules/ui/style/stylesheet.qss")
        qss_file.open(QFile.OpenModeFlag.ReadOnly);
        converted = qss_file.readAll().toStdString();
        self.app.setStyleSheet(converted);

    def run(self, window):
        window.show();
        sys.exit(self.app.exec());

        