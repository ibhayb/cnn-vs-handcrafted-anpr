from paddleocr import PaddleOCR
import re

### INITIALIZE PADDLE OCR ###
def initialize_ocr():
    return PaddleOCR(lang="german", show_log=False)

### EXTRACT INFORMATION FROM OCR ###
def extract_ocr_information(result):
    for line in result:
        label = line[0]
        score = line[1]
        label = re.sub('[^A-Z0-9]', '', label)
    return score, label
