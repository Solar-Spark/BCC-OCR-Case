import paddle
from paddleocr import PaddleOCR
import cv2
from skimage import img_as_ubyte
import numpy as np

# Установим девайс на GPU
paddle.device.set_device("gpu")
print("Используем девайс:", paddle.device.get_device())

# Инициализация OCR для русского языка с включенной классификацией ориентации
ocr = PaddleOCR(lang='ru', use_angle_cls=True)

def ocr_image(image):
    # Преобразуем в BGR
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Обеспечим uint8
    if image.dtype != np.uint8:
        image = img_as_ubyte(image)

    # Если grayscale → сделаем RGB
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

    # Запуск OCR (теперь без cls=)
    results = ocr.ocr(image)
    texts = results[0]['rec_texts']

    return " ".join(texts)

def ocr_images(image_arr):
    texts = []
    for image in image_arr:
        texts.append(ocr_image(image))
    return " ".join(texts)