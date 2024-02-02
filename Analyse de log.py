import requests
from urllib.parse import unquote
import base64 as b64


r = requests.get("http://challenge01.root-me.org/forensic/ch13/ch13.txt")
with open("text.txt", "w") as f:
    f.write(r.text)
with open("text.txt", "r") as f:
    logs = f.read().split("\n")[:-1]

# delta = []
# for i in range(1,len(logs)):
#     _time = logs[i-1][36:38]
#     time = logs[i][36:38]
#     if _time.startswith("0"):_time = "6" + _time[1]
#     if time.startswith("0"):time = "6" + time[1]
#     print(_time, time, int(time)-int(_time))
#     delta.append(
#         int(time)-int(_time)
#     )
import datetime
delta = []
for i in range(1,len(logs)):
    _time = logs[i-1][30:38]
    time = logs[i][30:38]
    datetime.datetime.()
    delta.append(
        int(time)-int(_time)
    )
idx=0
for log in logs:
    time = log[36:38]
    param = log[80:-25]
    t64 = unquote(param)
    d = b64.b64decode(t64).decode()
    print(time, delta[idx], d)
    idx+=1


