import requests
import json
import pandas as pd
import csv

with open('matchdata3.json') as f:
    data = json.load(f)


for d in data:
    
    win = d['radiant_win']
    rHeroes = d['radiant_team'].split(',')
    dHeroes = d['dire_team'].split(',')
    
    toCsv = []
    toCsv.append(int(win))
    print(int(win))
    toCsv.extend(rHeroes)
    toCsv.extend(dHeroes)
    toCsv = [toCsv]
    print(toCsv)

    #df = pd.DataFrame(toCsv,columns=['radiant_win','rhero1','rhero2','rhero3','rhero4','rhero5','dhero1','dhero2','dhero3','dhero4','dhero5'])

    #df.to_csv('matchdata.csv', index=False,header=False,mode='a')
    with open('matchdata.csv', 'a+') as f:
        write = csv.writer(f)
        write.writerow(toCsv)
    
    break