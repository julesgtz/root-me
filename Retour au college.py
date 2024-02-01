from math import sqrt
import threading
import socket
import re

host = "challenge01.root-me.org"
port = 52002

def receive(client):
        response = client.recv(4096)
        print(response)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))
response = client.recv(4096)

threading.Thread(target=receive, args=(client,)).start()

last_sentance = str(response).split(r"\n")[-1]
nb, nb2 = re.findall(r'\b\d+\b', last_sentance)
print(last_sentance)
result = round(sqrt(int(nb))*int(nb2), 2)
client.send((str(result) + "\n").encode())
