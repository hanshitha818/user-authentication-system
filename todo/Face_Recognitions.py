import FRM
import cv2

import os
from glob import glob


def face_id(user_name):
    iterations = 0

    video_capture = cv2.VideoCapture(0)
    directory = os.getcwd()
    persons = glob(directory+'/data/*')
    known_face_encodings = []
    known_face_names = []

    for person_name in persons:
        Known_names = os.path.basename(person_name)
        path = os.path.join(person_name, '*.png')
        for img in glob(path):
            print(img)
            face_image = FRM.load_image_file(img)
            face_encoding = FRM.face_encodings(face_image)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(Known_names)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        iterations+=1
        ret, frame = video_capture.read()        
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
       
        if process_this_frame:
          
            face_locations = FRM.face_locations(rgb_small_frame)
            face_encodings = FRM.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                
                matches = FRM.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
              
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                face_names.append(name)
               

        process_this_frame = not process_this_frame
        
        for (top, right, bottom, left), name in zip(face_locations, face_names):
          
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4



            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
     
        cv2.imshow('Video', frame)       
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if(len(face_names)==1):
            if face_names[0]==user_name:
                print('AUTHENTICATION DONE USING FACE RECOGNITION')
                cv2.waitKey(100)
                video_capture.release()
                cv2.destroyAllWindows()
                return 1
                break

        if(len(face_names)==1):
            if face_names[0]=='Unknown':
                print('FACE RECOGNITION FAIL')
                cv2.waitKey(100)
                video_capture.release()
                cv2.destroyAllWindows()
                return 0
                break

        if(iterations > 100):
            cv2.waitKey(50)
            try:
                print('FACE RECOGNITION FAIL')
                video_capture.release()
                cv2.destroyAllWindows()
                return 0
                break
            except:
                print('FACE RECOGNITION FAIL')
                return 0
                break

