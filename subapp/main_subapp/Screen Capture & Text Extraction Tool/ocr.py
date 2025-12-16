import cv2
import numpy as np
import pytesseract
import os
import time


SAVE_DIR = "screenshots"
os.makedirs(SAVE_DIR, exist_ok=True)

def preprocess_image(pil_image):
    img = np.array(pil_image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]
    return thresh


def extract_text(processed_image):
    return pytesseract.image_to_string(processed_image)


def save_image(image):
    filename = f"screenshot_{int(time.time())}.png"
    path = os.path.join(SAVE_DIR, filename)
    image.save(path)
    return path