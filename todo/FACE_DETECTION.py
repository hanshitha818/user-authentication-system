import cv2
import time
import numpy
import shutil
import os

def save_image(R_name):
  cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

  # Create the haar cascade
  faceCascade = cv2.CascadeClassifier("face_detection.xml")
  print(faceCascade)
  get_image = 0
  path = '.\data'

  while True:
    ret, frame = cap.read()

    try:
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

      # Detect faces in the image
      faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
      )


      print("Found {0} faces!".format(len(faces)))

      if(get_image==1):
        os.makedirs(path + '/' + R_name)
        cv2.imwrite(path + '/' + R_name + '/' + R_name + '.png',frame)        
        break
        

      if len(faces)>0:
        if(len(faces)==1):
          get_image = 1      
        for(x, y, w, h) in faces:
          cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

      cv2.imshow('frame', frame)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    except:
      print('Please Connect Camera Properly')
      cv2.waitKey(1000)
      return 0

  cv2.waitKey(2)
  cv2.destroyAllWindows()
  return 1
# save_image('ajay')
