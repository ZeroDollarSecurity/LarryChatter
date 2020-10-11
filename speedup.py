from time import time
from os import urandom


from cryptography.fernet import Fernet
from nacl.secret import SecretBox
from nacl.utils import random as nacl_random


key1 = Fernet.generate_key()
f = Fernet(key1)

key2 = urandom(32)
box = SecretBox(key2)

# assuming the average size of a doc: ~4MB
data = urandom(1024 ** 2 * 4)
runs = 500


tt = t = 0
for i in range(runs):
    t = time()
    ct = box.encrypt(data, nacl_random(SecretBox.NONCE_SIZE))
    tt += time() - t
print(tt/runs)


tt = t = 0
for i in range(runs):
    t = time()
    pt = box.decrypt(ct)
    tt += time() - t
print(tt/runs)


tt = t = 0
for i in range(runs):
    t = time()
    ct = f.encrypt(data)
    tt += time() - t
print(tt/runs)


tt = t = 0
for i in range(runs):
    t = time()
    pt = f.decrypt(ct)
    tt += time() - t
print(tt/runs)
