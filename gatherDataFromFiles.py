#
#Gather all the needed info from data in the folder data
#

import json
from os.path import exists

JSON_FILE = 1
CSV_FILE = 2
BOT_ID = 3
HUMAN_ID = 4
UNLABELED_ID = 5

BOT = 'BOT'
HUMAN = 'HUMAN'
UNLABELED = ''

SPLITTER = ','

OUTFILE = 'users_dataset.csv'

FILES = [
    #How to fill based on index :
    #0: Input file
    #1: File type
    #2: List of fields to gather. The first must always be the user id, used to check line validity
    #3: Label field
    #4: Mapping of check field value to our used labels. Use * to map everything to that value
    ["data\\cresci-rtbust-2019_tweets.json",JSON_FILE,["user,id"],"",""],
    ["data\\crowdflower_results_aggregated.csv",CSV_FILE,[9],3,{"genuine":HUMAN,"spambot":BOT}],
    ["data\\fake_followers.csv",CSV_FILE,[0],0,{"*":BOT}],
    ["data\\social_spambot_users_1.csv",CSV_FILE,[0],0,{"*":BOT}],
    ["data\\social_spambot_users_2.csv",CSV_FILE,[0],0,{"*":BOT}],
    ["data\\social_spambot_users_3.csv",CSV_FILE,[0],0,{"*":BOT}],
    ["data\\spambots_1.csv",CSV_FILE,[0],0,{"*":BOT}],
    ["data\\spambots_2.csv",CSV_FILE,[0],0,{"*":BOT}],
    ["data\\spambots_3.csv",CSV_FILE,[0],0,{"*":BOT}],
    ["data\\spambots_4.csv",CSV_FILE,[0],0,{"*":BOT}]
]

outFile = open(OUTFILE,'w', encoding="UTF-8")
for file in FILES:
    inFile = file[0]
    fileType = file[1]
    fields = file[2]
    labelField = file[3]
    labelMapping = file[4]

    inFile = open(inFile,'r', encoding="UTF-8")

    if fileType == JSON_FILE:
        data = inFile.readlines()
        if type(data) != str:
            data = ''.join(data)
        data = json.loads(data)
    else:
        data = []
        lines = inFile.readlines()
        for line in lines:
            data.append(line.split(SPLITTER))
    inFile.close()
    for entry in data:
        firstEntry = True
        fieldsLine = ""
        try :
            for field in fields:
                if type(field) == str:
                    if SPLITTER in field:
                        #Contains subfield, handle them
                        fieldValue = None
                        for subField in field.split(SPLITTER):
                            if fieldValue == None:
                                fieldValue = entry[subField]
                            else:
                                fieldValue = fieldValue[subField]
                    else:
                        fieldValue = entry[field]
                else:
                    fieldValue = entry[field].replace('"',"")
                #We expect first entry to be the user ID (which is mandatory info).
                #Check user ID validity
                if firstEntry:
                    if type(fieldValue) == str:
                        fieldValue = fieldValue.replace('"',"")
                        fieldValue = int(fieldValue)
                    firstEntry = False
                fieldsLine += str(fieldValue) + ","
        except: continue  #<= Line not valid continue>

        if labelField != '':
            label = entry[labelField].replace('"',"")
            if '*' in labelMapping:
                label = labelMapping['*']
            elif label in labelMapping:
                label = labelMapping[label]
            else:
                label = UNLABELED
        else:
            label = UNLABELED

        outFile.write(
            fieldsLine + label + "\n"
        )

outFile.close()