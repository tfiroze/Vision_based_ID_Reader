import random

def RegGen():
    year = ["18","19","20"]
    branch = ["BCE","BML","BIS","BSW","BEC","BIT","BKT"]
    yearPicker = random.choices(year, weights=(5,25,55))
    branchPicker = random.randint(0,6)
    if (branch[branchPicker] == "BCE" or branch[branchPicker]=="BEC"):
        id = random.randint(1,2000)
        if (id > 999):
            regID = str(yearPicker[0]+branch[branchPicker]+str(id))
        elif (99 < id < 999):
            regID = str(yearPicker[0]+branch[branchPicker]+"0"+str(id))
        elif (9<id<99):
            regID = str(yearPicker[0]+branch[branchPicker]+"00"+str(id))
        else:
            regID = str(yearPicker[0]+branch[branchPicker]+"000"+str(id))
    else:
        id = random.randint(1,500)
        if (99 < id < 501):
            regID = str(yearPicker[0]+branch[branchPicker]+"0"+str(id))
        elif (9<id<99):
            regID = str(yearPicker[0]+branch[branchPicker]+"00"+str(id))
        else:
            regID = str(yearPicker[0]+branch[branchPicker]+"000"+str(id))

    return regID
