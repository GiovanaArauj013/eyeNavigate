import cv2
from mtcnn import MTCNN

cap = cv2.VideoCapture(0)
detector = MTCNN()


while True:
    
   ret,frame = cap.read()
   faces = detector.detect_faces(frame)

   for face in faces:
      x,y,w,h = face['box']
      cv2.rectangle(frame,pt1=(x,y), pt2=(x+w,y+h),color=(255,0,0),thickness=2)
      cv2.imshow('Detector de face com MTCNN',frame)

   if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
