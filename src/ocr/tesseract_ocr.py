import pytesseract
import cv2
from PIL import Image


class TesseractOcr():
    def __init__(self):
        pass


    def read_text(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
        retval, binary_gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        # print(binary_gray)
        pil_img = Image.fromarray(binary_gray)
        text = pytesseract.image_to_string(pil_img, lang='eng', config='-psm 7')

        return text