# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 08:30:47 2021

@author: toshi
"""
#20211020
#健康管理アプリサンプル
from flask import Flask
from flask import render_template,request,redirect,jsonify
#from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timedelta
#import pytz
import os

#from PIL import Image
#別クラスのインポート
from Predict import Predict
from Energy import Energy


app = Flask(__name__)

#日本語ラベル（料理名）
dishname_ja={
        'curry':'カレー',
        'cabbageroll':'ロールキャベツ',
        'croquettes':'コロッケ',
        'gyoza':'餃子',
        'gyudon':'牛丼',
        'hamburg':'ハンバーグ',
        'karaage':'唐揚げ',
        'naporitan':'ナポリタン',
        'nikujaga':'肉じゃが',
        'omletrice':'オムライス',
        'oyakodon':'親子丼',
        'steak':'ステーキ',
        'tonkatsu':'とんかつ',
        'lettucesalad':'レタスサラダ',
        'yakisoba':'焼きそば',
        'bibinba':'ビビンバ',
        'grilledfish':'焼き魚',
        'harusamesalad':'春雨サラダ',
        'misosoup':'味噌汁',
        'potatosalad':'ポテトサラダ',
        }
c=Energy()
pred=Predict()







#登録されている全ての日の料理名を取得する（カレンダーに表示させる用）
def getEvents():
    events=[]
    #temp=c.userDataList
    for data in c.userDataList:
        events.append([data[0].replace('/','-'),dishname_ja[data[2]]])
    return events

def getWeekCal():
    weekCal=[]
    date=datetime.now()
    d=date-timedelta(days=6)
    for i in range(7):
        dstr=d.strftime("%Y/%m/%d")
        weekCal.append(c.getEnergyData(c.getDay(dstr))[0])
        d=d+timedelta(days=1)
    return weekCal
	
def get_key_from_value(d, val):
    keys = [k for k, v in d.items() if v == val][0]
    print(keys)
    return keys

#ホーム画面
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')
#カレンダー
@app.route('/calendar',methods=['GET','POST'])
def calendar():
    events=getEvents()
    return render_template('calendar.html',events=events)



#カレンダーで選択した日付の記録を取得
@app.route('/view_record/<id>',methods=['GET','POST'])
def view_record(id):
    day=id.replace('-','/')
    posts=c.getDay(day)
    dishdata=c.dishData
    return render_template('view_record.html',id=id,posts=posts,
						   dishdata=dishdata,dishname_ja=dishname_ja)

#画像選択追加画面
@app.route('/select/<id>',methods=['GET','POST'])
def select(id,c=c,pred=pred):
    if request.files and 'picfile'in request.files:
        f=request.files['picfile']
        f.save('pred_img/'+f.filename)
        img_name=f.filename
        output=pred.predict(img_name)
        re_label=c.dishLabel[output]
        os.remove('pred_img/'+img_name)
        pred=dishname_ja[re_label]
        confidence='confidence'
        data=dict(pred=pred,confidence=confidence)
        return jsonify(data)
    elif request.form and 'meal_time' in request.form:
        if request.form['dishname']=='' or not(request.files['fileField']):
            return render_template('select.html',id=id)
        title=get_key_from_value(dishname_ja,request.form['dishname'])
        if not(title in dishname_ja.keys()):#規定の料理以外は登録不可
            return render_template('select.html',id=id)
        start=id
        #日付表示、'-'を'/'に変換
        start=start.replace('-','/')
        meal_time=request.form['meal_time']
        #dish_id=make_id(str(start),meal_time)
        f=request.files['fileField']
        filepath='user_dish_img/'+f.filename
        f.save(filepath)

        #start(日付)meal_time(朝、昼、夜、他)title(料理名)
        c.postUserData(start,str(meal_time),title)
        
        return redirect('/')
        
    return render_template('select.html',id=id)



#グラフ画面（摂取カロリー）&リコメンド画面
@app.route('/view_data',methods=['GET','POST'])
def chart():
    weekCal=getWeekCal()
    c.OverAndShortEnergy()
    recommend_dish=c.recommendDish()
    weekList=c.getWeekList()
    print(weekList)
    return render_template('view_data.html',weekCal=weekCal,
						   recommend_dish=recommend_dish,dishname_ja=dishname_ja,weekList=weekList)



if __name__=='__main__':
    app.run(debug=True)
