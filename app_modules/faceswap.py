import cv2 as cv
import mediapipe as mp
import numpy as np
#PATHS SHORTCUT

FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
FACE_OVAL = [
    10, 338, 297, 332, 284, 251, 389, 356,
    454, 323, 361, 288, 397, 365, 379, 378,
    400, 377, 152, 148, 176, 149, 150, 136,
    172, 58, 132, 93, 234, 127, 162, 21,
    54, 103, 67, 109
]



class FaceSwap:
    def __init__(self):
        print("initialized");
    
    

    def update(self, detection_result: FaceLandmarkerResult, frame): # pyright: ignore[reportInvalidTypeForm]
        if detection_result is None or frame is None:
            return;

        faces = detection_result.face_landmarks

        try:
            face = faces[0];
        except:
            return frame;

        h,w = frame.shape[:2];
        face_points = []
   
       
        

        for landmark in face:
            pos_x = int(landmark.x * w);
            pos_y = int(landmark.y * h);
            face_points.append((pos_x, pos_y)); #FACE OVAL POINTS;

        min_y = face_points[0][1];
        max_y = face_points[0][1];

        min_x = face_points[0][0];
        max_x = face_points[0][0];
        for points in face_points:
            pos_x = points[0];
            pos_y = points[1];
            if(max_x < pos_x):
                max_x = pos_x;
            if(min_x > pos_x):
                min_x = pos_x;
        
            if(max_y < pos_y):
                max_y = pos_y;
            if(min_y > pos_y):
                min_y = pos_y;

        
        face_bounding_box = [(min_x, min_y), (max_x, max_y)];

        


        mask = np.zeros((h,w))
        face_outline = np.array([face_points[i] for i in FACE_OVAL])

        face_outline = np.array(face_outline)
        cv.fillConvexPoly(mask, face_outline, 255);

        overlay_image = cv.imread("faceswap_image\zelya_face.png")
        return mask;
        
            

        