import pymysql

db = pymysql.connect(
    host='localhost',
    user='root',
    password='20021215',
    db='maoyantop100',
    charset='utf8'
)
cu = db.cursor()

def querys(sql,params,type='no_select'):
    params = tuple(params)
    cu.execute(sql,params)
    if type != 'no_select':
        data_list = cu.fetchall()
        db.commit()
        return data_list
    else:
        db.commit()
        return '执行成功'

