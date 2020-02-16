#Packages needed
from PIL import Image
import cv2
import numpy as np 
import pyocr
import pyocr.builders

#Tesseract is wrapped in pyOCR. You access it with the method tools
tools = pyocr.get_available_tools()
print("The tools are of #:" ,len(tools))
tool = tools[0]
print("The name of the tool is",tool.get_name())

#Read and show images.
img = cv2.imread("test.png")
cv2.imshow("window",img)
cv2.waitKey()

#OCR in action
txt = tool.image_to_string(
    Image.open("test.png"),
    builder=pyocr.builders.TextBuilder()
    )
print(txt)