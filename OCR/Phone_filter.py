import re
import numpy as np

phnos="""
9007904635
9004635123
9007904212
8132621224
5788979045
9007904635
9007904635
7487919290
9000112661
"""

phnos=re.split('\n',phnos)

freq=np.unique(phnos,return_counts=True)[1].tolist()
val=np.unique(phnos,return_counts=True)[0].tolist()

maxindex=freq.index(max(freq))
maxval=val[maxindex]

print(maxval)
