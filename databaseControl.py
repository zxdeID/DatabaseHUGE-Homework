import time
import traceback
import pymysql
import os
from sqlUtils import *

def begin():
    os.system('cls')
    state = 0
    while state == 0:
        usrname = input('请输入用户名:\n')
        passwd = input('请输入密码:\n')
        db,state = login(usrname,passwd)
    mainloop(db)

def login(usrname,passwd):
    state = 0
    try:
        db = pymysql.connect(
            user=usrname,
            password=passwd,
            port=3306,
            host='127.0.0.1',
            database='medic',
            charset = 'utf8'
            )
        state = 1
        print('登陆成功！')
        time.sleep(1)
        return db,state
    except:
        print('连接失败！')
        return -1,state

def mainloop(db):
    choice = 0
    tips = '''
    -------------------------------------\n
    欢迎使用xxx医疗数据库
    请选择您要进行的操作：
    1.查询数据
    2.增添数据
    3.删除数据
    4.修改数据
    5.退出
    -------------------------------------\n
    '''
    while choice !=5:
        os.system('cls')
        print(tips)
        choice  = eval(input('请选择:\n'))
        if choice == 1:
            cha()

        elif choice == 2:
            zeng(db)

        elif choice == 3:
            shan(db)

        elif choice == 4:
            gai(db)

        else:
            os.system('cls')
            print('再见！')
            time.sleep(1)
            db.close()
            exit()
    
def zeng(db):
    '''
    基本功能实现了
    还有需要补充的功能：程序自动补充id避免id重复
    '''  
    os.system('cls')
    tableName = showTables(db,'修改')
    os.system('cls')
    columnName = showColumns(db,tableName)
    nums = len(columnName)  
    for q in columnName:
        print(q[0],end='\t\t')
    newData = input("\n表内有{}列数据，请您输入{}项，各项之间用空格分隔\n".format(nums,nums))
    dataLs = newData.split(' ')
    datas = ''
    columns = ''
    for id,col in enumerate(columnName):
        columns += col[0]
        columns += ','
        if col[1] == 'int(11)':
            datas += dataLs[id]
            datas += ','
        elif col[1] == 'text' or col[1] == 'date':
            datas += "'{}'".format(dataLs[id])
            datas += ','
    
    cursor = db.cursor()
    try:
        sql = '''insert into {} ({}) values ({})'''.format(tableName,columns[:-1],datas[:-1])
        cursor.execute(sql)
        db.commit()     
        print('您成功对{}进行了修改'.format(tableName))
        time.sleep(3)
    except:
        print('修改失败！')
        traceback.print_exc()
        time.sleep(3)
    cursor.close()
    return

def shan(db):
    '''
    基本功能实现了
    还有需要补充的功能：当表空时提示表空，删除时确认id是否在其中
    '''                                               
    os.system('cls')
    tableName = showTables(db,'修改')
    showTable(db,tableName)
    key = input('请输入您要删除的行所含有的id:\n')
    sql = 'delete from {} where id = {}'.format(tableName,key)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
        print('您成功对{}进行了修改'.format(tableName))
        time.sleep(3)
    except:
        print('删除失败！')
        traceback.print_exc()
        time.sleep(3)
    cursor.close()
    return

def gai(db):
    '''
    基本功能实现了
    还没想到有啥bug
    '''
    os.system('cls')
    tableName = showTables(db,'修改')
    cols = showColumns(db,tableName)
    showTable(db,tableName)
    chng = input('请输入您要修改的数据的行号和列号,以空格分隔:\n').split(' ')
    newdt = input('请输入修改后的新内容:\n')
    if cols[eval(chng[1])-1] == 'int(11)':
        pass
    else:
        newdt = "'"+newdt+"'"
    sql = 'update {} set {}={} where id={}'.format(tableName,cols[eval(chng[1])-1][0],newdt,chng[0])
    cursor = db.cursor()

    try:
        cursor.execute(sql)
        db.commit()
        print('修改成功！')
        time.sleep(3)
    except:
        print('修改失败！')
        traceback.print_exc()
        time.sleep(30)
    cursor.close()
    return

def cha():
    os.system('cls')
    print('查询操作维护中')
    time.sleep(1)
    return
        
if __name__ == '__main__':
    os.system('cls')
    begin()