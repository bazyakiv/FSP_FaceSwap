import cv2 as cv
import mediapipe as mp
import numpy as np
from .facedetection import FaceDetector_img;
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
    # Face oval
    *FACE_OVAL,
    # Eyebrows
    70, 63, 105, 66, 107,
    336, 296, 334, 293, 300,
    # Left eye
    33, 133, 159, 145, 160, 144, 161, 153,
    # Right eye
    362, 263, 386, 374, 387, 373, 388, 390,
    # Nose
    1, 2, 98, 327, 4, 19, 94,
    # Mouth
    61, 291, 0, 17, 78, 308, 13, 14, 82, 312,
    185, 40, 39, 37, 267, 269, 270, 409,
    95, 88, 178, 87, 14, 317, 402, 318
]





class FaceSwap:
    def __init__(self):
        print("initialized");
        self.fd = FaceDetector_img(False);
        self.image_processed = False;
    
    def read_image(self,target_face):
        self.fd.start();
        self.overlay_image = cv.imread(target_face)
        self.fd.read(self.overlay_image);
        self.fd.close();
        overlay_faces = self.fd.last_result.face_landmarks;
        try:
            self.overlay_face = overlay_faces[0]; # get the first face
        except:
            return;

     
        self.ov_h, self.ov_w = self.overlay_image.shape[:2];
        self.overlay_face_points = [];
        subdiv = cv.Subdiv2D((0,0,self.ov_w, self.ov_h));

        for landmark in self.overlay_face:
            pos_x = int(landmark.x *self.ov_w); # convert float range(0-1) to integer position
            pos_y = int(landmark.y * self.ov_h);
            if(pos_x < 0):
                pos_x = 1;
            elif(pos_x >= self.ov_w):
                pos_x = self.ov_w-1
            if(pos_y <0):
                pos_y = 1;
            elif(pos_y >= self.ov_h):
                pos_y = self.ov_h-1
          
            self.overlay_face_points.append((pos_x, pos_y)); 
            
     
        self.overlay_faceoutline = np.array([self.overlay_face_points[i] for i in FACE_OVAL]) # get all the positions from the oval points list
        overlay_keypositions = np.array([self.overlay_face_points[i] for i in FACE_KEYS])
        for pos in overlay_keypositions:
            subdiv.insert((int(pos[0]), int(pos[1])));
        
        def check_point(point):
            if (point[0] >= 0 and point[0] < self.ov_w) and (point[1] >= 0 and point[1] < self.ov_h):
                return True;
            return False;
            

        triangles = subdiv.getTriangleList();
        self.triangles = []


        for triangle in triangles:
            p1 = (int(triangle[0]), int(triangle[1]))
            p2 = (int(triangle[2]), int(triangle[3]))
            p3 = (int(triangle[4]), int(triangle[5]))
            points = [p1,p2,p3];
            center = np.mean([p1,p2,p3], axis=0)
       
            
            success = True;
            for point in points:
                success = check_point(point);
                if(not success):
                    break;
            
            if(not success):
                continue;

            index1 = self.overlay_face_points.index(p1)
            index2 = self.overlay_face_points.index(p2)
            index3 = self.overlay_face_points.index(p3)

            triplet = (index1, index2, index3);
           
            self.triangles.append(triplet);
    
        self.image_processed = True;
        
       

    def update(self, detection_result: FaceLandmarkerResult, frame): # pyright: ignore[reportInvalidTypeForm]
        if detection_result is None or frame is None or not self.image_processed:
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
        
        faceoutline = np.array([face_points[i] for i in FACE_OVAL])
       

        
        
        try:
           copied_frame = np.copy(frame);
           face_mask = np.zeros((h,w), dtype=np.uint8)
         
        
           face_mask = cv.fillConvexPoly(face_mask, faceoutline, 255);

           for triangle in self.triangles:
                src_points = (self.overlay_face_points[triangle[0]],self.overlay_face_points[triangle[1]],self.overlay_face_points[triangle[2]])
                dst_points = (face_points[triangle[0]],face_points[triangle[1]],face_points[triangle[2]])

                
                src_bounding_box = cv.boundingRect(np.int32(src_points));
                dst_bounding_box = cv.boundingRect(np.int32(dst_points));
                
                srcpoints = []
                dstpoints = []
                for point in src_points:
                    pointx = point[0] - src_bounding_box[0]
                    pointy = point[1] - src_bounding_box[1]
                    srcpoints.append((pointx, pointy))
                for point in dst_points:
                    pointx = point[0] - dst_bounding_box[0]
                    pointy = point[1] - dst_bounding_box[1]
                    dstpoints.append((pointx, pointy))
                d_x, d_y, d_bw, d_bh = dst_bounding_box
                s_x, s_y, s_bw, s_bh = src_bounding_box
                mask = np.zeros((d_bh, d_bw), dtype=np.uint8)
                

                mask = cv.fillConvexPoly(mask, np.int32(dstpoints), 255);
                expansion = np.ones((2,2), np.uint8);
                mask = cv.dilate(mask, expansion);
                matrix = cv.getAffineTransform(np.float32(srcpoints), np.float32(dstpoints));
                triangle_region = self.overlay_image[s_y:s_y+s_bh+5,s_x:s_x+s_bw+5]
                
                warped = cv.warpAffine(triangle_region, matrix, (d_bw, d_bh))

            

                foreground = cv.bitwise_and(warped, warped, mask= mask);
                frame_region = copied_frame[d_y:d_y + d_bh, d_x:d_x+d_bw]
                inv_mask = cv.bitwise_not(mask);
                background = cv.bitwise_and(frame_region, frame_region, mask=inv_mask)

               
                together =  cv.add(foreground, background)

                copied_frame[d_y:d_y + d_bh, d_x:d_x+d_bw] = together;
            
            
           center = np.mean(faceoutline, axis=0)
           
           return cv.seamlessClone(copied_frame, frame, face_mask, (int(center[0]), int(center[1])), cv.NORMAL_CLONE)
                
        
        except Exception as e:
            print("Couldn't insert frame", e);
        
    
        

        

        return frame;
        
            
