#!/usr/bin/env python3
import numpy as np
import cv2
import pyocr
import pyocr.builders
from PIL import Image
import re
from firebase import firebase
import os
import statistics

# Initialize path of the working directory and temporary file
path = os.getcwd()+r"/data.txt"

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
f = open(path, "w")
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    txt = tool.image_to_string(Image.fromarray(
        frame), builder=pyocr.builders.TextBuilder())

    RegID = extract_reg_number(txt)
    Name = extract_names(txt)

    # Writing the on file; Empty files should not be written
    if Name != "":
        if RegID != "":
            f.write(Name)
            f.write(",")
            f.write(RegID)
            f.write("\n")

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        f.flush()
        f.close()
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

if os.path.getsize(path) > 0:
    with open(path, 'r') as file:
        data = file.read()

    nameList = []           # nameList contains a list of extracted names
    regNoList = []          # negNoList contains a list of extracted registration number

    # Split the string into Names and Registration numbers
    string = re.split('\n|,', data)
    # Separate Registration numbers and other redundant data(if any) from list
    for i in string:
        m = re.search(r'\d+$', i)
        if(m is not None):
            regNoList.append(i)
        else:
            nameList.append(i)

    # print(nameList)
    # print("*"*130)
    # print("*"*130)
    # print(regNoList)

    # Get the frequency of elements and the elements as lists (in ascending order)
    regfreq = np.unique(regNoList, return_counts=True)[1].tolist()
    regval = np.unique(regNoList, return_counts=True)[0].tolist()
    # print(regfreq)
    # print(regval)
    
    namefreq = np.unique(nameList, return_counts=True)[1].tolist()
    nameval = np.unique(nameList, return_counts=True)[0].tolist()
    print(namefreq)
    print(nameval)

    # Get the index where the maximum value is located
    maxNameIndex = regfreq.index(max(regfreq))
    maxRegIndex = namefreq.index(max(namefreq))

    # Store Name and Reg Number
    ID = regval[maxNameIndex]
    Name = nameval[maxRegIndex]

    print(ID)
    print(Name)
    os.remove(path)

#Phone Number
cap = cv2.VideoCapture(0)
f = open(path, "w")
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    txt = tool.image_to_string(Image.fromarray(frame), builder=pyocr.builders.TextBuilder())
    
    PhoneNumber = extract_phoneNo(txt)
    if PhoneNumber != "":
        f.write(PhoneNumber)
        f.write("\n")

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        f.flush()
        f.close()
        break
cap.release()
cv2.destroyAllWindows()

regs =[]
if os.path.getsize(path) > 0:
    with open(path, 'r') as file:
        PhoneNumber = file.read()
        with open(path) as f:
            lines = [line.rstrip() for line in f]
        contactNumber = statistics.mode(lines)
# printing and post the filtered values
    Creds = {"Registration Number": ID, "Name": Name,"Contact Number":contactNumber}
    print("Name:", Name)
    print("Registration Number:", ID)
    print("Contact Number:", contactNumber)
    print("\nConfirm the details (y/n)")
    submit = input()
    if(submit == 'y'):
        results = firebase.post("/TestData/", Creds)
        print("Your details have been registered")
        os.remove(path)
    else:
        print("Try Again")
        os.remove(path)

else:
    print("No ID Card was detected. Please try again")

    # delete the file
    os.remove(path)