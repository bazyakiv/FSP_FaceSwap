import cv2 as cv
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles
from mediapipe.tasks.python.vision.drawing_utils import DrawingSpec
import time
#PATHS SHORTCUT
BaseOptions = mp.tasks.BaseOptions
FaceLandmarker  = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode
def print_result(result: FaceLandmarkerResult, output_image: mp.Image, timestamp_ms: int): # pyright: ignore[reportInvalidTypeForm]
    print('face landmarker result: {}'.format(result))

class FaceDetector:
     
     def callback(self, result: FaceLandmarkerResult, output_image: mp.Image, timestamp_ms: int): # pyright: ignore[reportInvalidTypeForm]
         self.last_result = result;
     
     def visualization(self, frame):
        
        if self.last_result is None or not self.last_result.face_landmarks:
            return frame

        landmarks_list = self.last_result.face_landmarks
    
        for landmarks in landmarks_list:
            spec = DrawingSpec(color=(181,101,100), thickness=2)
            drawing_utils.draw_landmarks(
            image=frame,
            landmark_list=landmarks,
            connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_TESSELATION,
             landmark_drawing_spec=None,
             connection_drawing_spec=spec
            )
            
            drawing_utils.draw_landmarks(
                image=frame,
                landmark_list=landmarks,
                connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_CONTOURS,
                 landmark_drawing_spec=None,
                 connection_drawing_spec=spec
            )
            drawing_utils.draw_landmarks(
                image=frame,
                landmark_list=landmarks,
                connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_LEFT_IRIS,
                 landmark_drawing_spec=None,
                 connection_drawing_spec=spec
            )
            drawing_utils.draw_landmarks(
                image=frame,
                landmark_list=landmarks,
                connections=vision.FaceLandmarksConnections.FACE_LANDMARKS_RIGHT_IRIS,
                 landmark_drawing_spec=None,
                 connection_drawing_spec=spec
            )
        return frame
    


class FaceDetector_ls(FaceDetector):
    def __init__(self, visualize=True):
        self.__options = FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=r"detection_model\face_landmarker.task"),
            running_mode = VisionRunningMode.LIVE_STREAM,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            num_faces = 1,
            result_callback = self.callback
        )
        self.landmarker = None
        self.last_result = None
        self.visualize = visualize;
        self.last_timestamp = 0

    def start(self):
        self.landmarker = FaceLandmarker.create_from_options(self.__options);

    
    def update(self, frame):
        if self.landmarker is None or frame is None:
            return
    
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        
        timestamp = int(time.time() * 1000)
        if timestamp <= self.last_timestamp:
            timestamp = self.last_timestamp + 1;
        self.last_timestamp = timestamp;
        self.landmarker.detect_async(image, timestamp)

        if self.visualize:
            return self.visualization(frame=frame);
        else:
            return frame;

    def close(self):
        if self.landmarker:
            self.landmarker.close()
    pass


class FaceDetector_img(FaceDetector):    
    def __init__(self, visualize=True):
        self.__options = FaceLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=r"detection_model\face_landmarker.task"),
            running_mode = VisionRunningMode.IMAGE,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
            num_faces = 1,
        )
        self.landmarker = None
        self.last_result = None
        self.visualize = visualize;
    
    def start(self):
        self.landmarker = FaceLandmarker.create_from_options(self.__options);

    
    def read(self, frame):
        if self.landmarker is None or frame is None:
            return
    
        rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        
        result = self.landmarker.detect(image)
        self.last_result = result;
        if self.visualize:
            return self.visualization(frame=frame);
        else:
            return frame;

    def close(self):
        if self.landmarker:
            self.landmarker.close()
