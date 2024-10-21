from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
import requests

url="https://www.ttfi.org/events/ranking/MjAyNA==/NDk"
response=requests.get(url)
soup=BeautifulSoup(response.content,'html.parser')
table=soup.find('table')

data=[]
for row in table.find_all('tr')[1:]:
    cols=row.find_all('td')
    if(len(cols)>=5):
        TTFI_ID=cols[0].text.strip()
        NAME=cols[1].text.strip()
        STATE=cols[2].text.strip()
        DOB=cols[3].text.strip()
        National_Ranking=cols[4].text.strip()  
        data.append([TTFI_ID,NAME,STATE,DOB,National_Ranking])
    
       
        
df=pd.DataFrame(data)
print(df)

no_of_players=df[(df['National_Ranking']>'19')&(df['National_Ranking']<'25')]
x=len(no_of_players)
print("\nno.of players from 19 to 25: ",x)

born_after_2010=df[(df['DOB']>'31 Dec 2010')]
print("\nplayer born after 2010 ",born_after_2010)

client=MongoClient("mongodb://127.0.0.1:27017")
db=client(['players'])
collection=db(['details'])

collection.insert_many(data)
y=collection.find({'STATE':'UP'})
for temp in y:
    print(temp)
y=collection.find({'National_Ranking':'10'})
for temp in y:
    print(temp)
