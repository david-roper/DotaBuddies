import json
import csv

last_match_id = ''
url = 'https://api.opendota.com/api/publicMatches?game_mode=22' + last_match_id

with open('matchdata2.json') as f:
    data1 = json.load(f)

with open('matchdata5.json') as f1:
    data2 = json.load(f1)


for d in data1:
    last = d['match_id']
    break

for d in data1:
    if(d['match_id'] < last):
        last = d['match_id']  


for d in data1:
    for d2 in data2:
        if(d['match_id'] == d2['match_id']):
            print("id: ",d['match_id'])

last_match_id = '&less_than_match_id=' + str(last)

url = 'https://api.opendota.com/api/publicMatches?game_mode=22' + last_match_id

print(url)
