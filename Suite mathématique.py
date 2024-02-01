import requests
import re

s = requests.Session()
resp = s.get("http://challenge01.root-me.org/programmation/ch1/")
pattern = re.search("U\<sub\>n\+1(.*)\<\/sub\>\<br", resp.text, flags=re.S)
calculs = pattern.group()
list1 = calculs.split(' ')

a = int(list1[3])
b = int(list1[11])
u0 = int((list1[15].split('\n')[0]))
n = int(list1[-1].split('>')[1].split('<')[0])

for i in range(n):
    u0 = (a + u0) + (i * b)

resp = s.get(f"http://challenge01.root-me.org/programmation/ch1/ep1_v.php?result={u0}")
print(resp.text)