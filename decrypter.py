from nacl.secret import SecretBox
from base64 import urlsafe_b64decode as decode

KEY = b'm_LAKLhu8ALI1-bufB1AfgR7kzxBrdHRaJ7KxvZm8dY='

box = SecretBox(deocode(key))

with open('systeminfo.larry', 'rb') as infile:
    encrypted_text = infile.read()

plaintext = box.decrypt(encrypted_text)

with open('systeminfo.txt', 'wb') as outfile:
    outfile.write(plaintext)
