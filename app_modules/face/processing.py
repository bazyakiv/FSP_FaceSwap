from .faceswap import FaceSwap
from .facedetection import FaceDetector_ls;
from .videocapture import VideoStream
import threading 
class FaceProcessor:
    def __init__(self):
        self.__stopped = True;
        self.frame = None;
        self.__lock = threading.Lock();
        self.__thread = None

        self.vs = VideoStream();
        self.fd = FaceDetector_ls(False);
        self.fs = FaceSwap();
        

    def start(self):
        if not self.__stopped:
            print("Face processing is already running!");
            return;

        self.__stopped = False;
        self.vs.start();
        self.fd.start();
        self.__thread = threading.Thread(target = self.update,args=())
        self.__thread.daemon = True;
        self.__thread.start();
        return self;


    def update(self):
        while not self.__stopped:
            frame = self.vs.read();
            if frame is not None:
                self.fd.update(frame);

                with self.__lock:
                    self.frame = self.fs.update(self.fd.last_result, frame);


    def read(self):
        with self.__lock:
            if self.frame is not None:
                return self.frame.copy();
            else:
                return None;
    
    def stop(self):
        self.vs.stop();
        self.fd.close();
        self.__stopped = True;

        if not self.__thread is None:
            self.__thread.join()

       