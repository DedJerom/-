
import requests
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

class DomIdLoader:
    def __init__(self,offset_, limit_, url):
        self.offset_ = offset_
        self.limit_ = limit_
        self.url = url
        self.objects_data = None
        self.objids = None

    def get_ids(self, count):
        count=count
        print(count)
        self.objids=[]
        paramz = {
            'offset': self.offset_,
            'limit': self.limit_,
            'sortField': 'devId.devShortCleanNm',
            'sortType': 'asc',
            'objStatus': '0',
        }
        while True:
            if (self.offset_ + self.limit_) < count:
                paramz = {
                    'offset': self.offset_,
                    'limit': self.limit_,
                    'sortField': 'devId.devShortCleanNm',
                    'sortType': 'asc',
                    'objStatus': '0',
                }
                print(paramz)
                res = requests.get(self.url, params=paramz)
                self.objects_data = res.json()
                objects_list = self.objects_data.get('data').get('list')
                for i in objects_list:
                    self.objids.append(i.get('objId'))
                self.offset_ += self.limit_
            else:
                print(count)
                self.limit_ = (count - self.offset_) + 1
                paramz = {
                    'offset': self.offset_,
                    'limit': self.limit_,
                    'sortField': 'devId.devShortCleanNm',
                    'sortType': 'asc',
                    'objStatus': '0',
                }
                print(self.limit_)
                print(paramz)
                res = requests.get(self.url, params=paramz)
                self.objects_data = res.json()
                objects_list = self.objects_data.get('data').get('list')
                for i in objects_list:
                    self.objids.append(i.get('objId'))
                break


    def show_ids(self):
         return(self.objids)
class AllIdLoader:
    def __init__(self, url):
        self.url = url
        self.objects_data = None
        self.count = None
    def FindCountAllDom(self):
        paramz = {
            'sortField': 'devId.devShortCleanNm',
            'sortType': 'asc',
            'objStatus': '0',
        }
        res = requests.get(self.url, params= paramz)
        self.objects_data = res.json()
        self.count= int(self.objects_data.get('data').get('total'))
        return(self.count)


class ObjectInfoExtractor:
    def __init__(self, ids, url):
        self.IdBuild = ids
        self.Baza = None
        self.url = url
        self.df = None
    def load_data(self):
        self.Baza=[]
        for obj in self.IdBuild:
            res = requests.get(self.url + str(obj))
            self.Baza.append(res.json())
        self.df = pd.json_normalize(self.Baza)
    def df_return(self):
        return self.df

class Saver:
    def __init__(self, data):
        self.DF = data
    def save_csv(self, Name):
        pd.DataFrame(self.DF).to_csv(Name)

    def save_xl(self,Name):
        pd.DataFrame(self.DF).to_excel(Name)

    def save_sql(self,Name_BD,Name):
        conn = sqlite3.connect(Name_BD)
        print(self.DF)
        object_columns = self.DF.select_dtypes(include=['object']).columns
        for obj in object_columns:
            self.DF[[obj]]= self.DF[[obj]].astype(str)
        pd.DataFrame(self.DF).to_sql(name=Name, con=conn, if_exists='replace', index=False)


class Visualizer:
    def __init__(self, data=None):
        self.df = data
    def load_df_excel(self,name):
        self.df = pd.read_excel(name)
    def make_boxplot(self, X, Y):
        self.df = pd.read_excel("DATAFRAME.xlsx")
        sns.scatterplot(data=self.df, x=X, y=Y)
        plt.show()

    def make_heatmap(self,array_name):
        self.df = pd.read_excel("DATAFRAME.xlsx")
        heatmap_df = self.df[[arr for arr in array_name]]
        heatmap = sns.heatmap(heatmap_df.corr(), vmin=-1, vmax=1, annot=True)
        plt.show()



dataframe1 = DomIdLoader(1,1000,'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/kn/object')
dataframe1.get_ids(AllIdLoader('https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/kn/object').FindCountAllDom())
AllBuild1 = ObjectInfoExtractor(dataframe1.show_ids(),'https://xn--80az8a.xn--d1aqf.xn--p1ai/%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D1%8B/api/object/')
AllBuild1.load_data()
Saver(AllBuild1.df_return()).save_sql("25.12.2022","Test_build_25.12")











new_df=pd.read_excel("DATAFRAME.xlsx")

#Средняя цена в разрезе регионов
region_price = new_df.set_index('data.developer.regRegionDesc')['data.objPriceAvg']
region_price.groupby('data.developer.regRegionDesc').mean().plot(kind='barh').sort_values('data.objPriceAvg')
plt.show()
#График застройка в разрезе регионов
count_build = new_df[['data.developer.regRegionDesc','data.developer.devId','data.developer.buildObjCnt']]
count_build = count_build.drop_duplicates()
count_build = count_build.set_index('data.developer.regRegionDesc')['data.developer.buildObjCnt']
count_build.groupby('data.developer.regRegionDesc').sum().plot(kind='barh')
plt.show()

#График застройка в разрезе дат
count_build = new_df[['data.developer.regRegionDesc','data.developer.devId','data.developer.buildObjCnt','data.objReady100PercDt']]
count_build = count_build.set_index('data.objReady100PercDt')['data.developer.regRegionDesc']
count_build.groupby('data.objReady100PercDt').size().sort_values('data.objReady100PercDt').plot()
plt.show()


#График парковочных мест

count_parking = new_df[['data.developer.regRegionDesc','data.objElemParkingCnt']]
count_parking.groupby('data.developer.regRegionDesc').sum().sort_values('data.objElemParkingCnt').plot(kind='barh')
plt.show()

#График максимальное кол-во этажей в регионах
Max_floor = new_df[['data.developer.regRegionDesc','data.floorMax']]
Max_floor.groupby('data.developer.regRegionDesc').max().sort_values('data.floorMax').plot(kind='barh')
plt.show()

#Средние цены
fig, ax = plt.subplots()
ax.hist(new_df['data.objPriceAvg'])
plt.show()


sns.scatterplot(data=new_df, x='data.objPriceAvg', y='data.floorMax', hue='data.developer.regRegionDesc')
plt.show()
sns.scatterplot(data=new_df, x='data.floorMax', y='data.objElemLivingCnt')
plt.show()

heatmap_df = new_df[['data.floorMax', 'data.objElemLivingCnt','data.objPriceAvg','data.objSquareLiving','data.objElemParkingCnt']]

heatmap = sns.heatmap(heatmap_df.corr(), vmin=-1, vmax=1, annot=True)
plt.show()





