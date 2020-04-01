# Vision based ID Reader

The objective of the project is to read and store data from an ID Card using a camera using OCR. The OCR package used here is pyocr.

The front of the ID card of VIT University contains Registration Number and Name of the student which is what we aim to extract. 
The OCR dumps all kinds of data, which we clean by means of Regex and stored in a file named data.txt
We clean that data by the logic, 'Most occured entry is the right entry' and push that to firebase as a dictionary with Registration Number as Key and Name as value

## Packages and Dependencies
pip install -r requirements.txt on your virtual environment

## Procedure
1. Install dependencies on your virtual environment.
2. Show the front of your ID card to the camera for say 4-6 seconds 
3. Press 'q' to close the window
