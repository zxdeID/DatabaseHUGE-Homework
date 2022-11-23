from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#设置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@127.0.0.1:3306/medic'    
db = SQLAlchemy(app)


@app.route('/')
def welcome():
    s = '我的狗勾真的很可爱耶'
    return render_template('welcome.html',a = s)

@app.route('/index')
def dex():
    return render_template('login.html',msg = '请登录')

@app.route('/index/login',methods=['post'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    #啊这里暂时是想和数据库内所存储的数据比较的，但是还没弄hhh 先这样敷衍一下吧~或许有时间还可以加一下弄一下不同用户的权限？（好乱哦好像没说明白
    if username == 'buchangsheng' and password == 'mydogissocute':
        return '登录成功'
    else:
        return render_template('login.html',msg = '登录失败')

'''
从此往下的一大堆杂玩意就全是数据库部分的内容了，可在url后面加上/table_list进去查看
'''
#表名页
@app.route('/table_list')
def table_list():
    return render_template('table_list.html')

#选择展示某个表
@app.route('/choose')
def choose():
    choice = request.args.get("choice")
    if choice == "1":
        return select_disease_list()
    elif choice == "2":
        return select_disease_suffered()
    elif choice == "3":
        return select_edit_record()
    else:
        print(f"choice = {choice},type = {type(choice)}")
        return select_disease_list()

#定义模型
class DiseaseList(db.Model):
    #表模型
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    ifImg = db.Column(db.Integer)
    ifText = db.Column(db.Integer)
    lastEditTime = db.Column(db.Date)
    hid = db.Column(db.Integer)

#查询所有数据
@app.route("/select_disease_list")
def select_disease_list():
    Disease_List = DiseaseList.query.order_by(DiseaseList.id.desc()).all()
    return render_template("disease_list.html",disease_list = Disease_List)

#添加数据
@app.route('/insert_disease_list',methods=['GET','POST'])
def insert():
    #进行添加操作
    ifImg = request.form['ifImg']
    ifText = request.form['ifText']
    lastEditTime = request.form['lastEditTime']
    hid = request.form['hid']
    diseaseList = DiseaseList(ifImg=ifImg,ifText=ifText,lastEditTime=lastEditTime,hid=hid)
    db.session.add(diseaseList)
    db.session.commit()
    #添加完成重定向至主页
    return redirect('/table_list')

@app.route("/insert_page_disease_list")
def insert_page():
    #跳转至添加信息页面
    return render_template("disease_list_insert.html")


#删除数据
@app.route("/delete_disease_list",methods=['GET'])
def delete():
    #操作数据库得到目标数据，before_number表示删除之前的数量，after_name表示删除之后的数量
    id = request.args.get("id")
    diseaseList = DiseaseList.query.filter_by(id=id).first()
    db.session.delete(diseaseList)
    db.session.commit()
    return redirect('/table_list')

#修改操作
@app.route("/alter_disease_list",methods=['GET','POST'])
def alter():
    # 可以通过请求方式来改变处理该请求的具体操作
    # 比如用户访问/alter页面  如果通过GET请求则返回修改页面 如果通过POST请求则使用修改操作
    if request.method == 'GET':
    #进行添加操作
        id = request.args.get("id")
        ifImg = request.args.get("ifImg")
        ifText = request.args.get("ifText")
        lastEditTime = request.args.get("lastEditTime")
        hid = request.args.get("hid")
        diseaseList = DiseaseList(id=id,ifImg=ifImg,ifText=ifText,lastEditTime=lastEditTime,hid=hid)
        return render_template("disease_list_alter.html",diseaseList = diseaseList)
    else:
        #接收参数，修改数据
        id = request.form["id"]
        ifImg = request.form['ifImg']
        ifText = request.form['ifText']
        lastEditTime = request.form['lastEditTime']
        hid = request.form['hid']
        diseaseList = DiseaseList.query.filter_by(id=id).first()
        diseaseList.ifImg = ifImg
        diseaseList.ifText = ifText
        diseaseList.lastEditTime = lastEditTime
        diseaseList.hid = hid
        db.session.commit()
        return redirect('/table_list')

#定义模型
class DiseaseSuffered(db.Model):
    #表模型
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    hid = db.Column(db.Integer)
    diseaseGet = db.Column(db.String(255))
    time = db.Column(db.Date)

#查询所有数据
@app.route("/select_disease_suffered")
def select_disease_suffered():
    Disease_Suffered = DiseaseSuffered.query.order_by(DiseaseSuffered.id.desc()).all()
    return render_template("disease_suffered.html",disease_suffered = Disease_Suffered)

#添加数据
@app.route('/insert_disease_suffered',methods=['GET','POST'])
def insert_disease_suffered():
    #进行添加操作
    hid = request.form['hid']
    diseaseGet = request.form['diseaseGet']
    time = request.form['time']
    diseaseSuffered = DiseaseSuffered(hid=hid,diseaseGet=diseaseGet,time=time)
    db.session.add(diseaseSuffered)
    db.session.commit()
    #添加完成重定向至主页
    return redirect('/table_list')

@app.route("/insert_page_disease_suffered")
def insert_page_disease_suffered():
    #跳转至添加信息页面
    return render_template("disease_suffered_insert.html")


#删除数据
@app.route("/delete_disease_suffered",methods=['GET'])
def delete_disease_suffered():
    #操作数据库得到目标数据，before_number表示删除之前的数量，after_name表示删除之后的数量
    id = request.args.get("id")
    diseaseSuffered = DiseaseSuffered.query.filter_by(id=id).first()
    db.session.delete(diseaseSuffered)
    db.session.commit()
    return redirect('/table_list')

#修改操作
@app.route("/alter_disease_suffered",methods=['GET','POST'])
def alter_disease_suffered():
    # 可以通过请求方式来改变处理该请求的具体操作
    # 比如用户访问/alter页面  如果通过GET请求则返回修改页面 如果通过POST请求则使用修改操作
    if request.method == 'GET':
    #进行添加操作
        id = request.args.get("id")
        hid = request.args.get("hid")
        diseaseGet= request.args.get("diseaseGet")
        time = request.args.get("time")
        diseaseSuffered = DiseaseSuffered(id=id,hid=hid,diseaseGet=diseaseGet,time=time)
        return render_template("disease_suffered_alter.html",diseaseSuffered = diseaseSuffered)
    else:
        #接收参数，修改数据
        id = request.form["id"]
        hid = request.form['hid']
        diseaseGet = request.form['diseaseGet']
        time = request.form['time']
        diseaseSuffered = DiseaseSuffered.query.filter_by(id=id).first()
        diseaseSuffered.hid = hid
        diseaseSuffered.diseaseGet = diseaseGet
        diseaseSuffered.time = time
        db.session.commit()
        return redirect('/table_list')

#定义模型
class EditRecord(db.Model):
    #表模型
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.String(255))
    editor = db.Column(db.String(255))
    time = db.Column(db.Date)

#查询所有数据
@app.route("/select_edit_record")
def select_edit_record():
    Edit_Record = EditRecord.query.order_by(EditRecord.id.desc()).all()
    return render_template("edit_record.html",edit_record = Edit_Record)

#添加数据
@app.route('/insert_edit_record',methods=['GET','POST'])
def insert_edit_record():
    #进行添加操作
    content = request.form['content']
    editor = request.form['editor']
    time = request.form['time']
    editRecord = EditRecord(content=content,editor=editor,time=time)
    db.session.add(editRecord)
    db.session.commit()
    #添加完成重定向至主页
    return redirect('/table_list')

@app.route("/insert_page_edit_record")
def insert_page_edit_record():
    #跳转至添加信息页面
    return render_template("edit_record_insert.html")


#删除数据
@app.route("/delete_edit_record",methods=['GET'])
def delete_edit_record():
    #操作数据库得到目标数据，before_number表示删除之前的数量，after_name表示删除之后的数量
    id = request.args.get("id")
    editRecord = EditRecord.query.filter_by(id=id).first()
    db.session.delete(editRecord)
    db.session.commit()
    return redirect('/table_list')

#修改操作
@app.route("/alter_edit_record",methods=['GET','POST'])
def alter_edit_record():
    # 可以通过请求方式来改变处理该请求的具体操作
    # 比如用户访问/alter页面  如果通过GET请求则返回修改页面 如果通过POST请求则使用修改操作
    if request.method == 'GET':
    #进行添加操作
        id = request.args.get("id")
        content = request.args.get("content")
        editor= request.args.get("editor")
        time = request.args.get("time")
        editRecord = EditRecord(id=id,content=content,editor=editor,time=time)
        return render_template("edit_record_alter.html",editRecord = editRecord)
    else:
        #接收参数，修改数据
        id = request.form["id"]
        content = request.form['content']
        editor = request.form['editor']
        time = request.form['time']
        editRecord = EditRecord.query.filter_by(id=id).first()
        editRecord.content = content
        editRecord.editor = editor
        editRecord.time = time
        db.session.commit()
        return redirect('/table_list')

if __name__ == '__main__':
    app.run(debug = True,port=5000)



