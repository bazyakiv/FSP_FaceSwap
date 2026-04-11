from app_modules.videocapture import VideoStream
import cv2 as cv
if __name__ == "__main__":
    videostreamer = VideoStream(0)
    
    videostreamer.start();
    while(True):
        frame = videostreamer.read()
       
        if frame is not None:
            cv.imshow("frame", frame)
        key = cv.waitKey(1) 

        if key == ord('s'):
            print("stop")
            videostreamer.stop()

        if key == ord('r'):
            print("restarting")
            videostreamer.start()

        if key == ord('q'):
            print("quiting")
            videostreamer.stop()
            break;

    cv.destroyAllWindows()
    