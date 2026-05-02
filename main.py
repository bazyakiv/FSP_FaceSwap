import mediapipe as mp
import cv2 as cv
from app_modules.videocapture import VideoStream 
from app_modules.facedetection import FaceDetector_ls
from app_modules.faceswap import FaceSwap

if __name__ == "__main__":

    vs = VideoStream()
    fd = FaceDetector_ls(visualize=False) # use the livestream version of the face detector
    fs = FaceSwap();
    vs.start() 
    fd.start()
    while True:
        frame = vs.read()
        
        if frame is not None:
            processed_frame = fd.update(frame)
        
            frame2 = fs.update(fd.last_result,processed_frame);
            if frame2 is not None:
                cv.imshow("vision", frame2);
            

        if cv.waitKey(1) == ord('q'):
            break

    cv.destroyAllWindows()