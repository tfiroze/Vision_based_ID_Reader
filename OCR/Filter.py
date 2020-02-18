import re
import numpy as np

#A test string
string="""
Dev Shankar Paul,19BEE0375
Ded Shankar Paul,19BEE0375
Dev Shankar Pails,19BEE0375
Dev Shanakar Paul,19BEE0375
Dev Shankar Paul,19BEE0375
Dev Shankar Paul,19BEE0375
Dev Shankar Paul,19BEE0375
Dev Shankar Paul,19BEE0375
Dev Shankar Paul,19BEE0375
Dev Shankar Paul,19BEE0375
Dev Shankar Paul,19BEE0375
Dev Shankar Paul,19BEE0375
"""

regs=[]

#Split the string into Names and Registration numbers
string=re.split('\n|,',string)

#Separate Registration numbers and other redundant data(if any) from list
for i in string:
    if(i.isalpha()==False):
        string.remove(i)
        regs.append(i)

#Get the frequency of elements and the elements as lists (in ascending order)
freq=np.unique(string,return_counts=True)[1].tolist()
val=np.unique(string,return_counts=True)[0].tolist()

regfreq=np.unique(regs,return_counts=True)[1].tolist()
regval=np.unique(regs,return_counts=True)[0].tolist()

#Get the index where the maximum value is located
maxindex=freq.index(max(freq))
maxregindex=regfreq.index(max(regfreq))

#Get the most frequently occuring element
maxstr=val[maxindex]
maxreg=regval[maxregindex]

#printing the filtered values
print(maxstr)
print(maxreg)

