import cv2
import numpy as np
from skimage.restoration import denoise_nl_means, estimate_sigma
from skimage import img_as_ubyte
import fitz
from PIL import Image

def preprocess_image(image):
    if image is None:
        print("Error: unable to load image")
        return None
    img_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    gray_image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    
    sigma_est = np.mean(estimate_sigma(gray_image, channel_axis=None))
    denoised_image = denoise_nl_means(
        gray_image,
        h=0.5 * sigma_est,
        fast_mode=True,
        patch_size=6,
        patch_distance=5,
        channel_axis=None
    )
    denoised_image = img_as_ubyte(denoised_image)
    return denoised_image

def convert_pdf_to_images(path):
    pdf = fitz.open(path)
    pages = []
    for page in pdf:
        pix = page.get_pixmap(dpi=130)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pages.append(img)
    return pages

def preprocess_document(path):
    pages = convert_pdf_to_images(path)
    images = []
    for page in pages:
        preprocessed = preprocess_image(page)
        images.append(preprocessed)
    return images