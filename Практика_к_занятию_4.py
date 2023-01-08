
import requests
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import io
import random


#Задача 1
headers={
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
}
def get_content(url):
    with requests.Session() as req:
        req.headers.update(headers)
        r = req.get(url).content
    return r
def analysis(str_df,meaning,arr_df):
    substring_1 = "в пределах"
    substring_2 = "не более"

    if substring_1 in str_df:
        arr = str_df.split()
        arr = arr[2].split("-")
        if meaning == "б/цвета":
            arr_df.append('В норме')
        else:

            if float(meaning)>=float(arr[0].replace(",", "."))  and float(arr[1].replace(",", "."))>=float(meaning):
                arr_df.append('В норме')
            else:
                arr_df.append('Не в норме')
    if substring_2 in str_df:
        arr = str_df.split()
        arr = arr[2]
        if meaning == "б/цвета":
            arr_df.append('В норме')
        else:
            if '-' in arr:
                arr = arr.split("-")
                if float(meaning) >= float(arr[0].replace(",", ".")) and float(arr[1].replace(",", ".")) >= float(meaning):
                    arr_df.append('В норме')
                else:
                    arr_df.append('Не в норме')
            else:
                if float(arr.replace(",", "."))>= float(meaning):
                    arr_df.append('В норме')
                else:
                    arr_df.append('Не в норме')
arr_df=[]
url ="https://data.gov.ru/opendata/7708660670-rodnik-neskuchniy-sad/data-20160608T1215-structure-20160608T1215.csv"
s = get_content(url)
df=pd.read_csv(io.StringIO(s.decode('UTF8')))

for i in range(0, len(df.index)):
    analysis(df['Норматив'].values[i],df['Результат анализа'].values[i],arr_df)
df["Результат"]=arr_df
print(df.set_index("Показатель"))
pd.DataFrame(df).to_csv("Химического анализа родника в Нескучном саду")

#Задача 2

arr_1=[]

def task_1():
    box =[1,1,1,1,1,0,0,0,0]
    count=0
    for i in range(3):
        a =random.randint(0,len(box)-1)
        if box[a]==1:
            count+=1
            box.pop(a)
        else:
            box.pop(a)
    if count==3:
       return 1
    else:
        return 0
count_luck=0
for i in range(10000):
    arr=[]
    a=task_1()
    arr.append(a)
    if a == 1:
        count_luck+=1
        arr.append(count_luck/(i+1))
    else:
        arr.append(count_luck/(i+1))
    arr_1.append(arr)

print(arr_1[len(arr_1)-1])

#Задача 3

arr_1=[]

def task_1():
    box =[1,1,1,0,0,0,0,0,0,0]
    count=0
    for i in range(2):
        a =random.randint(0,len(box)-1)
        if box[a]==1:
            count+=1
            box.pop(a)
        else:
            box.pop(a)
            break
    if count==1:
       return 1
    else:
        return 0
count_luck=0
for i in range(10000):
    arr=[]
    a=task_1()
    arr.append(a)
    if a == 1:
        count_luck+=1
        arr.append(count_luck/(i+1))
    else:
        arr.append(count_luck/(i+1))
    arr_1.append(arr)

print(arr_1[len(arr_1)-1])