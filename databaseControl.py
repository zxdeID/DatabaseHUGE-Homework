import time
import traceback
import pymysql
import os
from sqlUtils import *
from queryFunction import *

def begin():
    state = 0
    while state == 0:
        os.system('cls')
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
        time.sleep(3)
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
            cha(db)

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
    还有需要补充的功能：程序自动补充id避免id重复，在增添新项后按照id对各项进行排序
    '''  
    os.system('cls')
    tableName = showTables(db,'修改')
    os.system('cls')
    columnName = showColumns(db,tableName)
    nums = len(columnName)  
    for q in columnName[1:]:
        print(q[0],end='\t\t')
    newData = input("\n表内有{}列数据，请您输入{}项，各项之间用空格分隔\n".format(nums-1,nums-1))
    dataLs = newData.split(' ')
    datas = ''
    columns = ''
    for id,col in enumerate(columnName):
        if id == 0:
            continue
        columns += col[0]
        columns += ','
        if col[1] == 'int(11)' or col[1] == 'int(11) unsigned':
            datas += dataLs[id-1]
            datas += ','
        elif col[1] == 'text' or col[1] == 'date' or col[1] == 'datetime':
            datas += "'{}'".format(dataLs[id-1])
            datas += ','
    
    cursor = db.cursor()
    try:
        sql = '''insert into {} ({}) values ({})'''.format(tableName,columns[:-1],datas[:-1])
        cursor.execute(sql)
        db.commit()     
        print('您成功对{}进行了修改'.format(tableName))
        time.sleep(3)
    except:
        print('修改失败！10秒钟后退出！')
        print(sql)
        traceback.print_exc()
        time.sleep(1000)
    cursor.close()
    return

def shan(db):
    '''
    基本功能实现了
    '''                                               
    os.system('cls')
    notIn = True
    bo = False  
    while not bo:       #当表空时
        tableName = showTables(db,'修改')
        dic, bo = showTable(db,tableName)

    while notIn:        #当表id不对时
        key = eval(input('请输入您要删除的行所含有的id:\n'))
        for i in dic:
            if i == key:
                notIn = False
        print("输入id有误，请重试！")
        time.sleep(3)
        os.system('cls')
        dic, bo = showTable(db,tableName)

    sql = 'delete from {} where id = {}'.format(tableName,dic(key))
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
    # tableName = showTables(db,'修改')
    # dic,bo = showTable(db,tableName)
    bo = False
    while not bo:       #当表空时
        tableName = showTables(db,'修改')
        dic, bo = showTable(db,tableName)
    notOk = True
    while   notOk:  #当列数或者行数不对时
        cols = showColumns(db,tableName)
        col_nums = len(cols)    #列数
        ids = len(dic)
        range_col = range(1,col_nums+1)
        range_id = range(1,ids+1)
        chng = input('请输入您要修改的数据的行号和列号,以空格分隔:\n').split(' ')
        if eval(chng[0]) in range_id and eval(chng[1]) in range_col:
            notOk = False
        else:
            print("行号或列号范围有误！3秒后返回！")
            time.sleep(3)
            os.system('cls')
            dic, bo = showTable(db,tableName)

    newdt = input('请输入修改后的新内容:\n')
    if cols[eval(chng[1])-1] == 'int(11)':
        pass
    else:
        newdt = "'"+newdt+"'"
    sql = 'update {} set {}={} where id={}'.format(tableName,cols[eval(chng[1])-1][0],newdt,dic[eval(chng[0])])
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

def cha(db):
    txt = '''
    -------------------------------------\n
    请选择您要进行的查询操作：
    1.给定疾病名称，查询疾病数据贡献来源的人所患有的所有疾病
    2.给定疾病名称，查询疾病来源地
    3.给定疾病，查询该疾病的患病人数
    4.给定疾病，查询患有该病的患者的平均年龄
    5.给定年龄或职业 查找患者患有的疾病有哪些
    6.给定修改人查询修改时间和修改内容
    7.给定疾病名称，查询病人的职业
    8.给定疾病名称，查询提供疾病资料的人的遗传病史
    9.返回上一级菜单
    -------------------------------------\n
    请输入您要选择的选项：\n    
    '''
    choice = -1
    while choice != 7:
        os.system('cls')
        print(txt)
        choice = eval(input())
        if choice == 1:
            query1(db)
        elif choice == 2:
            query2(db)
        elif choice == 3:
            query3(db)
        elif choice == 4:
           query4(db)
        elif choice == 5:
           query5(db)
        elif choice == 6:
           query6(db)
        elif choice == 7:
           query7(db)
        elif choice == 8:
           query8(db)
        elif choice == 9:
           return
        else:
            print("请键入1-9内的数字！")
            time.sleep(3)
    return
        
if __name__ == '__main__':
    os.system('cls')
    begin()