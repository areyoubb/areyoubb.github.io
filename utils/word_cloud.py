from .utils import *
import sys
sys.path.append('..')
from ciyun import *
import json

def getCommentImage(searchIpt):
    searchName = list(df1.loc[df1['name'].str.contains(searchIpt)]['name'])[0]
    comments = str(df1[df1['name'] == searchIpt ]['content'].values).strip("[]'")

    reSrc = getimg(comments)
    return reSrc