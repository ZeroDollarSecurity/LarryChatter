from datetime import datetime, timezone
import hashlib
import random


def generatehandle():
    # Returns a LARRYCHATTER Command Post handle to check every 24 hours
    NAME = "larry"
    SECRET_SEED = '123456'
    date = datetime.now(timezone.utc).strftime("%d%m%Y")
    #date = str(29122019)
    append = date + SECRET_SEED
    hashed_append = hashlib.sha384(append.encode()).hexdigest()
    code = hashed_append[5:11]
    handle = code[:3] + NAME + code[3:]
    return handle
            

def predictHandle(date):
    # Takes a date string as argument("DDMMYY") and predicts the Twitter handle to register as LARRYCHATTER CP and returns it
    NAME = "larry"
    SECRET_SEED = '123456'
    append = date + SECRET_SEED
    hashed_append = hashlib.sha384(append.encode()).hexdigest()
    code = hashed_append[5:11]
    handle = code[:3] + NAME + code[3:]
    return handle


def regHandle():
    # Takes user input date("DDMMYYYY") and predicts and prints a Twitter handle to register as LARRYCHATTER CP for the day
    datetoday = datetime.now(timezone.utc).strftime("%d%m%Y")
    print("Today's Date is: " + datetoday)
    handletoday = predictHandle(datetoday)
    print("Today's LARRYCHATTER Command Post Handle is: " + handletoday)
    print("\n")
    date = input("Enter the date for which you want to predict the LARRYCHATTER Command Post Handle: ")
    handleatdate = predictHandle(date)
    print("LARRYCHATTER Command Post Handle at " + date + " is: " + handleatdate)

#regHandle()
#generatehandle()

