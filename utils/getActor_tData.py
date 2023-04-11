from .utils import *
import numpy as np

def getDirectorsDataTop():
    directors = typeList('director')
    dirObj = {}
    for i in directors:
        if dirObj.get(i, -1) == -1:
            dirObj[i] = 1
        else:
            dirObj[i] += 1
    dirSortObj = sorted(dirObj.items(),key=lambda x : x[1],reverse=True)[:20]
    tDirData = np.array(dirSortObj)[::-1]
    row = []
    columns = []
    for i in tDirData:
        row.append(i[0])
        columns.append(i[1])
    return row,columns

def getstarsDataTop():
    stars = typeList('star')
    starsObj = {}
    for i in stars:
        if starsObj.get(i, -1) == -1:
            starsObj[i] = 1
        else:
            starsObj[i] += 1
    starsSortObj = sorted(starsObj.items(), key=lambda x: x[1], reverse=True)[:20]
    tstarsSortObj = np.array(starsSortObj)[::-1]
    row = []
    columns = []
    for i in starsSortObj:
        row.append(i[0])
        columns.append(i[1])
    return row, columns
