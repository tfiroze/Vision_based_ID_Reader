from regID import RegGen
from time_and_location_data import timeandlocation
from firebase import firebase

llist = []
firebase = firebase.FirebaseApplication('https://vision-based-id-reader.firebaseio.com/', None)

for i in range(10):
    time,location = timeandlocation()
    regNo = RegGen()
    if regNo not in llist:
        llist.append(regNo)
        Creds = {"Time":time,"Registration Number": regNo, "Location": location}
        result = firebase.post("/TestDat",Creds)
    print(Creds)
    

print(len(llist))