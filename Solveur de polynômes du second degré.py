import socket
import re
import math
host = "challenge01.root-me.org"
port = 52018

def solve(content):
    try:

        values = re.search(r'Solve this equation please: (-?\d+).x² (.*?) (-?\d+).x¹ (.*?) (-?\d+) = (-?\d+)', content)
        a = int(values.group(1))
        _b = values.group(2)
        b = int(values.group(3))
        _c = values.group(4)
        c =int(values.group(5))
        res = int(values.group(6))
        if _b == "-": b=b*-1
        if _c == "-": c=c*-1

        c = c+(res*-1)

        delta = b ** 2 - 4 * a * c

        if delta > 0:
            x1 = (-b + (delta ** 0.5)) / (2 * a)
            x2 = (-b - (delta ** 0.5)) / (2 * a)
            return "x1: " + str(round(x1, 3)) + " ; x2: " + str(round(x2, 3))
        elif delta == 0:
            x = -b / (2 * a)
            return "x: " + str(round(x, 3)),
        else:
            return "Not possible"

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
