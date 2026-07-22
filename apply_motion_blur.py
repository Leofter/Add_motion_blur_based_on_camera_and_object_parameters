import cv2
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()
CAMINHO_IMAGEM = os.getenv("IMAGE_PATH")
FPS = 90.0
RESOLUCAO_LARGURA = 4092
LARGURA_SENSOR_MM = 1.0
DISTANCIA_FOCAL_MM = 50.0
ANGULO_OBTURADOR = 0.0
VELOCIDADE_KMH = 50.0
DISTANCIA_OBJETO_M = 1.0
ANGULO_MOVIMENTO_GRAUS = 0.0

img = cv2.imread(CAMINHO_IMAGEM)
h_img, w_img = img.shape[:2]

velocidade_ms = VELOCIDADE_KMH / 3.6
tempo_exposicao = (ANGULO_OBTURADOR / 360.0) / FPS
largura_fov_m = DISTANCIA_OBJETO_M * (LARGURA_SENSOR_MM / DISTANCIA_FOCAL_MM)
ppm = RESOLUCAO_LARGURA / largura_fov_m
tamanho_blur_px = max(3, int(velocidade_ms * tempo_exposicao * ppm) | 1)

kernel = np.zeros((tamanho_blur_px, tamanho_blur_px), dtype=np.float32)
centro = tamanho_blur_px // 2
for i in range(tamanho_blur_px):
    dist = abs(i - centro)
    kernel[centro, i] = max(0, 1.0 - (dist / (tamanho_blur_px / 2.0)) ** 2)
matriz_rotacao = cv2.getRotationMatrix2D((centro, centro), ANGULO_MOVIMENTO_GRAUS, 1.0)
kernel = cv2.warpAffine(kernel, matriz_rotacao, (tamanho_blur_px, tamanho_blur_px))
kernel /= np.sum(kernel)

roi_selecionada = cv2.selectROI("Selecione", img, fromCenter=False, showCrosshair=True)
cv2.destroyWindow("Selecione")

mascara_grabcut = np.zeros((h_img, w_img), np.uint8)
bgd_model = np.zeros((1, 65), np.float64)
fgd_model = np.zeros((1, 65), np.float64)
cv2.grabCut(
    img,
    mascara_grabcut,
    roi_selecionada,
    bgd_model,
    fgd_model,
    5,
    cv2.GC_INIT_WITH_RECT,
)
mascara = np.where((mascara_grabcut == 2) | (mascara_grabcut == 0), 0, 255).astype(
    "uint8"
)

mascara_dilatada = cv2.dilate(mascara, np.ones((5, 5), np.uint8), iterations=1)
fundo_limpo = cv2.inpaint(img, mascara_dilatada, 5, cv2.INPAINT_TELEA)

carro_isolado = cv2.bitwise_and(img, img, mask=mascara)
mascara_float = mascara.astype(np.float32) / 255.0

carro_blur = cv2.filter2D(carro_isolado.astype(np.float32), -1, kernel)
mascara_blur = cv2.filter2D(mascara_float, -1, kernel)
mascara_blur_3c = np.repeat(mascara_blur[:, :, np.newaxis], 3, axis=2)

resultado = carro_blur + (1.0 - mascara_blur_3c) * fundo_limpo.astype(np.float32)
img_final = np.clip(resultado, 0, 255).astype(np.uint8)

cv2.imshow("Motion Blur Real - Segmentacao", img_final)
cv2.waitKey(0)
cv2.destroyAllWindows()
