import requests
from bs4 import BeautifulSoup
import base64
from PIL import Image
import io
import qrtools

s = requests.Session()
resp = s.get("http://challenge01.root-me.org/programmation/ch7/")
soup = BeautifulSoup(resp.content, "html.parser")
img = soup.find("img")
b64 = img["src"].split(",")[-1]
img = Image.open(io.BytesIO(base64.decodebytes(bytes(b64, "utf-8"))))
img.save(r'qrcode.jpeg')
qr = qrtools.QR()
text = qr.decode(filename="qrcode.jpeg")
print(text)
resp = s.post("http://challenge01.root-me.org/programmation/ch7/", data={"metup": text.decode()})
print(resp.text)