import requests
import parsel
import pymysql
import time

#确定真实的url地址
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54',
            'cookie' : '__mta=142375821.1679885971059.1680695671548.1680695707380.118; uuid_n_v=v1; uuid=65036C10CC4B11EDBCBCAB7DE9BBBE740279836B7BE44093B7D465D90D3A5F39; _lxsdk_cuid=1872101ae21c8-01f81d117066be-26031851-144000-1872101ae22c8; ci=55%2C%E5%8D%97%E4%BA%AC; ci.sig=hoCtvadkL6uyN_XrKMXw3c-CPCM; WEBDFPID=0y4951470x3y5896y7z96y6x27u7wv8u8127319765997958z66y48zz-1995338144452-1679978143760QSQAUCUfd79fef3d01d5e9aadc18ccd4d0c95071957; token=AgHIIbO5UjHnTyQEWZxsCzg20BrNGWgQ0F7oxNA5APPxIqw5U4DI8EFGDcoqsgcVv4p4IgZ1fxn28QAAAABPFwAAfp8qhdGzWMqhbcAtSz8ngPa-G4zDlQzpzwRy-pkNgJU7Ufd2NO1b2DVwi44_YsbE; uid=2629226624; uid.sig=crOw-XJI29Atyju8l5stvSbi_z4; _lxsdk=65036C10CC4B11EDBCBCAB7DE9BBBE740279836B7BE44093B7D465D90D3A5F39; __mta=142375821.1679885971059.1679988872710.1679988876693.69; _csrf=3410a0934383edf37765b05551bf04e292ee38cce2598ac1985f44fb09e5c4c4; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1679973734,1680012007,1680142545,1680669588; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1680695707; _lxsdk_s=18751446bda-dea-5e8-3f7%7C2629226624%7C9'}
page = 0
file_name=r'E:\bishe\img\\'
# db = pymysql.connect(
#     host='localhost',
#     user='root',
#     password='20021215',
#     db='maoyantop100',
#     charset='utf8'
# )
# cu = db.cursor()

for i in range(0,91,10):
    page += 1
    print('============正在爬取第{}页============'.format(page))
    url = 'https://www.maoyan.com/board/4?offset={}'.format(i)

#发送请求
    response = requests.get(url=url,headers=headers)
    # print(response)
    html_text = response.text
    # print(html_text)

# #解析数据
    parse = parsel.Selector(html_text) #转换数据类型
    dds = parse.css('.board-wrapper dd')
    for dd in dds:
        name = dd.css('.name a::attr(title)').get()
        href1 = dd.css('.name a::attr(href)').get()
        href1 = href1[7:]
        img_href = dd.css('.image-link img::attr(data-src)').get()
        img_content = requests.get(url=img_href,headers=headers).content
        with open(file_name+href1+'.jpg',mode='wb') as f:
            f.write(img_content)
            print(name,img_href)
    time.sleep(3)




