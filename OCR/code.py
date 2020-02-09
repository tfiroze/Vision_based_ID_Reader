import numpy as np
import cv2
import pyocr
import pyocr.builders
from PIL import Image

tools = pyocr.get_available_tools()
tool = tools[0]

cap = cv2.VideoCapture(0)
file = open("data.txt", "w")
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Our operations on the frame come here
    txt = tool.image_to_string(
        Image.fromarray(frame),
        builder=pyocr.builders.TextBuilder()
    )

    #Writing the on file
    file.write(txt)
    print(txt)

    # Display the resulting frame
    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        file.flush()
        file.close()
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()