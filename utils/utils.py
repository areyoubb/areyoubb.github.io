import pandas as pd
import pymysql

db = pymysql.connect(
    host='localhost',
    user='root',
    password='20021215',
    db='maoyantop100',
    charset='utf8'
)
db.cursor()
sql = 'select * from maoyantop'
df = pd.read_sql(sql,db)

sql1 = 'select * from mypl'
df1 = pd.read_sql(sql1,db)

def typeList(type):
    type = df[type].values
    type = list(map(lambda x:x.split(','),type))
    typeList = []
    for i in type:
        for j in i:
            typeList.append(j)
    return  typeList


