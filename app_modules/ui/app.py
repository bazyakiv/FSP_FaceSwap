import sys
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import QFile
from ..misc.relative_path import resource_path
class Application:
    
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self.load_fonts()
        self.load_stylesheet()
        
    
    def load_fonts(self):
        fonts = [resource_path("app_modules/ui/style/fonts/JosefinSans-VariableFont_wght.ttf")];
        print("Loading fonts:....")
        for font in fonts:
            
            id = QtGui.QFontDatabase.addApplicationFont(font);


            families = QtGui.QFontDatabase.applicationFontFamilies(id);
            print("Available font families:", families)
        
        self.window_icon = QtGui.QIcon(resource_path("app_modules/ui/style/icon.ico"));
        
        

    def load_stylesheet(self):
        qss_file = QFile(resource_path("app_modules/ui/style/stylesheet.qss"))
        qss_file.open(QFile.OpenModeFlag.ReadOnly);
        converted = qss_file.readAll().toStdString();
        self.app.setStyleSheet(converted);

    def run(self, window):
        window.setWindowIcon(self.window_icon)
        window.show();
        
        sys.exit(self.app.exec());

        