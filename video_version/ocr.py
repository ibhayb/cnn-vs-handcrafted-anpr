from PIL import Image
import pytesseract
import cv2 as cv

# process
def process_ocr(plate):
    plate = cv.cvtColor(plate, cv.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(plate, config='--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    return text
