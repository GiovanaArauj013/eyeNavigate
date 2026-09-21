import cv2
import mediapipe as mp

cam = cv2.VideoCapture(0)

detector_face = mp.solutions.face_detection
drawing = mp.solutions.drawing_utils

with detector_face.FaceDetection(model_selection = 0, min_detection_confidence=0.7) as dec:
    while cam.isOpened():
        status, imagem = cam.read()
        if not status :
            print("Ignorando frames vazios da câmera.")
            continue

        imagem.flags.writeable = False
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        resultados = dec.process(imagem)

        imagem.flags.writeable = True
        imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)

        if resultados.detections:
            for face in resultados.detections:
                drawing.draw_detection(imagem, face)

        cv2.imshow('Detector de face com MediaPipe', cv2.flip(imagem, 1))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cam.release()
cv2.destroyAllWindows()    
