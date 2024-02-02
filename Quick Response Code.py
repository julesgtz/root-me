import requests
from bs4 import BeautifulSoup
import base64
from PIL import Image, ImageDraw
import io
import cv2
import re
import unicodedata

s = requests.Session()
resp = s.get("http://challenge01.root-me.org/programmation/ch7/")
soup = BeautifulSoup(resp.content, "html.parser")
img = soup.find("img")
b64 = img["src"].split(",")[-1]
img = Image.open(io.BytesIO(base64.decodebytes(bytes(b64, "utf-8"))))
draw = ImageDraw.Draw(img)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
W = 9
for (x, y) in [(18, 18), (18, 218), (218, 18)]:
    draw.rectangle((x, y, x + 7 * W, y + 7 * W), BLACK, BLACK)
    draw.rectangle((x + W, y + W, x + 6 * W, y + 6 * W), WHITE, WHITE)
    draw.rectangle((x + 2 * W, y + 2 * W, x + 5 * W, y + 5 * W), BLACK, BLACK)
img.save('qrcode.png')
img = cv2.imread("qrcode.png")
detect = cv2.QRCodeDetector()
value, points, straight_qrcode = detect.detectAndDecode(img)
pattern = re.compile('The key is (/\w+)')
match = pattern.match(value)
value = match.group(1)
resp = s.post("http://challenge01.root-me.org/programmation/ch7/", data={"metu": value})
print(resp.text)