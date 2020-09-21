from cryptography.fernet import Fernet

KEY = b'7H0RviHlSUDJ8ug1xf0lm5ZO_JZjWketfjcZ9gzaYZU='

f = Fernet(KEY)

with open('systeminfo.larry', 'rb') as infile:
    encrypted_text = infile.read()

plaintext = f.decrypt(encrypted_text)

with open('systeminfo.txt', 'wb') as outfile:
    outfile.write(plaintext)

