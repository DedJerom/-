import requests
import pandas as pd
import sqlite3
offset_ = 1
limit_ = 1000
objids = []
url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/kn/object?offset={offset_}&limit={limit_}&sortField=devId.devShortCleanNm&sortType=asc&objStatus=0'
res = requests.get(url)
objects_data = res.json()
count = int(objects_data.get('data').get('total'))


while True:
    if (offset_ + limit_) < count:
        url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/kn/object?offset={offset_}&limit={limit_}&sortField=devId.devShortCleanNm&sortType=asc&objStatus=0'
        res = requests.get(url)
        objects_data = res.json()
        objects_list = objects_data.get('data').get('list')
        for i in objects_list:
            objids.append(i.get('objId'))
        offset_ += limit_
    else:
        limit_ = (count - offset_)+1
        url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/kn/object?offset={offset_}&limit={limit_}&sortField=devId.devShortCleanNm&sortType=asc&objStatus=0'
        res = requests.get(url)
        objects_data = res.json()
        objects_list = objects_data.get('data').get('list')
        for i in objects_list:
            objids.append(i.get('objId'))
        break


d=[]
for obj in objids:
    url = f'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/object/{obj}'
    res = requests.get(url)
    d.append(res.json())
    
df = pd.json_normalize(d)
pd.DataFrame(df).to_csv('DATAFRAME.csv')
pd.DataFrame(df).to_excel('DATAFRAME.xlsx')
pd.DataFrame(df).to_pickle('DATAFRAME.pkl')
conn = sqlite3.connect("new_building")
df[['data.photoRenderDTO','data.objectTransportInfo','data.metro.colors','data.rnvDTO']] = df[['data.photoRenderDTO','data.objectTransportInfo','data.metro.colors','data.rnvDTO']].astype(str)

pd.DataFrame(df).to_sql(name='DATAFRAME', con=conn, if_exists='replace', index=False)


