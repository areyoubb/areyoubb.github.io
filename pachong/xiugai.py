import pymysql
import pandas as pd
db = pymysql.connect(
    host='localhost',
    user='root',
    password='20021215',
    db='maoyantop100',
    charset='utf8'
)
cu = db.cursor()
sql = 'select * from maoyantop0'
data = pd.read_sql(sql,db)
for i in range(98):
    href1 = data['href'][i][29:]
    name = data['name'][i]
    img_href = href1+'.jpg'
    sql1 = 'update maoyantop set img_href=%s where name=%s'
    try:
        cu.execute(sql1, (img_href, name))
        db.commit()
    except:
        db.rollback()
        print('你他妈插错了')

cu.close()
db.close()
