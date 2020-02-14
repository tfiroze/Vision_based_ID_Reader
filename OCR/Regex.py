import re

#SAMPLE DATA [BACK OF ID CARD]
stringback = """
App. No: 2019012333
Blood Group : O+
Official Address:
    Vellore Institute of Technology,
    Vellore - 632 014, Tamilnadu, India.
    Ph : 0416 224 3091
    Fax : 0416 224 3092
Address:
    FLAT-8/8,CHAYANAT HSG. COMPLEX, 1050/2, SURVEY PARK,
    NEAR BENGAL AMBUJA
    HOUSING COMPLEX, KOLKATA,700075, WEST BENGAL,
    INDIA
Contact No.
    9007904635
    
Valid upto: JUL-2023
Issuing Authority   Holder's Signature  
19BEE0375
Website:www.vit.ac.in
"""

stringfront= """
VIT
VELLORE CAMPUS
Dev Shankar Paul
19BEE0375
HOSTELLER
"""

def extract_phone_number(string):
    pattern=re.compile(r'\d{10}')
    r=pattern.findall(string)
    r=r[len(r)-1]
    return r

def extract_reg_number(string):
    pat3=re.compile(r'[0-2][0-9][B|M][A-Z][A-Z][0-2][0-9][0-9][0-9]')
    re3=pat3.findall(string)
    re3=''.join(re3)
    return re3

numbers = extract_phone_number(stringback)
regs=extract_reg_number(stringback)

print(numbers)
print('\n')
print(regs)
print('\n')

