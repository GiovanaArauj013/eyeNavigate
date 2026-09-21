import cv2
import mediapipe as mp
import os
import collections
import numpy as np
import pyautogui
from pynput.mouse import Controller
mouse = Controller()

janela_largura, janela_altura = pyautogui.size()
detector_face = mp.solutions.face_detection
drawing = mp.solutions.drawing_utils
cam = cv2.VideoCapture(0)
track_points = collections.deque(maxlen=14)
MOVE_THRESHOLD = 30
coordenadasDireita = None
coordenadasEsquerda = None
coordenadasAtuais = None

######################################ENQUADRAMENTO########################################################

pyautogui.alert("O código irá começar, se posicione no enquadramneto da câmera, quando satifeito, presione Q")

if not cam.isOpened():
    pyautogui.alert("Erro ao abrir a câmera!")
    exit()


while True:
    

    ret, frame = cam.read()
    frame = cv2.resize(frame, (janela_largura, janela_altura))
    cv2.imshow('Camera', frame)
    if not ret:
        print("Falha ao capturar o quadro!")
        break


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()


###################### ABRIR PRIMEIRO VIDEO DE CALIBRAGEM ############################

caminho_video1 = '/home/giovana/Área de trabalho/eyeNavigate/v3/calibragemDireita.mp4'

cap = cv2.VideoCapture(caminho_video1)

if not cap.isOpened():
    pyautogui.alert("Erro ao abrir o vídeo!")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Video', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


######################## faz a captura da coordeenadas (lado direito)#############################

cam = cv2.VideoCapture(0)
counter = 0

with detector_face.FaceDetection(model_selection = 1, min_detection_confidence=1) as dec:   
    while cam.isOpened():
        counter += 1
        status, imagem = cam.read()
       
        if not status :
            print("Ignorando frames vazios da câmera.")
            continue

        imagem.flags.writeable = False
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        resultados = dec.process(imagem)
        frame_height, frame_width, c = imagem.shape

        imagem.flags.writeable = True
        imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)

        if resultados.detections:
            detection = resultados.detections[0] 
            drawing.draw_detection(imagem, detection)
            face_react = np.multiply(
                    [
                        detection.location_data.relative_bounding_box.xmin,
                        detection.location_data.relative_bounding_box.ymin,
                        detection.location_data.relative_bounding_box.width,
                        detection.location_data.relative_bounding_box.height,
                    ],
                    [frame_width, frame_height, frame_width, frame_height],
                ).astype(int)

            fx, fy, _, _ = face_react

            track_points.appendleft([fx, fy])
            if (counter <= 10):
             for i in range(1, len(track_points)):
                if counter >= 10 and i == 1 and track_points[-10] is not None:
                    dX = track_points[-10][0] - track_points[i][0]
                    dY = track_points[-10][1] - track_points[i][1]
                    direction_x, direction_y = "", ""
                    coordenadasDireita = face_react
                    print (coordenadasDireita)
            else: break

                            
cam.release() 
cv2.destroyAllWindows()    


###################### ABRIR SEGUNDO VIDEO DE CALIBRAGEM ############################

caminho_video2 = '/home/giovana/Área de trabalho/eyeNavigate/v3/calibragemEsquerda.mp4'

cap = cv2.VideoCapture(caminho_video2)

if not cap.isOpened():
    print("Erro ao abrir o vídeo!")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('Video', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



######################## faz a captura da coordeenadas (lado desquerdo)#############################

cam = cv2.VideoCapture(0)
counter = 0
with detector_face.FaceDetection(model_selection = 1, min_detection_confidence=1) as dec:   
    while cam.isOpened():
        counter += 1
        status, imagem = cam.read()
       
        if not status :
            print("Ignorando frames vazios da câmera.")
            continue

        imagem.flags.writeable = False
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        resultados = dec.process(imagem)
        frame_height, frame_width, c = imagem.shape

        imagem.flags.writeable = True
        imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)

        if resultados.detections:
            detection = resultados.detections[0]
            drawing.draw_detection(imagem, detection)
            face_react = np.multiply(
                    [
                        detection.location_data.relative_bounding_box.xmin,
                        detection.location_data.relative_bounding_box.ymin,
                        detection.location_data.relative_bounding_box.width,
                        detection.location_data.relative_bounding_box.height,
                    ],
                    [frame_width, frame_height, frame_width, frame_height],
                ).astype(int)

            fx, fy, _, _ = face_react

            track_points.appendleft([fx, fy])
            if (counter <= 10):
             for i in range(1, len(track_points)):
                if counter >= 10 and i == 1 and track_points[-10] is not None:
                    dX = track_points[-10][0] - track_points[i][0]
                    dY = track_points[-10][1] - track_points[i][1]
                    direction_x, direction_y = "", ""
                    coordenadasEsquerda = face_react
                    print (coordenadasEsquerda)
            else: break

            
                            
cam.release() 
cv2.destroyAllWindows()    




#######################################################AGORA BOTA O SCROLL#################################################################

pyautogui.alert("Pronto para começar!")
cam = cv2.VideoCapture(0)
counter = 0


with detector_face.FaceDetection(model_selection = 1, min_detection_confidence=1) as dec:   
    while cam.isOpened():
        counter += 1
        status, imagem = cam.read()
       
        if not status :
            print("Ignorando frames vazios da câmera.")
            continue

        imagem.flags.writeable = False
        imagem = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        resultados = dec.process(imagem)
        frame_height, frame_width, c = imagem.shape

        imagem.flags.writeable = True
        imagem = cv2.cvtColor(imagem, cv2.COLOR_RGB2BGR)

        if resultados.detections:
            for face in resultados.detections:
                drawing.draw_detection(imagem, face)
                face_react = np.multiply(
                    [
                        face.location_data.relative_bounding_box.xmin,
                        face.location_data.relative_bounding_box.ymin,
                        face.location_data.relative_bounding_box.width,
                        face.location_data.relative_bounding_box.height,
                    ],
                    [frame_width, frame_height, frame_width, frame_height],
                ).astype(int)

                fx, fy, _, _ = face_react

                track_points.appendleft([fx, fy])

                for i in range(1, len(track_points)):
                    if counter >= 10 and i == 1 and track_points[-10] is not None:
                        dX = track_points[-10][0] - track_points[i][0]
                        dY = track_points[-10][1] - track_points[i][1]
                        direction_x, direction_y = "", ""
                coordenadasAtuais = face_react
                print (coordenadasAtuais)

                

                if np.allclose(coordenadasAtuais, coordenadasDireita, atol=20):
                   direction_x = "Direita"
                elif np.allclose(coordenadasAtuais, coordenadasEsquerda, atol=20):
                   direction_x = "Esquerda"
                            
                            
                if direction_x == "Direita" :
                         mouse.scroll(0,-1) #scroll para baixo

                if direction_x == "Esquerda":
                         mouse.scroll(0,1) #scroll para cima

        cv2.imshow('Reconhecimento de movimento', imagem)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
                           
      
cam.release() 
cv2.destroyAllWindows()   