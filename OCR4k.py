import pytesseract
import cv2
import numpy as np
import pyautogui
from time import sleep
import os
from datetime import datetime

# Define o caminho do executável do Tesseract (caso não esteja no PATH)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Ajuste conforme a localização do Tesseract


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

def upscale_image(image, scale_factor=4):
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
        upscaled_frame = upscale_image(frame, scale_factor=4)  # Aumento de 2x
        
        # Aplica o filtro de nitidez na imagem aumentada
        sharpened_frame = apply_sharpening_filter(upscaled_frame)
        
        # Salva a imagem filtrada e aumentada na pasta 'prints'
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S%f')  # Timestamp para nome único
        cv2.imwrite(f'prints/upscaled_sharpened_screenshot_{timestamp}.png', sharpened_frame)  # Salva a imagem
        
        # Realiza OCR usando Tesseract
        text = pytesseract.image_to_string(sharpened_frame)
        
        # Exibe o texto extraído no log (console)
        print("T1BRPadrao:", text)
        
        # Salva o texto extraído no arquivo .txt
        with open(output_file, "a", encoding="utf-8") as file:
            file.write(text + "\n")
        
        # Pausa por aproximadamente 1/60 de segundo (aproximadamente 16.7ms)

# Ajuste da região conforme solicitado
region = (0, 0, 3000, 30)  # x=0, y=20, largura=870, altura=100

# Defina o nome do arquivo .txt de saída
output_file = "T3BRPadrao.txt"

# Executa a captura e OCR em tempo real
capture_and_ocr(region, output_file)
