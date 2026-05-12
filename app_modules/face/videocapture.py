import cv2 as cv
import threading 
class VideoStream:
    def __init__(self):
       
        self.__capture = None
        self.__stopped = True
        self.frame = None
        self.__lock = threading.Lock()
        self.__thread = None
        

    def start(self, src):
        if not self.__stopped:
            print("Capture is already running!");
            return;

        
        self.__capture = cv.VideoCapture(src)
        
        if(not self.__capture.isOpened):
            print("Could not open the Camera!");
            return;
        self.__stopped = False;

        self.__thread = threading.Thread(target=self.update, args=())
        self.__thread.daemon = True
        self.__thread.start();
        return self


    def update(self):
        while not self.__stopped:
            ret, frame = self.__capture.read()
            
            if not ret:
                print("Something went wrong")
                self.stop()
                break
            
            

            with self.__lock:
                self.frame = frame
                
        
            
            

    def read(self):
        with self.__lock:
            if self.frame is not None:
                return self.frame.copy()
            else:
                return None;

    def stop(self):
        self.__stopped = True;

        if not self.__thread is None:
            self.__thread.join()
        
        self.__capture.release()
        
        
