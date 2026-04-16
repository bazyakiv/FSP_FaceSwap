import cv2 as cv
import mediapipe as mp
import numpy as np
#PATHS SHORTCUT
FaceLandmarkerResult = mp.tasks.vision.FaceLandmarkerResult
class FaceSwap:
    def __init__(self):
        print("initialized");

    def update(self, detection_result: FaceLandmarkerResult, frame):
        if detection_result is None or frame is None:
            return;

        faces = detection_result.face_landmarks
        h,w = frame.shape[:2];
        face_points = []
        for face in faces:
            for landmark in face:
                face_points.append( (int(landmark.x*w), int(landmark.y * h)));


        print(face_points[0], "\n");
            

        