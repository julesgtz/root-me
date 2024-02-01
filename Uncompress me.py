import socket
import re
import zlib
from base64 import b64decode

host = "challenge01.root-me.org"
port = 52022

def solve(content):
    try:
        clear_content = re.search(r"'(.*?)'", content).group(1)
        result = zlib.decompress(b64decode(clear_content)).decode('utf-8')
        return result
    except AttributeError:
        return False

def receive(client):
    result = True
    while result:
        response = client.recv(4096).decode()
        result = solve(response)
        if result:
            client.send((str(result) + "\n").encode())
        else:
            print(response)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host,port))
receive(client)
# threading.Thread(target=receive, args=(client,)).start()