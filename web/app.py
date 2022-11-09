from flask import Flask,render_template,request

app = Flask(__name__)

@app.route('/')
def welcome():
    s = '我的狗勾真的很可爱耶'
    return render_template('welcome.html',a = s)


@app.route('/user/')
def users():
    return 'user!'

'''
@app.route('/<name>')
def who(name):
    return "hey,%s"%name
'''
if __name__ == '__main__':
    app.run(port=8080)



