import csv
import pandas as pd

fields = ['match_id','radiant_win']

df = pd.read_csv('match.csv',skipinitialspace=True, usecols=fields)

df['radiant_win'] = df['radiant_win'].astype(int)

fields2 = ['match_id','hero_id']

heros = pd.read_csv('players.csv',skipinitialspace=True, usecols=fields2)

with open('oldmatchdata.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(['radiant_win','rhero1','rhero2','rhero3','rhero4','rhero5','dhero1','dhero2','dhero3','dhero4','dhero5'])

for match in df.match_id:
    herosPlayed = heros.loc[heros['match_id'] == match]
    heroslist = herosPlayed['hero_id'].values.tolist()
    
    dlist = df['radiant_win'].values[match].tolist()
    
    
    fList = [dlist] + heroslist
    
    with open('oldmatchdata.csv', 'a') as f:
        write = csv.writer(f)
        write.writerow(fList)
    
    


    


# for match in df.match_id:
#     heros = 