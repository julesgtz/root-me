import threading
import socket
import re
import base64


host = "challenge01.root-me.org"
port = 52017
MORSE= {"A" : ".-","B" : "-...","C" : "-.-.","D" : "-..","E" : ".","F" : "..-.","G" : "--.","H" : "....","I" : "..","J" : ".---","K" : "-.-","L" : ".-..","M" : "--","N" : "-.","O" : "---","P" : ".--.","Q" : "--.-","R" : ".-.","S" : "...","T" : "-","U" : "..-","V" : "...-","W" : ".--","X" : "-..-","Y" : "-.--","Z" : "--.."}
MORSE_INV = {value:key for key,value in MORSE.items()}
def morse_decode(content):
        lst = content.split("/")
        result = []
        for item in lst:
                result.append(MORSE_INV.get(item))
        return "".join(result)

def solve(content):
        if "flag" in content:
                return False
        clear_content = re.search(r"'(.*?)'", content).group(1)
        print(f"Decode {clear_content}")
        try:
                resp = base64.b85decode(clear_content).decode()
                print(f"b85 {resp}")
                return resp
        except:
                pass
        try:
                resp = base64.b64decode(clear_content).decode()
                print(f"b64 {resp}")
                return resp
        except:
                pass

        try:
                resp = base64.b32decode(clear_content).decode()
                print(f"b32 {resp}")
                return resp
        except:
                pass

        try:
                resp = base64.b16decode(clear_content).decode()
                print(f"b16 {resp}")
                return resp
        except:
                pass

        try:
                resp = base64.b32hexdecode(clear_content).decode()
                print(f"b32hex {resp}")
                return resp
        except:
                pass

        try:
                resp = bytes.fromhex(clear_content).decode('utf-8')
                print(f"hex {resp}")
                return resp
        except:
                pass

        try:
                resp = morse_decode(clear_content).lower()
                print(f"morse {resp}")
                return resp
        except:
                pass

        print(f"Failed to decode : {clear_content}")

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
# clear_content = re.search(r"'(.*?)'", response).group(1)
# result = codecs.decode(clear_content, 'rot_13')
threading.Thread(target=receive, args=(client,)).start()
# client.send((str(result) + "\n").encode())