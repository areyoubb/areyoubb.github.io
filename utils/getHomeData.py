from .utils import *


def getHomeData():
    maxMovieLen = len(df.values) #电影总个数
    maxRate = df['score'].max() #最高评分
    castsList = typeList('star')
    maxCasts = max(castsList,key=castsList.count) #劳模
    typesList = typeList('type')
    maxTypes = len(set(typesList)) #总类型个数
    langList = typeList('oriLang')
    maxLang = max(langList, key=langList.count)  # 最多语言
    return maxMovieLen,maxRate,maxCasts,maxTypes,maxLang

def getTypesEchartsData():
    typesList = typeList('type')
    typeObj={}
    for i in typesList:
        if typeObj.get(i,-1) == -1:
            typeObj[i] = 1
        else:
            typeObj[i] = typeObj[i] + 1
    typeEcharts = []
    for key,value in typeObj.items():
        typeEcharts.append({
            'name':key,
            'value':value
        })
    return  typeEcharts

def getRateEchats():
    rateList = df['score'].map(lambda x:float(x)).values
    rateList.sort()
    rateObj = {}
    for i in rateList:
        if rateObj.get(i, -1) == -1:
            rateObj[i] = 1
        else:
            rateObj[i] = rateObj[i] + 1
    return list(rateObj.keys()),list(rateObj.values())

def getTableData():
    return  df.values