import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import urllib.request
import os

# 1. Auto-Download the required AI model file (Only runs once)
model_path = 'face_landmarker.task'
if not os.path.exists(model_path):
    print("Downloading face_landmarker.task model (this might take a few seconds)...")
    url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
    urllib.request.urlretrieve(url, model_path)
    print("Download complete!")

# 2. Setup the Modern Tasks API
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=True, # <--- This is the magic setting!
    output_facial_transformation_matrixes=False,
    num_faces=1
)

# 3. Initialize the Landmarker
landmarker = vision.FaceLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
blink_counter = 0
is_blinking = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    
    # Mirror the frame
    frame = cv2.flip(frame, 1) 
    
    # OpenCV uses BGR, MediaPipe Tasks uses RGB Image objects
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    
    # 4. Run the modern detection
    detection_result = landmarker.detect(mp_image)
    
    # 5. The New Blink Logic (No Math Required!)
    if detection_result.face_blendshapes:
        # Grab the 52 blendshape scores for the first detected face
        blendshapes = detection_result.face_blendshapes[0]
        
        left_blink_score = 0
        right_blink_score = 0
        
        # Search the categories for the built-in blink scores
        for shape in blendshapes:
            if shape.category_name == 'eyeBlinkLeft':
                left_blink_score = shape.score
            elif shape.category_name == 'eyeBlinkRight':
                right_blink_score = shape.score
        
        # --- NEW CODE STARTS HERE ---
        # If either eye hits 0.35, trigger the blink
        if left_blink_score > 0.35 or right_blink_score > 0.35:
            is_blinking = True
        elif is_blinking and (left_blink_score <= 0.35 and right_blink_score <= 0.35):
            blink_counter += 1
            is_blinking = False
        # --- NEW CODE ENDS HERE ---

       # Display the new metrics
        cv2.putText(frame, f'L: {left_blink_score:.2f} R: {right_blink_score:.2f}', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, f'Total Blinks: {blink_counter}', (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
    cv2.imshow('Tasks API - Blendshapes Blink Test', frame)
    
    if cv2.waitKey(1) == 27: # Press ESC to close
        break

cap.release()
cv2.destroyAllWindows()