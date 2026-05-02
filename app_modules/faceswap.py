import cv2 as cv
import mediapipe as mp
import numpy as np
from app_modules.facedetection import FaceDetector_img;
#PATHS SHORTCUT

FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
FACE_OVAL = [
    10, 338, 297, 332, 284, 251, 389, 356,
    454, 323, 361, 288, 397, 365, 379, 378,
    400, 377, 152, 148, 176, 149, 150, 136,
    172, 58, 132, 93, 234, 127, 162, 21,
    54, 103, 67, 109
]

FACE_KEYS = [
    4,33,263, 10 # Nose Tip, Left/Right inner eye corner, chin
]


img_path = "faceswap_image\zelya_face.png";


def normalize_image(array):
    array = np.astype(array, np.float32);
    return array/255.0

class FaceSwap:
    def __init__(self):
        print("initialized");
        self.fd = FaceDetector_img(False);
        self.read_image();
    
    def read_image(self):
        self.fd.start();
        overlay_image = cv.imread(img_path)
        self.fd.read(overlay_image);
        self.fd.close();
        overlay_faces = self.fd.last_result.face_landmarks;
        try:
            self.overlay_face = overlay_faces[0]; # get the first face
        except:
            return;
       

    def update(self, detection_result: FaceLandmarkerResult, frame): # pyright: ignore[reportInvalidTypeForm]
        if detection_result is None or frame is None:
            return;

        faces = detection_result.face_landmarks # face detection face landmarks

        try:
            face = faces[0]; # get the first face
        except:
            return frame;

        h,w = frame.shape[:2];  # get the height and width of the frame
        face_points = []
   
       
        

        for landmark in face:
            pos_x = int(landmark.x * w); # convert float range(0-1) to integer position
            pos_y = int(landmark.y * h);
            face_points.append((pos_x, pos_y)); #FACE OVAL POINTS;

    
        key_facepoints = np.array([face_points[i] for i in FACE_KEYS]) # get the key  points


        
    


        overlay_image = cv.imread(img_path) # get the target face

        

        

        ov_h, ov_w = overlay_image.shape[:2];
        overlay_face_points = [];
        for landmark in self.overlay_face:
            pos_x = int(landmark.x * ov_w); # convert float range(0-1) to integer position
            pos_y = int(landmark.y * ov_h);
            overlay_face_points.append((pos_x, pos_y)); #FACE OVAL POINTS;

        

        

        overlay_key_facepoints = np.array([overlay_face_points[i] for i in FACE_KEYS]) # get the key points
        overlay_faceoutline = np.array([overlay_face_points[i] for i in FACE_OVAL]) # get all the positions from the oval points list

        
        
        mask = np.zeros((ov_h,ov_w), dtype=np.uint8) # create an empty mask
        
        cv.fillConvexPoly(mask, overlay_faceoutline, 255); # create a polygon figure and fill it with white color, that will represent our mask
       

        src_pts = np.float32([overlay_key_facepoints[0], overlay_key_facepoints[1], overlay_key_facepoints[2], overlay_key_facepoints[3]])
        dst_pts = np.float32([key_facepoints[0], key_facepoints[1], key_facepoints[2],key_facepoints[3]])

        matrix = cv.getPerspectiveTransform(src_pts, dst_pts);
        overlay_image = cv.warpPerspective(overlay_image, matrix, (w, h))
        mask = cv.warpPerspective(mask, matrix, (w, h))
        overlay_image = np.astype(overlay_image, np.float32)
        mask = cv.blur(src=mask, ksize=(15,15)); # blur the edges for smooth transitions
        normalized_mask = normalize_image(mask); # normalize from values from 0-255 to 0-1
        normalized_mask = np.expand_dims(normalized_mask, axis=2); # add the channel axis to the mask, since it only has (h,w) but it needs (h,w,1)
        try:
           

            foreground = overlay_image * normalized_mask ; # cut out the target face to match the masks shape
            
            background = frame * (1.0 - normalized_mask); # cut out the current face from the original frame
          
                
            together = np.astype(foreground + background, np.uint8); # add the layers, and convert them into integer values
                
        
            return together; # return the frame!
        except:
            print("Couldn't insert frame");
        
    
        

        

        return frame;
        
            
