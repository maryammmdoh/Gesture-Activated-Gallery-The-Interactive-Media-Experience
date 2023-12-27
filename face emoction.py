import cv2
from deepface import DeepFace
import numpy as np
#face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
#face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')




video=cv2.VideoCapture(0)

while True:
    ret,frame=video.read()
   # face_cascade = cv2.CascadeClassifier("C:\\project HCI\\haarcascade_frontalface_default.xml")
    face_cascade = cv2.CascadeClassifier( "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face=face_cascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5)
    for x,y,w,e in face:
        img=cv2.rectangle(frame,(x,y),(x+w,y+e),(0,0,255),1)
        try:
            analyze=DeepFace.analyze(frame,actions=['emotion'])
            print(analyze['dominant_emotion'])
        except:
           print("no face")

    cv2.imshow('video',frame)
    cv2.waitKey(1)
    video.release()
    
    cv2.destroyAllWindows()