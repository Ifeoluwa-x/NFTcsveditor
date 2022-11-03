import os 
import csv
import pandas as pd
import json
import hashlib

# THIS block of code right here appends a new header column for the "HASH" space to the csv file
# op = open("chisel.csv", "r")
# dt = csv.DictReader(op)
# up_dt = []
# for r in dt:
# 	row = {'Series Number': r['Series Number'],
# 		'Filename': r['Filename'],
#         'Description': r['Description'],
#         'Gender': r['Gender'],
# 		'UUID': r['UUID']}
# 	up_dt.append(row)
# op.close()
# op = open("chisel.csv", "w", newline='')
# headers = ['Series Number', 'Filename','Description','Gender', 'UUID', 'HASH']
# data = csv.DictWriter(op, delimiter=',', fieldnames=headers)
# data.writerow(dict((heads, heads) for heads in headers))
# data.writerows(up_dt)
# op.close()








# This block of code creates a json array and stores in the the hash column
op = open("chisel.csv", "r")
dt = csv.DictReader(op)
up_dt = []
for r in dt:
	row = {'Series Number': r['Series Number'],
		'Filename': r['Filename'],
        'Description': r['Description'],
        'Gender': r['Gender'],
		'UUID': r['UUID'],
        'HASH': {
            "format": "CHIP-0007",
            "name": r['Filename'] ,
            "description": r['Description'],
            "minting_tool": "Team chisel",
            "sensitive_content": False,
            "series_number":r['Series Number'] ,
            "series_total": 526,
            "attributes": [
                {
            "trait_type": "gender",
            "value": r['Gender']
        }
    ],
            "collection": {
                "name": "Zuri NFT Tickets for Free Lunch",
                "id": r['UUID'],
                "attributes": [
                    {
                        "type": "description",
                        "value": "Rewards for accomplishments during HNGi9."
                    }
                ]
            }
        }}
	up_dt.append(row)
op.close()

op = open("chisel.csv", "w", newline='')
headers = ['Series Number', 'Filename','Description','Gender', 'UUID', 'HASH']
data = csv.DictWriter(op, delimiter=',', fieldnames=headers)
data.writerow(dict((heads, heads) for heads in headers))
data.writerows(up_dt)
op.close()





# This block of code takes each of thos json array and converts them to an encrypted hash code and updates the hash column

df = pd.read_csv("chisel.csv")
hash = df['HASH']
num = df['Series Number']
for x,y in zip(hash, num):
    up = json.dumps(x)
    ory = hashlib.sha256(up.encode('utf-8'))
    str_hex = ory.hexdigest()
    df.loc[y, 'HASH'] = str_hex

    # writing into the file
    df.to_csv("chisel.csv", index=False)
    