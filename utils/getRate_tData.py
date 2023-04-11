from .utils import *

def getAllType():
    return list(set(typeList('type')))

def getAllRateDataByType(type):
    if type == 'all':
        rateList = df['score'].values
        rateList.sort()
    else:
        typelist = df['type'].map(lambda x: x.split(sep=','))
        oldrateList = df['score'].values
        rateList = []
        for i,item in enumerate(typelist):
            if type in item:
                rateList.append(oldrateList[i])

    rateObj = {}
    for i in rateList:
        if rateObj.get(i,-1) == -1:
            rateObj[i] = 1
        else:
            rateObj[i] = rateObj[i] + 1
    return list(rateObj.keys()),list(rateObj.values())

def getStar(searchIpt):
    stars = list(df1.loc[df1['name'].str.contains(searchIpt)]['score'])
    scoreData = []
    if searchIpt in df1['name'].values:
        searchName = list(df1.loc[df1['name'].str.contains(searchIpt)]['name'])[0]
        setStar = set(stars)
        count = 0
        for i in setStar:
            for j in stars:
                if i == j:
                    count +=1
            scoreData.append({'name':i,
                            'value':count
                                })
            count = 0
            b = 1
        return searchName,scoreData
    else:
        searchName = None
        return searchName, scoreData





def getYearMean():
    releasetime = list(set(df['releasetime'].values))
    yearList = []
    for i in set(df['releasetime']):
        a = int(i[:4])
        yearList.append(a)

    meanlist = []
    for i in releasetime:
        print(i)
        meanlist.append(df[df['releasetime'] ==i]['score'].mean())
    return yearList,meanlist