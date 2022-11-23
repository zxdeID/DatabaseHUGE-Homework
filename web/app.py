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


#定义模型
class DiseaseList(db.Model):
    #表模型
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    ifImg = db.Column(db.Integer)
    ifText = db.Column(db.Integer)
    lastEditTime = db.Column(db.Date)
    hid = db.Column(db.Integer)

@app.route('/table_list')
def table_list():
    return render_template('table_list.html')

@app.route('/choose')
def choose():
    choice = request.args.get("choice")
    if choice == "1":
        return selectAll()
    else:
        print(f"choice = {choice},type = {type(choice)}")
        return selectAll()
    # return selectAll()


#查询所有数据
@app.route("/select")
def selectAll():
    Disease_List = DiseaseList.query.order_by(DiseaseList.id.desc()).all()
    return render_template("disease_list.html",disease_list = Disease_List)

#添加数据
@app.route('/insert',methods=['GET','POST'])
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
    return redirect('/')

@app.route("/insert_page")
def insert_page():
    #跳转至添加信息页面
    return render_template("disease_list_insert.html")


#删除数据
@app.route("/delete",methods=['GET'])
def delete():
    #操作数据库得到目标数据，before_number表示删除之前的数量，after_name表示删除之后的数量
    id = request.args.get("id")
    diseaseList = DiseaseList.query.filter_by(id=id).first()
    db.session.delete(diseaseList)
    db.session.commit()
    return redirect('/')

#修改操作
@app.route("/alter",methods=['GET','POST'])
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
        print(f"id = {id}")
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
        return redirect('/')

if __name__ == '__main__':
    app.run(port=5000)



