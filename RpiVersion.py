#!/usr/bin/env python3
import numpy as np
import cv2
import pyocr
import pyocr.builders
from PIL import Image
import re
from firebase import firebase
import datetime
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23
GPIO.setup(24, GPIO.OUT)  #LED to GPIO24
print("[INFO]:GPIO Set")

# Lists serve as the file
nameList = []   
regNoList = []          
     
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

# Activate Tesseract
tools = pyocr.get_available_tools()
tool = tools[0]
print("[INFO]:Tesseract Set")

# Open Camera
cap = cv2.VideoCapture(0)
print("[INFO]:Camera On"]
try:
	while(True):
		button_state = GPIO.input(23)
		
		#Image Preprocessing
		ret, frame = cap.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
		
		#OCR in Action
		txt = tool.image_to_string(Image.fromarray(gray), builder=pyocr.builders.TextBuilder())
		
		RegID = extract_reg_number(txt)
		Name = extract_names(txt)
		
		if(RegID != ""):
			regNoList.append(RegID)
		
		if(Name != ""):
			nameList.append(Name)
			
		if button_state==False:	
			GPIO.output(24, 1)
			print('Button Pressed...')
			time.sleep(0.2)
			GPIO.output(24,0)
			break
		else:
			GPIO.output(24, 0)
except:
	GPIO.cleanup()	
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

# Get the frequency of elements and the elements as lists (in ascending order)
regfreq = np.unique(regNoList, return_counts=True)[1].tolist()
regval = np.unique(regNoList, return_counts=True)[0].tolist()
    
namefreq = np.unique(nameList, return_counts=True)[1].tolist()
nameval = np.unique(nameList, return_counts=True)[0].tolist()

#Failsafe
if regfreq == [] and namefreq == []:
    print("No ID Card Detected")

#Get the index where the maximum value is located
else:
    maxNameIndex = regfreq.index(max(regfreq))
    maxRegIndex = namefreq.index(max(namefreq))
    Time = datetime.datetime.now()

    # Store Name and Reg Number
    ID = regval[maxNameIndex]
    Name = nameval[maxRegIndex]
    Time = Time.strftime("%H:%M:%S %d-%m-%Y")
    
    #Pushing to Firebase
    Creds = {"Time":Time,"Registration Number": ID, "Name": Name}
    print("Name:", Name)
    print("Registration Number:", ID)
    print("\nConfirm the details (y/n)")

    submit = input()
    if(submit == 'y'):
        results = firebase.post("/TestData/", Creds)
        print("Your details have been registered")
    else:
        print("Oops! Try Again")
