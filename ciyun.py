import jieba
import wordcloud
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import random
import imageio
from utils.query import *
from utils.utils import *

def getimg(comments):
    cut = jieba.cut(comments)
    string = ''.join(cut).replace('\n', '').replace('\r', '').replace('n','')
    # img = Image.open(r'C:\study\python\bis\static\img\kl.jpg')
    # img_arr = np.array(img)
    mk = imageio.imread(r'C:\study\python\bis\static\img\{}.jpg'.format(random.randint(1,11)))
    print(r'C:\study\python\bis\static\img\{}.jpg'.format(random.randint(1,11)))
    color_new = wordcloud.ImageColorGenerator(mk)
    wc = WordCloud(
        background_color='white',
        mask=mk,
        font_path='simhei.ttf',
        contour_color='gray',
        color_func=color_new,
        max_words=20000
    )
    wc.generate_from_text(string)

    #绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')
    randomInt = random.randint(1,1000)
    plt.savefig('./static/img/wct/{}.png'.format(randomInt),dpi=200)
    return '/static/img/wct/{}.png'.format(randomInt)


def getimgByTitle(field,target,resImage):
    sql = 'select {} from maoyantop'.format(field)
    data = querys(sql,[],'select')
    comments = ''
    for i in data:
        comments = comments+i[0]
    cut = jieba.cut(comments)
    string = ' '.join(cut)
    print(string)
    mk = imageio.imread(target)
    color_new = wordcloud.ImageColorGenerator(mk)
    wc = WordCloud(
        background_color='white',
        mask=mk,
        font_path='simhei.ttf',
        contour_color='gray',
        color_func=color_new,

    )
    wc.generate_from_text(string)

    #绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')
    plt.savefig(resImage,dpi=200)


def getimgByActor(field,target,resImage,type):
    starList = typeList('star')
    comments = ''
    for i in starList:
        comments = comments+i[0]
    cut = jieba.cut(comments)
    string = ' '.join(cut)
    print(string)
    mk = imageio.imread(target)
    color_new = wordcloud.ImageColorGenerator(mk)
    wc = WordCloud(
        background_color='white',
        mask=mk,
        font_path='simhei.ttf',
        contour_color='gray',
        color_func=color_new,

    )
    wc.generate_from_text(string)

    #绘制图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')
    plt.savefig(resImage,dpi=200)


getimgByTitle('name',r'C:\study\python\bis\static\img\4.jpg','./static/img/wct/title_t.png')
getimgByActor('star',r'C:\study\python\bis\static\img\5.jpg','./static/img/wct/star_t.png','star')

