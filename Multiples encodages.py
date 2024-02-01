import threading
import socket
import re
import codecs

host = "challenge01.root-me.org"
port = 52017

def receive(client):
        response = client.recv(4096)
        print(response)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))
response = client.recv(4096).decode()
print(response)
# clear_content = re.search(r"'(.*?)'", response).group(1)
# result = codecs.decode(clear_content, 'rot_13')
# threading.Thread(target=receive, args=(client,)).start()
# client.send((str(result) + "\n").encode())