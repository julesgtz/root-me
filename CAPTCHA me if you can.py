import requests
from bs4 import BeautifulSoup
from base64 import b64decode
import base64
import re
from PIL import Image
import pytesseract
import io

s = requests.Session()
resp = s.get("http://challenge01.root-me.org/programmation/ch8/")
soup = BeautifulSoup(resp.content, "html.parser")
img = soup.find("img")
b64 = img["src"].split(",")[-1]
img = Image.open(io.BytesIO(base64.decodebytes(bytes(b64, "utf-8"))))
img.save(r'captcha.jpeg')
text = pytesseract.image_to_string("captcha.jpeg", lang="fr")
# a continuer faut ajouter au PATH
resp = s.post("http://challenge01.root-me.org/programmation/ch8/", data={"cametu": text})
print(resp.text)