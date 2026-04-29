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


def normalize_image(array):
    array = np.astype(array, np.float32);
    return array/255.0



class FaceSwap:
    def __init__(self):
        print("initialized");
    
    

    def update(self, detection_result: FaceLandmarkerResult, frame): # pyright: ignore[reportInvalidTypeForm]
        if detection_result is None or frame is None:
            return;

        faces = detection_result.face_landmarks # face detection face landmarks

        try:
            face = faces[0]; # get the first face
        except:
            return frame;

        h,w = frame.shape[:2]; 3 # get the height and width of the frame
        face_points = []
   
       
        

        for landmark in face:
            pos_x = int(landmark.x * w); # convert float range(0-1) to integer position
            pos_y = int(landmark.y * h);
            face_points.append((pos_x, pos_y)); #FACE OVAL POINTS;

        min_y = face_points[0][1]; # get start y and end y
        max_y = face_points[0][1];

        min_x = face_points[0][0]; # get start x and end x
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

        
        face_bounding_box = [(min_x, min_y), (max_x, max_y)]; # create the boundaries of the face

        


        mask = np.zeros((h,w), dtype=np.uint8) # create an empty mask
        
        face_outline = np.array([face_points[i] for i in FACE_OVAL]) # get all the positions from the oval points list
        face_outline = np.array(face_outline)


        cv.fillConvexPoly(mask, face_outline, 255); # create a polygon figure and fill it with white color, that will represent our mask
        mask = cv.blur(src=mask, ksize=(15,15)); # blur the edges for smooth transitions
        normalized_mask = normalize_image(mask); # normalize from values from 0-255 to 0-1
        normalized_mask = np.expand_dims(normalized_mask, axis=2); # add the channel axis to the mask, since it only has (h,w) but it needs (h,w,1)


        overlay_image = np.astype(cv.imread("faceswap_image\zelya_face.png"), np.float32) # get the target face
        
        overlay_width = face_bounding_box[1][0] - face_bounding_box[0][0];
        overlay_height = face_bounding_box[1][1] - face_bounding_box[0][1];
        overlay_position = (face_bounding_box[0][0], face_bounding_box[0][1]);
        overlay_image = cv.resize(src=overlay_image, dsize=(overlay_width, overlay_height), interpolation=cv.INTER_LINEAR); # resize the target face to the boundary size
        
      
        

        try:
            mask_roi = normalized_mask[face_bounding_box[0][1]:face_bounding_box[1][1], face_bounding_box[0][0]:face_bounding_box[1][0]] # get the region of interest for the face only

            foreground = overlay_image * mask_roi ; # cut out the target face to match the masks shape
            
            background = frame * (1.0 - normalized_mask); # cut out the current face from the original frame
            background = background[face_bounding_box[0][1]:face_bounding_box[1][1], face_bounding_box[0][0]:face_bounding_box[1][0]] # get the ROI of the face
                
            together = np.astype(foreground + background, np.uint8); # add the layers, and convert them into integer values
                
            frame[face_bounding_box[0][1]:face_bounding_box[1][1], face_bounding_box[0][0]:face_bounding_box[1][0]] = together # replace the ROI region with new swapped face
            return frame; # return the frame!
        except:
            print("Couldn't insert frame");
        
    
        

        

        return frame;
        
            
