import cv2
print ("import starting")
import os
from flask import Flask, jsonify, request
from datetime import date
from datetime import datetime
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import joblib
from flask_cors import CORS
import threading
# --- NEW MEDIAPIPE BLINK DETECTOR INITIALIZATION ---
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

print("Loading Blink Detection AI Model...")
base_options = python.BaseOptions(model_asset_path=r"A:\smart attendance system\face__recognition-main\face_recognition_flask\face_landmarker.task")
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=True,
    output_facial_transformation_matrixes=False,
    num_faces=1
)
landmarker = vision.FaceLandmarker.create_from_options(options)
print("Model Loaded Successfully!")
# ---------------------------------------------------
# app instance 
app = Flask(__name__)
CORS(app)


nimgs = 50

imgBackground=cv2.imread("background.png")

datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")


face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


if not os.path.isdir('Attendance'):
    os.makedirs('Attendance')
if not os.path.isdir('static'):
    os.makedirs('static')
if not os.path.isdir('static/faces'):
    os.makedirs('static/faces')
if f'Attendance-{datetoday}.csv' not in os.listdir('Attendance'):
    with open(f'Attendance/Attendance-{datetoday}.csv', 'w') as f:
        f.write('Name,Roll,Time')

def totalreg():
    return len(os.listdir('static/faces'))

def extract_faces(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
        return face_points
    except:
        return []

def identify_face(facearray):
    model = joblib.load('static/face_recognition_model.pkl')
    return model.predict(facearray)


def train_model():
    faces = []
    labels = []
    userlist = os.listdir('static/faces')
    for user in userlist:
        for imgname in os.listdir(f'static/faces/{user}'):
            img = cv2.imread(f'static/faces/{user}/{imgname}')
            resized_face = cv2.resize(img, (50, 50))
            faces.append(resized_face.ravel())
            labels.append(user)
    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces, labels)
    joblib.dump(knn, 'static/face_recognition_model.pkl')

def extract_attendance():
    df = pd.read_csv(f'Attendance/Attendance-{datetoday}.csv')
    names = df['Name']
    rolls = df['Roll']
    times = df['Time']
    l = len(df)
    return names, rolls, times, l

def add_attendance(name):
    username = name.split('_')[0]
    userid = name.split('_')[1]
    current_time = datetime.now().strftime("%H:%M:%S")

    # Safely read the CSV and check for duplicates using strings
    try:
        df = pd.read_csv(f'Attendance/Attendance-{datetoday}.csv')
        # Convert all existing IDs to strings to avoid mismatch errors
        existing_rolls = [str(roll) for roll in df['Roll'].values]
    except Exception as e:
        # If the file is empty or has an error, assume no one is marked yet
        existing_rolls = []

    # Only write to the file if the ID is NOT already in the list
    if str(userid) not in existing_rolls:
        with open(f'Attendance/Attendance-{datetoday}.csv', 'a') as f:
            f.write(f'\n{username},{userid},{current_time}')

def getallusers():
    userlist = os.listdir('static/faces')
    names = []
    rolls = []
    l = len(userlist)

    for i in userlist:
        name, roll = i.split('_')
        names.append(name)
        rolls.append(roll)

    return userlist, names, rolls, l


# --- नया /attendance राउट यहाँ ऐड किया गया है ---
@app.route('/attendance', methods=['GET'])
def attendance():
    names, rolls, times, l = extract_attendance()
    return jsonify({
        "names": names.tolist(),
        "rolls": rolls.tolist(),
        "times": times.tolist(),
        "l": l,
        "totalreg": totalreg(),
        "datetoday": datetoday2
    })


@app.route('/')
def home():
    names, rolls, times, l = extract_attendance()
    return jsonify({
        "names": names.tolist(),
        "rolls": rolls.tolist(),
        "times": times.tolist(),
        "l": l,
        "totalreg": totalreg(),
        "datetoday": datetoday2
    })

