import hashlib
from threading import Thread, Lock
from time import sleep, time
from itertools import tee


# Credit https://github.com/applied-risk/snmpv3brute
# 80% du code a été trouvé sur github, juste ajouter des threads
# 38 secondes pour trouver le mot de passe / 2k8 mdp par seconde

GREEN = "\033[92m"
YELLOW = "\033[33m"
RED = "\033[91m"
WHITE = "\033[97m"

NB_THREAD = 15 # 100 = 45s, 50 = 46s, 25 = 40s, 15 = 46s


class Solution:
    msg = "3081800201033011020420dd06a7020300ffe30401050201030431302f041180001f8880e9bd0c1d12667a5100000000020105020120040475736572040cb92621f4a93d1bf9738cd5bd04003035041180001f8880e9bd0c1d12667a51000000000400a11e02046b4c5ac20201000201003010300e060a2b06010201041e0105010500"
    target = "b92621f4a93d1bf9738cd5bd"
    msg_2 = bytes.fromhex(msg.replace(target, "000000000000000000000000"))
    engineid = bytes.fromhex("80001f8880e9bd0c1d12667a5100000000")

    def __init__(self):
        self.lock = Lock()
        self.passwords, temp_passwords = tee(self.get_pwd())
        self.total_passwords = sum(1 for _ in temp_passwords)
        self.thread = []
        self.pwd = None
        self.passwords_processed = 0
        self.progress_lock = Lock()
        self.progress = Thread(target=self.print_progress)
        self.last_per = -1

    def calculate_md5(self, i):
        print(f"{GREEN}[+]{WHITE} Thread {i} started")
        password = True
        while password:
            password = None

            with self.lock:
                try:
                    if self.passwords:
                        password = next(self.passwords)
                        self.passwords_processed += 1
                except StopIteration:
                    print("error stop")
                    pass
                except Exception as e:
                    print(e)
            if password:
                if not len(password) == 0:
                    try:
                        password_buf = (password * (1048576 // len(password) + 1))[:1048576].encode('utf-8')
                        h = hashlib.md5()
                        h.update(password_buf)
                        key = h.digest()
                        strpass = key + self.engineid + key
                        h = hashlib.md5()
                        h.update(strpass)
                        extended_key = h.hexdigest() + '00' * 48

                        # Correctly generating K1 and K2
                        ipad = bytes.fromhex('36' * 64)
                        opad = bytes.fromhex('5c' * 64)
                        k1 = bytes.fromhex('%032x' % (int(extended_key, 16) ^ int(ipad.hex(), 16)))
                        k2 = bytes.fromhex('%032x' % (int(extended_key, 16) ^ int(opad.hex(), 16)))

                        # Update HMAC computation
                        h = hashlib.md5()
                        h.update(k1 + self.msg_2)
                        first_pass = h.digest()
                        h = hashlib.md5()
                        h.update(k2 + first_pass)
                        final_hash = h.hexdigest()
                        if final_hash[:24] == self.target:
                            print(f"{GREEN}[+]{WHITE} Password found : {password}")
                            self.pwd = True
                            with self.lock:
                                self.passwords = None

                    except ValueError:
                        pass

    def print_progress(self):
        running = True
        while running:
            running = None
            with self.lock:
                if self.passwords:
                    running = True
                    progress = (self.passwords_processed / self.total_passwords) * 100
                    if progress // 2 > self.last_per:
                        print(f"{YELLOW}[!]{WHITE} Progress: {progress:.2f}%")
                        self.last_per = progress // 2

    def run(self):
        start = time()
        self.thread.append(self.progress)
        for _ in range(NB_THREAD):
            self.thread.append(Thread(target=self.calculate_md5, args=(_,)))
        for thread in self.thread:
            thread.start()
            # sleep(0.1)
        for thread in self.thread:
            thread.join()
        if not self.pwd:
            print(f"{RED}[-]{WHITE} No password found !")
        print(f"{GREEN}[+]{WHITE} All tasks finished")
        print(f"{YELLOW}[!]{WHITE} Was running for : {time()-start:.2f}s")

    def get_pwd(self):
        with open("dict.txt", 'r', encoding='utf-8', errors='replace') as f:
            for ligne in f:
                yield ligne.strip()


if __name__ == "__main__":
    Solution().run()
