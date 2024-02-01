import threading
import socket
import re
from base64 import b64decode

host = "challenge01.root-me.org"
port = 52023

def receive(client):
        response = client.recv(4096)
        print(response)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))
response = client.recv(4096).decode()
clear_content = re.search(r"'(.*?)'", response).group(1)
result = b64decode(clear_content).decode('utf-8')
threading.Thread(target=receive, args=(client,)).start()
client.send((str(result) + "\n").encode())
