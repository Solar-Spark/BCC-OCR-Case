from paddleocr import PaddleOCR
import cv2
from skimage import img_as_ubyte
import numpy as np

ocr = PaddleOCR(lang='ru')

def ocr_image(image):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    if image.dtype != np.uint8:
        image = img_as_ubyte(image)

    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    results = ocr.ocr(image)
    texts = results[0]['rec_texts']
    return " ".join(texts)

def ocr_images(image_arr):
    texts = []
    for image in image_arr:
        texts.append(ocr_image(image))
    return " ".join(texts)