@app.route('/start', methods=['GET'])
def start():
    names, rolls, times, l = extract_attendance()

    if 'face_recognition_model.pkl' not in os.listdir('static'):
        return jsonify({
        "names": names.tolist(),
        "rolls": rolls.tolist(),
        "times": times.tolist(),
        "l": l,
        "totalreg": totalreg(),
        "datetoday": datetoday2,
        "mess":"There is no trained model in the static folder. Please add a new face to continue."
    })

    ret = True
    print("initializing camera", flush=True) 
    cap = cv2.VideoCapture(0)
    
    # --- 1. SET UP THE GATEKEEPER VARIABLES ---
    blink_counter = 0
    closed_frames = 0 
    face_stable_frames = 0 # <--- NEW: Tracks how long a face has been continuously visible
    real_person_verified = False
    while ret:
        ret, frame = cap.read()
        print("frame captured")
        
        # --- 2. RUN BLINK DETECTION FIRST ---
        # Convert frame for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        detection_result = landmarker.detect(mp_image)
        
        # Display instructions
        if not real_person_verified:
             cv2.putText(frame, "Please Blink to Verify", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        if detection_result.face_blendshapes:
            # 1. A face is on screen! Increment the stability timer.
            face_stable_frames += 1
            
            # 2. Only look for blinks IF the face has been stable for 15 frames (~0.5 seconds)
            if face_stable_frames > 15:
                blendshapes = detection_result.face_blendshapes[0]
                
                left_blink_score = 0
                right_blink_score = 0
                
                for shape in blendshapes:
                    if shape.category_name == 'eyeBlinkLeft':
                        left_blink_score = shape.score
                    elif shape.category_name == 'eyeBlinkRight':
                        right_blink_score = shape.score
                
              # --- THE ULTIMATE ANTI-SPOOFING GATEKEEPER ---
        
        # 1. THE SYMMETRY LOCK: Real eyes blink perfectly together.
        # Shaking the phone causes the mesh to tear, creating uneven scores.
        # If the difference between the eyes is > 15%, it is a fake!
                if abs(left_blink_score - right_blink_score) > 0.15:
                	closed_frames = 0 # Cancel the sequence immediately
            
                else:
                	# 2. Require BOTH eyes to close deeply and evenly
                	if left_blink_score > 0.5 and right_blink_score > 0.5:
                	  closed_frames += 1
            
                	# 3. Require BOTH eyes to cleanly open
                	elif left_blink_score < 0.35 and right_blink_score < 0.35:
                
                		# 4. The Goldilocks Check (2 to 8 frames)
                		if closed_frames >= 2 and closed_frames <= 8: 
                    		  blink_counter += 1
                    		  real_person_verified = True # <--- THE GATE IS OPEN!
                    
                		# Reset the counter
                		closed_frames = 0
            else:
                # The face is still too new. Let the motion blur settle.
                cv2.putText(frame, "Stabilizing...", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        else:
            # 3. No face detected! Reset the stability timer and the blink counter.
            face_stable_frames = 0
            closed_frames = 0

        # --- 3. RUN FACE RECOGNITION (Only if verified) ---
        if real_person_verified:
            if len(extract_faces(frame)) > 0:
                (x, y, w, h) = extract_faces(frame)[0]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (86, 32, 251), 1)
                cv2.rectangle(frame, (x, y), (x+w, y-40), (86, 32, 251), -1)
                face = cv2.resize(frame[y:y+h, x:x+w], (50, 50))
                identified_person = identify_face(face.reshape(1, -1))[0]
                
                # Log Attendance
                add_attendance(identified_person)
                
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
                cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1)
                cv2.putText(frame, f'{identified_person}', (x,y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
                cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)
                
                # Check background size
                if imgBackground.shape[0] >= 162+480 and imgBackground.shape[1] >= 55+640:
                     imgBackground[162:162 + 480, 55:55 + 640] = frame
                     cv2.imshow('Attendance', imgBackground)
                else:
                     cv2.imshow('Attendance', frame)
                
                cv2.waitKey(1500)
                
                # Reset verification so the next person has to blink too
                real_person_verified = False 
                break # Exit loop after logging attendance

        else:
            # 4. NO BLINK YET: Keep showing the live camera feed
            cv2.imshow('Attendance', frame)
            if cv2.waitKey(1) == 27: # Press ESC to manually cancel if needed
                break
                
    cap.release()
    cv2.destroyAllWindows()
    names, rolls, times, l = extract_attendance()
    return jsonify({
        "names": names.tolist(),
        "rolls": rolls.tolist(),
        "times": times.tolist(),
        "l": l,
        "totalreg": totalreg(),
        "datetoday": datetoday2
    })


@app.route('/add', methods=['GET', 'POST'])
def add():
    newusername = request.form['newusername']
    newuserid = request.form['newuserid']
    userimagefolder = 'static/faces/'+newusername+'_'+str(newuserid)
    if not os.path.isdir(userimagefolder):
        os.makedirs(userimagefolder)
    i, j = 0, 0
    cap = cv2.VideoCapture(0)
    while 1:
        _, frame = cap.read()
        faces = extract_faces(frame)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 20), 2)
            cv2.putText(frame, f'Images Captured: {i}/{nimgs}', (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 20), 2, cv2.LINE_AA)
            if j % 5 == 0:
                name = newusername+'_'+str(i)+'.jpg'
                cv2.imwrite(userimagefolder+'/'+name, frame[y:y+h, x:x+w])
                i += 1
            j += 1
        if i == nimgs:
            break
        cv2.imshow('Adding new User', frame)
        if cv2.waitKey(1) == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    print('Training Model')
    
    threading.Thread(target=train_model).start() # <-- यहाँ () मिसिंग था
    
    names, rolls, times, l = extract_attendance()
    return jsonify({
        "names": names.tolist(),
        "rolls": rolls.tolist(),
        "times": times.tolist(),
        "l": l,
        "totalreg": totalreg(),
        "datetoday": datetoday2
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080 )