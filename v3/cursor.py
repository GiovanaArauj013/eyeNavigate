import cv2
import mediapipe as mp
import numpy as np
import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0
janela_largura, janela_altura = pyautogui.size()

mp_face_mesh = mp.solutions.face_mesh
camera = cv2.VideoCapture(0)

face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


######################################ENQUADRAMENTO########################################################

pyautogui.alert("O código irá começar, se posicione no enquadramneto da câmera, quando satifeito, presione Q")

if not camera.isOpened():
    pyautogui.alert("Erro ao abrir a câmera!")
    exit()


while True:
    

    ret, frame = camera.read()
    frame = cv2.resize(frame, (janela_largura, janela_altura))
    cv2.imshow('Camera', frame)
    if not ret:
        print("Falha ao capturar o quadro!")
        break


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


camera.release()
cv2.destroyAllWindows()


###################### ABRIR VIDEO DE CALIBRAGEM ############################


cap = cv2.VideoCapture("/home/giovana/Área de trabalho/eyeNavigate/v3/calibragemOlhos.mp4")

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

##################### DEFINE LOCALIZAÇÃO DOS PONTOS NA TELA##################################

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    pyautogui.alert("Erro ao reabrir a câmera")
    exit()

win_name = "Calibragem"
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)


pontos_janela = [
    (int(janela_largura * 0.1), int(janela_altura * 0.1)),
    (int(janela_largura * 0.5), int(janela_altura * 0.1)),
    (int(janela_largura * 0.9), int(janela_altura * 0.1)),
    (int(janela_largura * 0.1), int(janela_altura * 0.5)),
    (int(janela_largura * 0.5), int(janela_altura * 0.5)),
    (int(janela_largura * 0.9), int(janela_altura * 0.5)),
    (int(janela_largura * 0.1), int(janela_altura * 0.9)),
    (int(janela_largura * 0.5), int(janela_altura * 0.9)),
    (int(janela_largura * 0.9), int(janela_altura * 0.9)),
]


####################### PARA LOCALIZAR IRIS ######################
indices_iris_direita = [473, 474, 475, 476, 477]
indices_iris_esquerda = [468, 469, 470, 471, 472]

calibragem = [] 


def obter_iris(face_landmarks):
    x_iris_d = sum(face_landmarks.landmark[ind].x for ind in indices_iris_direita) / len(indices_iris_direita)
    y_iris_d = sum(face_landmarks.landmark[ind].y for ind in indices_iris_direita) / len(indices_iris_direita)

    x_iris_e = sum(face_landmarks.landmark[ind].x for ind in indices_iris_esquerda) / len(indices_iris_esquerda)
    y_iris_e = sum(face_landmarks.landmark[ind].y for ind in indices_iris_esquerda) / len(indices_iris_esquerda)

    x_draw_d = int(x_iris_d * janela_largura)
    y_draw_d = int(y_iris_d * janela_altura)

    x_draw_e = int(x_iris_e * janela_largura)
    y_draw_e = int(y_iris_e * janela_altura)

    iris_media = (
        (x_draw_d + x_draw_e) // 2,
        (y_draw_d + y_draw_e) // 2
    )

    return (x_draw_d, y_draw_d), (x_draw_e, y_draw_e), iris_media


############################### PARA REGISTRAR AS COORDENADAS OBTIDAS NA CALIBRAGEM ##################################3333
def capturar_ponto(indice_ponto, ponto_tela):
    while True:
        sucesso, imagem = camera.read()
        if not sucesso:
            return None

        imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        resultados = face_mesh.process(imagem_rgb)

        imagem_calibracao = np.zeros((janela_altura, janela_largura, 3), dtype=np.uint8)

        cv2.circle(imagem_calibracao, ponto_tela, 12, (0, 0, 255), -1)
        cv2.putText(
            imagem_calibracao,
            f"Olhe para o ponto {indice_ponto + 1} e aperte ESPACO",
            (40, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        iris_d = None
        iris_e = None
        iris_m = None

        if resultados.multi_face_landmarks:
            face_landmarks = resultados.multi_face_landmarks[0]
            iris_d, iris_e, iris_m = obter_iris(face_landmarks)

        cv2.imshow(win_name, imagem_calibracao)
        cv2.setWindowProperty(win_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        tecla = cv2.waitKey(1) & 0xFF

        if tecla == ord('q'):
            return None

        if tecla == ord(' ') and iris_d is not None and iris_e is not None:
            print(f"Ponto {indice_ponto + 1} capturado.")
            return {
                "ponto_tela": ponto_tela,
                "iris_direita": iris_d,
                "iris_esquerda": iris_e,
                "iris_media": iris_m
            }


############################### EXECUTA CALIBRAGEM ######################################

for i, ponto in enumerate(pontos_janela):
    registro = capturar_ponto(i, ponto)

    if registro is None:
        print("Calibragem cancelada.")
        camera.release()
        cv2.destroyAllWindows()
        raise SystemExit

    calibragem.append(registro)

cv2.destroyAllWindows()
print("Calibração finalizada.")

for i, item in enumerate(calibragem, start=1):
    print(f"Ponto {i}: tela={item['ponto_tela']} iris_media={item['iris_media']}")


   ####################### EXTRAINDO LIMITES DA CALIBRAGEM (Para calcular o movimento do mousemais fluido) ########33
iris_x_calibrados = [item["iris_media"][0] for item in calibragem]
iris_y_calibrados = [item["iris_media"][1] for item in calibragem]

min_iris_x = min(iris_x_calibrados)
max_iris_x = max(iris_x_calibrados)
min_iris_y = min(iris_y_calibrados)
max_iris_y = max(iris_y_calibrados)

# margem para evitar cursor preso nas bordas
margem_x = 30
margem_y = 30

# posição inicial do cursor
cursor_x, cursor_y = pyautogui.position()


cv2.namedWindow("Rastreio", cv2.WINDOW_NORMAL)

while True:
    sucesso, imagem = camera.read()
    if not sucesso:
        break

    imagem = cv2.resize(imagem, (janela_largura, janela_altura))
    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    resultados = face_mesh.process(imagem_rgb)

    if resultados.multi_face_landmarks:
        face_landmarks = resultados.multi_face_landmarks[0]
        iris_d, iris_e, iris_atual = obter_iris(face_landmarks)

        cv2.circle(imagem, iris_d, 5, (0, 255, 0), -1)
        cv2.circle(imagem, iris_e, 5, (0, 255, 0), -1)
        cv2.circle(imagem, iris_atual, 5, (255, 0, 0), -1)

   ########## MAPEIA O OLHAR #########
        novo_x = np.interp(
            iris_atual[0],
            [min_iris_x, max_iris_x],
            [ janela_largura - margem_x, margem_x]
        )

        novo_y = np.interp(
            iris_atual[1],
            [min_iris_y, max_iris_y],
            [margem_y, janela_altura - margem_y]
        )
 
        cursor_x = cursor_x + (novo_x - cursor_x) * 0.25 #<- 0.25 para suavizar o movimento
        cursor_y = cursor_y + (novo_y - cursor_y) * 0.25

        pyautogui.moveTo(int(cursor_x), int(cursor_y))

        cv2.putText(
            imagem,
            f"Cursor: ({int(cursor_x)}, {int(cursor_y)})",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

    cv2.imshow("Rastreio", imagem)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()