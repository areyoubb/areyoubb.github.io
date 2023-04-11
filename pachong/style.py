# for data scraping
#encoding:utf-8
import requests
from bs4 import BeautifulSoup
import time as ti
import csv
from lxml import etree
import re
# for data analyzing
import pandas as pd

#Part I: camouflage and request response:
def get_html(url):
    #Because many web pages have anti crawlers, we add hearders disguise
    #In the cat's eye movie web page -- F12 -- Network -- all -- 4 -- header -- find the user agent
    #Copy and paste the content
    headers = {  # 设置header
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Accept-Language' : 'zh-CN,zh;q=0.9',
        'Cache-Control' : 'no-cache',
        'Connection' : 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50',
        'referer' : 'https://passport.meituan.com/',
        'Cookie' : '__mta=42753434.1633656738499.1634781127005.1634781128998.34; uuid_n_v=v1; _lxsdk_cuid=17c5d879290c8-03443510ba6172-6373267-144000-17c5d879291c8; uuid=60ACEF00317A11ECAAC07D88ABE178B722CFA72214D742A2849B46660B8F79A8; _lxsdk=60ACEF00317A11ECAAC07D88ABE178B722CFA72214D742A2849B46660B8F79A8; _csrf=94b23e138a83e44c117736c59d0901983cb89b75a2c0de2587b8c273d115e639; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1634716251,1634716252,1634719353,1634779997; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1634781129; _lxsdk_s=17ca07b2470-536-b73-84%7C%7C12'
    }
    #The purpose of responding to the request, combined with the disguise of hearders, is to let the server know that this is not a crawler, but a person
    #Get website information using get
    result = requests.get(url, headers = headers)
    #Because the crawler is fast, the server may make an error 403
    #Write a judgment, 200 is success
    if result.status_code == 200:
        #The response is successful and a string is returned
        return result.text
    return


def parsing_html(html):
  ti.sleep(1)
  # patter = re.compile('<dd>.*?board-index')
  bsSoup = BeautifulSoup(html, 'html.parser')
  # a = [x.find("i").text for x in bsSoup.find_all("dd")]
  movies = bsSoup.find_all("dd")
  a = []
  for i in movies:
    ti.sleep(0.1)
    rating = i.find('i').text
    title = i.find("a").get("title")
    actors = re.findall("主演：(.*)", i.find("p", class_="star").text)[0]
    time = re.findall("上映时间：(.*)", i.find("p", class_="releasetime").text)[0]
    url1 = "https://maoyan.com" + i.find("p", class_="name").a.get("href")
    score = i.find("i", class_="integer").text + i.find("i", class_="fraction").text
    movie = get_html(url1)
    bsMovie = BeautifulSoup(movie, 'html.parser')
    # print(bsMovie)
    director = bsMovie.find("a", class_="name").text.replace("\n", "").replace(" ", "")
    income = bsMovie.find_all("div", class_="mbox-name")
    income = income[-2].text if income else "暂无"
    location_and_duration = bsMovie.find("div", class_="movie-brief-container").find_all("li", class_="ellipsis")[
      1].text.split('/')
    duration = location_and_duration[1].strip()
    location = location_and_duration[0].strip()
    ti.sleep(0.5)
    m_type_list = [t.text.strip() for t in
                   bsMovie.find("div", class_="movie-brief-container").find("li", class_="ellipsis").find_all("a",
                                                                                                              class_="text-link")]
    m_type = ','.join(m_type_list)
    ti.sleep(0.2)
    # print(m_type)
    c = {'Rating': rating,
         'Title': title,
         'Name of director': director,
         'Name of actors': actors,
         'Cumulative income': income,
         'Duration': duration,
         'Type': m_type,
         'Country or a Region': location,
         'Release time': time,
         'Web link': url1,
         'Score': score
         }
    a.append(c)
  return a

def write_to_file(content):
    with open('maoyan.csv', 'a', encoding='utf-8-sig')as csvfile:
      writer = csv.writer(csvfile)
      values = list(content.values())
      writer.writerow(values)
def next_page(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_html(url)
    for item in parsing_html(html):
      print(item)
      write_to_file(item)

for i in range(10):
    next_page(offset=10*i)
    ti.sleep(1)