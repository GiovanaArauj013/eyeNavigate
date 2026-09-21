import cv2
import torch



modelo = torch.hub.load('ultralytics/yolov5', 'yolov5s')




webcam = cv2.VideoCapture(0)  # 0 para a câmera padrão


while True:
    ret, frame = webcam.read()
    if not ret:
        break


    results = modelo(frame)


    for det in results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = det
        if cls == 0:  # Classe 0 é 'person' no modelo YOLOv5
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)


    cv2.imshow('Deteccao de face', frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


webcam.release()
cv2.destroyAllWindows()
