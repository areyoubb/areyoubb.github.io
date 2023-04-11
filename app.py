from flask import Flask,request,render_template,session,redirect
from utils import query
from flask import flash
from tkinter import messagebox
import time
import sys
import re
from utils.getHomeData import *
from utils.getRate_tData import *
from utils.getType_tData import *
from utils.getActor_tData import *
from utils.word_cloud import *
app = Flask(__name__)
app.config['SECRET_KEY']='sfasf'
app.secret_key = 'this is session_key you know?'

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =='GET':
        return render_template('login.html')
    elif request.method =='POST':
        request.form = dict(request.form)
        ntype = list(request.form.keys())[0]
        if ntype=='username':
            def filter_fn(item):
                return request.form['username'] in item and request.form['pwd'] in item
            users = query.querys('select * from user',[],'select')
            filter_user = list(filter(filter_fn,users))
            if len(filter_user):
                session['username'] = request.form['username']
                return redirect('/home')
            else:
                return render_template("erro.html",message="输入的用户名或密码错误")

        elif ntype=='zcusername':
            if len(request.form['zcusername'])!=0 and len(request.form['pwd1'])!=0 :
                if request.form['pwd1'] != request.form['pwd2']:
                    return render_template('erro.html',message="两次密码不一致")
                def filter_fn(item):
                    return  request.form['zcusername'] in item
                users = query.querys('select * from user',[],'select')
                filter_list = list(filter(filter_fn,users))
                if len(filter_list):
                    return render_template('erro.html',message="该用户已被注册")
                else:
                    query.querys('insert into user(username,password) values (%s,%s)',[request.form['zcusername'],request.form['pwd1']])
                    flash('注册成功^v^，请登录')
                    return render_template('login.html')
            else:
                return render_template('erro.html',message="用户名和密码不能为空")

@app.route('/loginOut')
def loginOut():
    session.clear()
    return redirect('/login')

@app.route('/home',methods=['GET','POST'])
def home():
    username = session.get('username')
    maxMovieLen,maxRate,maxCasts,maxTypes,maxLang = getHomeData()
    typeEcharts = getTypesEchartsData()
    row,column = getRateEchats()
    tableData = getTableData()
    return render_template('index.html',username=username,
                           maxMovieLen=maxMovieLen,
                           maxRate=maxRate,
                           maxCasts=maxCasts,
                           maxTypes=maxTypes,
                           maxLang=maxLang,
                           typeEcharts=typeEcharts,
                           row=row,
                           column=column,
                           tableData=tableData
                           )





@app.route('/')
def allRequest():
    return  render_template('login.html')

@app.route('/rate_t/<type>',methods =['GET','POST'] )
def rate_t(type):
    username = session.get('username')
    typeList = getAllType()
    row,column = getAllRateDataByType(type)
    yearRow,yearColumns = getYearMean()
    if request.method == 'GET':
        searchName, scoreData = getStar('我不是药神')
    else:
        request.form = dict(request.form)
        searchName, scoreData = getStar(request.form['searchIpt'])
        if searchName == None:
            return render_template('erro.html',message='没有这个电影哦')
    return render_template('rate_t.html',
                           username = username,
                           typeList = typeList,
                           type = type,
                           row = row,
                           column = column,
                           searchName=searchName,
                           scoreData=scoreData,
                           yearRow = yearRow,
                           yearColumns = yearColumns)

@app.route('/type_t')
def type_t():
    username = session.get('username')
    typeData = getTypeDate()
    return render_template('type_t.html',
                           username=username,
                           typeData = typeData )

@app.route('/actor_t')
def actor_t():
    username = session.get('username')
    row,columns = getDirectorsDataTop()
    srow,scolumns = getstarsDataTop()
    return render_template('actor_t.html',
                           username = username,
                           row = row,
                           columns = columns,
                           srow=srow,
                           scolumns=scolumns)


@app.route('/comments_c',methods=['GET','POST'])
def comments_c():
    username = session.get('username')
    if request.method == 'GET':
        return render_template('comments_c.html',username=username)
    else:
        resSrc = getCommentImage(dict(request.form)['searchIpt'])

        return render_template('comments_c.html',username=username,resSrc = resSrc)

@app.route('/title_c')
def title_c():
    username = session.get('username')
    return render_template('title_c.html',
                           username=username)

@app.route('/star_c')
def star_c():
    username = session.get('username')
    return render_template('star_c.html',
                           username=username)

@app.before_request
def before_requre():
    pat = re.compile(r'^/static')
    if re.search(pat,request.path):
        return
    if request.path == '/login':
        return
    if request.path == '/':
        return
    username = session.get('username')
    if username:
        return
    return render_template('erro.html',message='你还没登陆哟')


if __name__ == '__main__':
    app.run()
