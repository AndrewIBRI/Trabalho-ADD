import cv2
import numpy as np
import pyautogui
import easyocr
from time import sleep
import os
from datetime import datetime

# Inicializa o EasyOCR com suporte a GPU
reader = easyocr.Reader(['en'], gpu=True, verbose=False)

# Cria a pasta 'prints' se não existir
if not os.path.exists('prints'):
    os.makedirs('prints')

def apply_sharpening_filter(image):
    # Kernel de nitidez com mais intensidade
    kernel = np.array([[0, -0.5, 0],
                       [-0.5, 3, -0.5],
                       [0, -0.5, 0]])  # Aumento na intensidade da nitidez
    
    # Aplica o filtro de nitidez usando filter2D
    sharpened_image = cv2.filter2D(image, -1, kernel)
    
    return sharpened_image

def upscale_image(image, scale_factor=2):
    """
    Aumenta a resolução da imagem.
    """
    width = int(image.shape[1] * scale_factor)
    height = int(image.shape[0] * scale_factor)
    
    # Redimensiona a imagem
    upscaled_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_CUBIC)
    
    return upscaled_image

def capture_and_ocr(region, output_file):
    while True:
        # Captura a região da tela
        screenshot = pyautogui.screenshot(region=region)
        
        # Converte para um array do OpenCV
        frame = np.array(screenshot)
        
        # Aplica o upscaling para aumentar a resolução da imagem
        upscaled_frame = upscale_image(frame, scale_factor=2)  # Aumento de 2x
        
        # Aplica o filtro de nitidez na imagem aumentada
        sharpened_frame = apply_sharpening_filter(upscaled_frame)
        
        # Realiza OCR com EasyOCR
        text = reader.readtext(sharpened_frame, detail=0)
        
        # Exibe o texto extraído no log (console)
        print("T1BRPadrao:", " ".join(text))
        
        # Salva o texto extraído no arquivo .txt
        with open(output_file, "a", encoding="utf-8") as file:
            file.write(" ".join(text) + "\n")
        
        # Pausa por aproximadamente 1/60 de segundo (aproximadamente 16.7ms)
        sleep(1)

# Ajuste da região conforme solicitado
region = (0, 0, 3000, 30)  # x=0, y=20, largura=870, altura=100

# Defina o nome do arquivo .txt de saída
output_file = "texto_extraido.txt"

# Executa a captura e OCR em tempo real
capture_and_ocr(region, output_file)
