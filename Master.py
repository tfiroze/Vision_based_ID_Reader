#!/usr/bin/env python3
import numpy as np
import cv2
import pyocr
import pyocr.builders
from PIL import Image
import re
from firebase import firebase
import datetime

# Lists serve as the file
nameList = []   
regNoList = []          
phoneNoList = []       

# Firebase path
firebase = firebase.FirebaseApplication('https://vision-based-id-reader.firebaseio.com/', None)

#Regex for Registration Number
def extract_reg_number(string):
    pat3 = re.compile(r'[0-2][0-9][B|M][A-Z][A-Z][0-2][0-9][0-9][0-9]')
    re3 = pat3.findall(string)
    re3 = ''.join(re3)
    return re3

#Regex for Name
def extract_names(string):
    pattern = re.compile(r'[A-Z][a-z]+')
    names = pattern.findall(string)
    newname = ' '.join(names)
    return newname

#Regex for Phone Number
def extract_phoneNo(string):
    pat2 = re.compile(r'[6-9][0-9]{9}')
    number = pat2.findall(string)
    number = ''.join(number)
    return number

# Activate Tesseract
tools = pyocr.get_available_tools()
tool = tools[0]

# Open Camera
cap = cv2.VideoCapture(0)
while(True):
    #Image Preprocessing
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, threshd = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) 
    
    #OCR in Action
    txt = tool.image_to_string(Image.fromarray(gray), builder=pyocr.builders.TextBuilder())

    RegID = extract_reg_number(txt)
    Name = extract_names(txt)
    PhoneNumber = extract_phoneNo(txt)

    if(RegID != ""):
        regNoList.append(RegID)

    if(Name != ""):
        nameList.append(Name)
    
    if(PhoneNumber != ""):
        phoneNoList.append(PhoneNumber)


    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


# Get the frequency of elements and the elements as lists (in ascending order)
regfreq = np.unique(regNoList, return_counts=True)[1].tolist()
regval = np.unique(regNoList, return_counts=True)[0].tolist()
    
namefreq = np.unique(nameList, return_counts=True)[1].tolist()
nameval = np.unique(nameList, return_counts=True)[0].tolist()

phonefreq = np.unique(phoneNoList, return_counts=True)[1].tolist()
phoneval = np.unique(phoneNoList, return_counts=True)[0].tolist()

#Failsafe
if regfreq == [] and namefreq == []:
    print("No ID Card Detected")
elif phonefreq ==[]:
    print("Back side of the ID Card wasn't read properly")

#Get the index where the maximum value is located
else:
    maxNameIndex = regfreq.index(max(regfreq))
    maxRegIndex = namefreq.index(max(namefreq))
    maxPhoneIndex = phonefreq.index(max(phonefreq))
    Time = datetime.datetime.now()

    # Store Name and Reg Number
    ID = regval[maxNameIndex]
    Name = nameval[maxRegIndex]
    Contact = phoneval[maxPhoneIndex]
    Time = Time.strftime("%H:%M:%S %d-%m-%Y")
    
    #Pushing to Firebase
    Creds = {"Time":Time,"Registration Number": ID, "Name": Name,"Contact Number":Contact}
    print("Name:", Name)
    print("Registration Number:", ID)
    print("Contact Number:", Contact)
    print("\nConfirm the details (y/n)")

    submit = input()
    if(submit == 'y'):
        results = firebase.post("/TestData/", Creds)
        print("Your details have been registered")
    else:
        print("Oops! Try Again")
