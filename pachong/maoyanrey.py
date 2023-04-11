import requests
import parsel
import pymysql
import time

#确定真实的url地址
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54',
            'cookie' : '__mta=142375821.1679885971059.1679885983930.1679929475832.5; uuid_n_v=v1; uuid=65036C10CC4B11EDBCBCAB7DE9BBBE740279836B7BE44093B7D465D90D3A5F39; _lxsdk_cuid=1872101ae21c8-01f81d117066be-26031851-144000-1872101ae22c8; __mta=142375821.1679885971059.1679885982301.1679885983930.4; ci=55%2C%E5%8D%97%E4%BA%AC; ci.sig=hoCtvadkL6uyN_XrKMXw3c-CPCM; featrues=[object Object]; featrues.sig=KbQquuOrr42L3kMHbtKc319ems8; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1679885971,1679929290; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _csrf=4c106483df6f6ca13c2e108ec35230d41a9e2930e72f2671cc2c8575031561e7; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1679929476; _lxsdk=65036C10CC4B11EDBCBCAB7DE9BBBE740279836B7BE44093B7D465D90D3A5F39; _lxsdk_s=1872396abce-052-55e-e52%7C%7C2'}
page = 0

db = pymysql.connect(
    host='localhost',
    user='root',
    password='20021215',
    db='maoyantop100',
    charset='utf8'
)
cu = db.cursor()


url = 'https://www.maoyan.com/board?requestCode=d2a868d7c350463690a0a67859bffd0cngjhj'

#发送请求
response = requests.get(url=url,headers=headers)
# print(response)
html_text = response.text
# print(html_text)

#解析数据
parse = parsel.Selector(html_text) #转换数据类型
dds = parse.css('.board-wrapper dd')
for dd in dds:
    name = dd.css('.name a::attr(title)').get()
    star = dd.css('.star::text').get().strip()
    releasetime = dd.css('.releasetime::text').get()
    score = dd.css('.score i::text').getall()
    score = ''.join(score)
    print(name, star, releasetime, score, sep=' | ')
    #插入数据库
    sql = """INSERT INTO reying(name,star,releasetime,score)
                VALUES(%s,%s,%s,%s)"""
    try:
            cu.execute(sql,(name,star,releasetime,score))
            db.commit()
    except:
            db.rollback()
cu.close()
db.close()


# # print(dds)


