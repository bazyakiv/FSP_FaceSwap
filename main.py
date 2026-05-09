
import cv2 as cv



from app_modules.face.processing import FaceProcessor

from app_modules.ui.app import Application
from app_modules.ui.mainwindow import MainWindow
from app_modules.ui.faceswappanel import FaceSwapPanel


if __name__ == "__main__":
   
    app = Application();
    fp = FaceProcessor()
    f_panel = FaceSwapPanel(fp)
    window = MainWindow("FaceSwap", (300,400), (800,600), f_panel)
  
    app.run(window);
 
            
    
    