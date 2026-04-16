import mediapipe as mp
import cv2 as cv
from app_modules.videocapture import VideoStream 
from app_modules.facedetection import FaceDetector
from app_modules.faceswap import FaceSwap

if __name__ == "__main__":

    vs = VideoStream()
    fd = FaceDetector(visualize=True)
    fs = FaceSwap();
    vs.start() 
    fd.start()
    while True:
        frame = vs.read()
        
        if frame is not None:
            processed_frame = fd.update(frame)
        
            fs.update(fd.last_result,processed_frame);
           
            cv.imshow("vision", processed_frame)
            

        if cv.waitKey(1) == ord('q'):
            break

    cv.destroyAllWindows()