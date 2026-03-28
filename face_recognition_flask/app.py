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

# Shared flag for controlled stop of attendance camera loop
camera_stop_requested = False

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

    print(f"Attempting to add attendance for {username} (ID: {userid}) at {current_time}")

    try:
        df = pd.read_csv(f'Attendance/Attendance-{datetoday}.csv')
        existing_rolls = [str(roll) for roll in df['Roll'].values]
        print(f"Existing rolls: {existing_rolls}")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        existing_rolls = []

    if str(userid) not in existing_rolls:
        with open(f'Attendance/Attendance-{datetoday}.csv', 'a') as f:
            f.write(f'\n{username},{userid},{current_time}')
        print(f"Attendance added for {username}")
        return True
    else:
        print(f"Attendance already exists for {username} (ID: {userid})")
        return False

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
        "mess":"No trained model found. Please add a new user and wait for training to complete before taking attendance."
    })

    global camera_stop_requested
    camera_stop_requested = False

    print("initializing camera", flush=True)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return jsonify({
            "names": names.tolist(),
            "rolls": rolls.tolist(),
            "times": times.tolist(),
            "l": l,
            "totalreg": totalreg(),
            "datetoday": datetoday2,
            "mess": "Unable to open camera. Make sure camera is connected and not used by another application."
        })

    ret = True
    
    # --- 1. SET UP THE GATEKEEPER VARIABLES ---
    blink_counter = 0
    closing = False
    face_stable_frames = 0
    eye_move_frames = 0
    prev_eye_center = None
    real_person_verified = False
    attendance_logged = False
    while ret:
        if camera_stop_requested:
            print("camera stop requested, exiting loop", flush=True)
            break
        ret, frame = cap.read()
        print("frame captured")
        
        # --- 2. RUN BLINK DETECTION FIRST ---
        # Convert frame for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        detection_result = landmarker.detect(mp_image)

        state_text = "Waiting for face..."

        # Display instructions and live state overlay
        if not real_person_verified:
            cv2.putText(frame, f"Blink {3 - blink_counter} more times to verify", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        eye_motion_verified = False
        if hasattr(detection_result, 'face_landmarks') and detection_result.face_landmarks:
            try:
                landmarks = detection_result.face_landmarks[0].landmark
                h, w, _ = frame.shape
                # Choose stable eye points from Mediapipe face mesh
                left_eye = ((landmarks[33].x + landmarks[133].x) / 2 * w, (landmarks[159].y + landmarks[145].y) / 2 * h)
                right_eye = ((landmarks[362].x + landmarks[263].x) / 2 * w, (landmarks[386].y + landmarks[374].y) / 2 * h)
                eye_center = ((left_eye[0] + right_eye[0]) / 2, (left_eye[1] + right_eye[1]) / 2)

                if prev_eye_center is not None:
                    dx = eye_center[0] - prev_eye_center[0]
                    dy = eye_center[1] - prev_eye_center[1]
                    dist = (dx*dx + dy*dy) ** 0.5
                    if dist > 6:  # movement threshold in pixels (tune for camera/resolution)
                        eye_move_frames += 1
                    else:
                        eye_move_frames = max(0, eye_move_frames - 1)

                    if eye_move_frames >= 2:
                        eye_motion_verified = True
                        state_text = "Eye movement verified"
                prev_eye_center = eye_center
            except Exception:
                eye_motion_verified = False

        if detection_result.face_blendshapes:
            # 1. A face is on screen! Increment the stability timer.
            face_stable_frames += 1
            state_text = f"Face detected (stable {face_stable_frames})"

            # 2. Only look for blinks IF the face has been stable for 5 frames (~0.17 seconds)
            if face_stable_frames > 5:
                blendshapes = detection_result.face_blendshapes[0]
                left_blink_score = 0
                right_blink_score = 0
                for shape in blendshapes:
                    if shape.category_name == 'eyeBlinkLeft':
                        left_blink_score = shape.score
                    elif shape.category_name == 'eyeBlinkRight':
                        right_blink_score = shape.score

                # Eye-specific blink detection with symmetry and thresholds
                if abs(left_blink_score - right_blink_score) > 0.20:
                    print(f"Asymmetric blink: L={left_blink_score:.2f} R={right_blink_score:.2f}")
                else:
                    avg_blink = (left_blink_score + right_blink_score) / 2
                    if avg_blink > 0.55 and not closing:
                        closing = True
                        print("Eye closing detected")
                    if closing and avg_blink < 0.35:
                        blink_counter += 1
                        print(f"Blink counted! Total: {blink_counter}")
                        closing = False
                        if blink_counter > 2:
                            real_person_verified = True
                            state_text = "Verified by blinks"

        else:
            # 3. No face detected! Reset the stability timer and the blink counter.
            face_stable_frames = 0
            closing = False

        if blink_counter > 2 or eye_motion_verified or face_stable_frames >= 200:
            real_person_verified = True

        # Live status overlay
        cv2.putText(frame, f'Status: {state_text}', (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 0), 2)

        # --- 3. RUN FACE RECOGNITION (Only if verified) ---
        if real_person_verified and not attendance_logged:
            faces = extract_faces(frame)
            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (86, 32, 251), 1)
                cv2.rectangle(frame, (x, y), (x+w, y-40), (86, 32, 251), -1)
                face = cv2.resize(frame[y:y+h, x:x+w], (50, 50))
                identified_person = identify_face(face.reshape(1, -1))[0]
                print(f"Identified person: {identified_person}")

                # Log Attendance immediately on blink + face detected
                added = add_attendance(identified_person)
                if added:
                    attendance_logged = True
                    state_text = f"Attendance logged: {identified_person}"
                else:
                    state_text = f"Attendance already exists today for {identified_person}"

                cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 1)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(50,50,255),2)
                cv2.rectangle(frame,(x,y-40),(x+w,y),(50,50,255),-1)
                cv2.putText(frame, f'{identified_person}', (x,y-15), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
                cv2.rectangle(frame, (x,y), (x+w, y+h), (50,50,255), 1)

                if imgBackground.shape[0] >= 162+480 and imgBackground.shape[1] >= 55+640:
                     imgBackground[162:162 + 480, 55:55 + 640] = frame
                     cv2.imshow('Attendance', imgBackground)
                else:
                     cv2.imshow('Attendance', frame)

                cv2.waitKey(1500)
                real_person_verified = False
                break
            else:
                state_text = "Please align your face for attendance"

                
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


@app.route('/stop', methods=['GET'])
def stop():
    global camera_stop_requested
    camera_stop_requested = True
    return jsonify({
        "success": True,
        "message": "Camera closing requested. It will stop and can be reopened with 'Take Attendance'."
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

    # train synchronously so model exists before /start is called
    train_model()

    names, rolls, times, l = extract_attendance()
    return jsonify({
        "success": True,
        "message": "User added and model updated.",
        "names": names.tolist(),
        "rolls": rolls.tolist(),
        "times": times.tolist(),
        "l": l,
        "totalreg": totalreg(),
        "datetoday": datetoday2
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080 )