#!/usr/bin/env python3
import numpy as np
import cv2
import pyocr
import pyocr.builders
from PIL import Image
import re
from firebase import firebase


# Lists serve as the file
nameList = []           # nameList contains a list of extracted names
regNoList = []          # regNoList contains a list of extracted registration number
phoneNoList = []        # phoneNoList contains a list of exreacted contact details

# Firebase path
firebase = firebase.FirebaseApplication('https://vision-based-id-reader.firebaseio.com/', None)

# Regex for Registration Number
def extract_reg_number(string):
    pat3 = re.compile(r'[0-2][0-9][B|M][A-Z][A-Z][0-2][0-9][0-9][0-9]')
    re3 = pat3.findall(string)
    re3 = ''.join(re3)
    return re3

# Regex for Name
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
    ret, frame = cap.read()
    txt = tool.image_to_string(Image.fromarray(frame), builder=pyocr.builders.TextBuilder())

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

# Get the index where the maximum value is located
maxNameIndex = regfreq.index(max(regfreq))
maxRegIndex = namefreq.index(max(namefreq))
maxPhoneIndex = phonefreq.index(max(phonefreq))

# Store Name and Reg Number
ID = regval[maxNameIndex]
Name = nameval[maxRegIndex]
Contact = phoneval[maxPhoneIndex]

Creds = {"Registration Number": ID, "Name": Name,"Contact Number":Contact}
print("Name:", Name)
print("Registration Number:", ID)
print("Contact Number:", Contact)
print("\nConfirm the details (y/n)")

submit = input()
if(submit == 'y'):
    results = firebase.post("/TestData/", Creds)
    print("Your details have been registered")
else:
    print("Try Again")
