import requests
import parsel
import pymysql
import time as tm
import random
import json

#确定真实的url地址
headers = {
'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
'cookie' : '__mta=140808461.1666837926934.1680667253554.1680667259440.127; _lxsdk_cuid=184174852ffc8-008eee64429eac-7b555472-144000-184174852ffc8; uuid_n_v=v1; uuid=95883010CC4A11EDBD26259CDD2D2B04F3AC4D66D8FC49088B9DAD6F1D1D3E04; _lxsdk=95883010CC4A11EDBD26259CDD2D2B04F3AC4D66D8FC49088B9DAD6F1D1D3E04; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; _csrf=cb202da7b785e5fb5927322f10e8e3a20bdb26ed6bfbaf2616b5a7c16b840c8f; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1680406171,1680487211,1680495287,1680666101; __mta=140808461.1666837926934.1680666924463.1680667229721.121; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1680667259; _lxsdk_s=1874f8184b8-7c0-e56-f6a%7C%7C40'
}

headers1 = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'_lxsdk_cuid=184174852ffc8-008eee64429eac-7b555472-144000-184174852ffc8; _lxsdk=95883010CC4A11EDBD26259CDD2D2B04F3AC4D66D8FC49088B9DAD6F1D1D3E04; uuid_n_v=v1; uuid_n_v.sig=FRxddd2YAJ1gjqdUfeFwe7NJ00g; iuuid=186A2A40D4EA11ED9D8C63EC269F30B5E4781A70F65648FDAE2EF959A42C5BA9; iuuid.sig=QuZchFW_FYdS6iHaNn46XJNH8IY; webp=true; webp.sig=95QtTJb-iuzhirMSz19_ivGc7OY; ci=55%2C%E5%8D%97%E4%BA%AC; ci.sig=hoCtvadkL6uyN_XrKMXw3c-CPCM; ci=55%2C%E5%8D%97%E4%BA%AC; ci.sig=hoCtvadkL6uyN_XrKMXw3c-CPCM; ci=55%2C%E5%8D%97%E4%BA%AC; ci.sig=hoCtvadkL6uyN_XrKMXw3c-CPCM; featrues=[object Object]; featrues.sig=KbQquuOrr42L3kMHbtKc319ems8; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1680495287,1680666101,1680775371,1680833764; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1680833765; _lxsdk_s=187597fdacb-19c-365-eea%7C%7C3',
'Host':'m.maoyan.com',
'If-None-Match':'W/"152e-zg6GRoHY7yvrqB/qDob4/BYhYKU"',
'sec-ch-ua':'"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
'sec-ch-ua-mobile':'?0',
'sec-ch-ua-platform':'"Windows"',
'Sec-Fetch-Dest':'document',
'Sec-Fetch-Mode':'navigate',
'Sec-Fetch-Site':'none',
'Sec-Fetch-User':'?1',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62}',
}
page = 0

db = pymysql.connect(
    host='localhost',
    user='root',
    password='20021215',
    db='maoyantop100',
    charset='utf8'
)
cu = db.cursor()

for i in range(0,91,10):
    page += 1
    print('============正在爬取第{}页============'.format(page))
    url = 'https://www.maoyan.com/board/4?offset={}'.format(i)

#发送请求
    response = requests.get(url=url,headers=headers)
    html_text = response.text
    # print(html_text)

#解析数据
    parse = parsel.Selector(html_text) #转换数据类型
    dds = parse.css('.board-wrapper dd')

    for dd in dds:
        href = dd.css('.name a::attr(href)').get()
        href = href[7:]
        name = dd.css('.name a::attr(title)').get()
        for html in href:
            pl_url = 'https://m.maoyan.com/ajax/detailmovie?movieId={}'.format(href)
            re = requests.get(url=pl_url, headers=headers1)
            re.encoding = 'utf-8'
            josn1 = re.json()["detailMovie"]
            print('正在爬取{}的具体内容'.format(name))
            oriLang = josn1['oriLang']
            cat = josn1['cat']
            dir = josn1['dir']
            print(oriLang,cat,dir)
            tm.sleep(random.randint(0, 3))
            if name == name:
                break;

            # 插入数据库
            sql = """INSERT INTO mypl1(oriLang,typle,director)
                    VALUES(%s,%s,%s)"""
            try:
                cu.execute(sql, (oriLang,cat,dir))
                db.commit()
            except:
                db.rollback()
                print('插入失败')




cu.close()
db.close()


# # print(dds)


