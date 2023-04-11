import requests
import parsel
import pymysql
import time as tm
import random
import json

#确定真实的url地址
headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'__mta=140808461.1666837926934.1680836991489.1680837011371.175; _lxsdk_cuid=184174852ffc8-008eee64429eac-7b555472-144000-184174852ffc8; uuid_n_v=v1; uuid=95883010CC4A11EDBD26259CDD2D2B04F3AC4D66D8FC49088B9DAD6F1D1D3E04; _lxsdk=95883010CC4A11EDBD26259CDD2D2B04F3AC4D66D8FC49088B9DAD6F1D1D3E04; ci=55%2C%E5%8D%97%E4%BA%AC; ci.sig=hoCtvadkL6uyN_XrKMXw3c-CPCM; featrues=[object Object]; featrues.sig=KbQquuOrr42L3kMHbtKc319ems8; _csrf=ca881e29eabe7b7c875c42dc86c296922253fcb219d9924bf1efdf2a44253b10; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1680495287,1680666101,1680775371,1680833764; _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; __mta=140808461.1666837926934.1680836096099.1680836207768.165; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1680837011; _lxsdk_s=187597fdacb-19c-365-eea%7C%7C68',
'Host':'www.maoyan.com',
'Referer':'https://tfz.maoyan.com/',
'sec-ch-ua':'"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
'sec-ch-ua-mobile':'?0',
'sec-ch-ua-platform':'"Windows"',
'Sec-Fetch-Dest':'document',
'Sec-Fetch-Mode':'navigate',
'Sec-Fetch-Site':'same-site',
'Sec-Fetch-User':'?1',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62'
}

headers1 = {
'Cookie':'__mta=142375821.1679885971059.1680144635906.1680669588162.112; uuid_n_v=v1; uuid=65036C10CC4B11EDBCBCAB7DE9BBBE740279836B7BE44093B7D465D90D3A5F39; _lxsdk_cuid=1872101ae21c8-01f81d117066be-26031851-144000-1872101ae22c8; ci=55%2C%E5%8D%97%E4%BA%AC; ci.sig=hoCtvadkL6uyN_XrKMXw3c-CPCM; WEBDFPID=0y4951470x3y5896y7z96y6x27u7wv8u8127319765997958z66y48zz-1995338144452-1679978143760QSQAUCUfd79fef3d01d5e9aadc18ccd4d0c95071957; token=AgHIIbO5UjHnTyQEWZxsCzg20BrNGWgQ0F7oxNA5APPxIqw5U4DI8EFGDcoqsgcVv4p4IgZ1fxn28QAAAABPFwAAfp8qhdGzWMqhbcAtSz8ngPa-G4zDlQzpzwRy-pkNgJU7Ufd2NO1b2DVwi44_YsbE; uid=2629226624; uid.sig=crOw-XJI29Atyju8l5stvSbi_z4; _lxsdk=65036C10CC4B11EDBCBCAB7DE9BBBE740279836B7BE44093B7D465D90D3A5F39; __mta=142375821.1679885971059.1679988872710.1679988876693.69; _csrf=3410a0934383edf37765b05551bf04e292ee38cce2598ac1985f44fb09e5c4c4; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1679973734,1680012007,1680142545,1680669588; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1680669588; _lxsdk_s=1874fb6ba2d-7e7-a5f-230%7C%7C2',
'Host':'m.maoyan.com',
'sec-ch-ua':'"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
'sec-ch-ua-mobile':'?0',
'sec-ch-ua-platform':'"Windows"',
'Sec-Fetch-Dest':'document',
'Sec-Fetch-Mode':'navigate',
'Sec-Fetch-Site':'none',
'Sec-Fetch-User':'?1',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 S'
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
    pa = 0
    pa1 = 0
    for dd in dds:
        href = dd.css('.name a::attr(href)').get()
        href = href[7:]
        time1 = dd.css('.releasetime::text').get()
        time1 = time1[5:15]
        name = dd.css('.name a::attr(title)').get()
        for html in href:
            pl_url = 'https://m.maoyan.com/mmdb/comments/movie/{}.json?_v_=yes&offset=10&startTime='.format(href)
            re = requests.get(url=pl_url, headers=headers1)
            re.encoding = 'utf-8'
            josn1 = re.json()["hcmts"]
            print('正在爬取{}的评论'.format(name))
            tm.sleep(random.randint(0, 3))
            for i in range(len(josn1)):
                nick = josn1[i]['nick']
                score = josn1[i]['score']
                # city = josn1[i]['cityName']
                content = josn1[i]['content']
                content = content.replace('\n', '')
                print(nick,'\t',score, '\n', content)
            # 插入数据库
                sql = """INSERT INTO mypl(name,nick,score,content)
                    VALUES(%s,%s,%s,%s)"""
                try:
                    cu.execute(sql, (name,nick,score,content))
                    db.commit()
                except:
                    db.rollback()
            if nick == nick:
                break;

    tm.sleep(random.randint(3, 5))

cu.close()
db.close()


# # print(dds)


