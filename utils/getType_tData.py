from .utils import *

def getTypeDate():
    typelist = typeList('type')
    typeObj = {}
    for i in typelist:
        if typeObj.get(i,-1) == -1:
            typeObj[i] = 1
        else:
            typeObj[i] += 1
    typeData = []
    for key,item in typeObj.items():
        typeData.append({
            'name':key,
            'value':item
        })
    return  typeData