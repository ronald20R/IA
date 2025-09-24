import cv2
import numpy as np
import pygame
import threading

fuego_reportado = 0
estado_alarma = False

def reproducir_audio():
    pygame.mixer.init()
    pygame.mixer.music.load("alarma.mp3")
    pygame.mixer.music.play(-1)

def pausa_audio():
    pygame.mixer.music.stop()

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    if not ret:
        break
    frame = cv2.resize(frame, (1000, 600))
    brillo = 10
    contraste = 10

    frame = cv2.convertScaleAbs(frame, alpha=contraste, beta=brillo)

    blur = cv2.GaussianBlur(frame, (15, 15), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 100, 80])
    upper_red = np.array([10, 256, 256])

    lower = np.array(lower_red, dtype='uint8')
    upper = np.array(upper_red, dtype='uint8')
    mask = cv2.inRange(hsv, lower_red, upper_red)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    fuego_detectado = False

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 200:
            fuego_detectado = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "Fuego detectado", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow("Fuego detectado", frame)
    if fuego_detectado:
        fuego_reportado += 1
    else:
        fuego_reportado = 0
    if fuego_reportado >= 1:
        if not estado_alarma:
            threading.Thread(target=reproducir_audio).start()
            estado_alarma = True
    if fuego_reportado  == 0 and estado_alarma:
        pausa_audio()
        estado_alarma = False

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
video.release()


