import mediapipe as mp
import cv2 as cv
from app_modules.videocapture import VideoStream 
from app_modules.facedetection import FaceDetector


if __name__ == "__main__":
    vs = VideoStream()
    fd = FaceDetector(visualize=True)
    vs.start() 
    fd.start()
    while True:
        frame = vs.read()
        
        if frame is not None:
            visualized = fd.update(frame)
            if visualized is not None:
                cv.imshow("visualized", visualized)
            else:
                cv.imshow("not visualized", frame)

        if cv.waitKey(1) == ord('q'):
            break

    cv.destroyAllWindows()