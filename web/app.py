from flask import Flask,render_template,request

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(port=8080)



