import  requests
import parsel
import time
import json
import pymysql
import pandas as pd
import re

db = pymysql.connect(
    host='localhost',
    user='root',
    password='20021215',
    db='maoyantop100',
    charset='utf8'
)
cu = db.cursor()
sql = """select releasetime from maoyantop"""
data = pd.read_sql(sql,db)
data1 = pd.DataFrame(data)
ls = []
for i in range(len(data1)):
    ls = data1.iloc[i].tolist()
    s = ''.join(ls)
    b = re.sub("'",'',s[5:15])
    data1.iloc[i]=b
    url = 'https://m.maoyan.com/mmdb/comments/movie/{}.json?_v_=yes&offset=3&startTime={}'.format(1292, b)
    print(url)
    break



headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54',
'cookie' : 'Cookie: _lxsdk_cuid=184174852ffc8-008eee64429eac-7b555472-144000-184174852ffc8; _lxsdk=95883010CC4A11EDBD26259CDD2D2B04F3AC4D66D8FC49088B9DAD6F1D1D3E04; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1679968660,1679971948,1679994018,1680015288'
}
last_time = ''
re = requests.get(url=url,headers=headers)
re.encoding = 'utf-8'
# print(re.text)
josn1 = re.json()["hcmts"]
for i in range(len(josn1)):
    nick = josn1[i]['nick']
    content = josn1[i]['content']
    content = content.replace('\n','')
    print(nick,'\n',content)





