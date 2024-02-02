import requests
import base64
import re
from PIL import Image
import pytesseract
import io
import time
import unicodedata

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
while True:
    s = requests.Session()

    start = time.time()
    resp = s.get("http://challenge01.root-me.org/programmation/ch8/")
    b64 = re.search(r';base64,(.*?)\"', resp.text)
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(b64.group(1), "utf-8"))))
    img = img.convert("RGBA")
    pixdata = img.load()

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y] == (0, 0, 0, 255):
                pixdata[x, y] = (255, 255, 255, 255)

    width, height = img.size
    new_size = width*8, height*8
    img = img.resize(new_size, Image.LANCZOS)
    img = img.convert('L')
    img = img.point(lambda x: 0 if x < 155 else 255, '1')
    img.save('captcha.png')
    text = pytesseract.image_to_string(img)
    end = time.time()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
    print(text)
    print(f"took : {end - start}")
    resp = s.post("http://challenge01.root-me.org/programmation/ch8/", data={"cametu": text.decode('utf-8').rstrip()})
    print(resp.text)