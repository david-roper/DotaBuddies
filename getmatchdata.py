import requests
import json
import pandas as pd
import csv
import time

last_match_id = ''
with open('newmatchdata.csv', 'a') as f:
    write = csv.writer(f)
    write.writerow(['radiant_win','rhero1','rhero2','rhero3','rhero4','rhero5','dhero1','dhero2','dhero3','dhero4','dhero5'])
for j in range(8):
    
    for i in range(50):

        url = 'https://api.opendota.com/api/publicMatches?game_mode=22' + last_match_id

        response = requests.get(url)

        data = response.json()

        last = data[0]['match_id']
        for d in data:
            
            win = d['radiant_win']
            rHeroes = d['radiant_team'].split(',')
            dHeroes = d['dire_team'].split(',')
            
            toCsv = []
            toCsv.append(int(win))
            toCsv.extend(rHeroes)
            toCsv.extend(dHeroes)
            toCsv = [toCsv]

            if(d['match_id'] < last):
                last = d['match_id'] 
            

            with open('newmatchdata.csv', 'a') as f:
                write = csv.writer(f)
                write.writerow(toCsv[0])
            
            
            last_match_id = '&less_than_match_id=' + str(last)
        print('done match: ', i)
    print('last match: ', last)  
    time.sleep(60)
    