import os
import pymysql
import time
from sqlUtils import *
import traceback


def query1(db):
    '''
    给定疾病名称，查询疾病数据贡献来源的人所患有的所有疾病
    db:连接的数据库
    小bug：没有排除空结果
    '''
    os.system('cls')
    dise = input('请输入疾病名称:\n')
    cursor = db.cursor()
    sql = '''
    select P.hid,D.diseaseGet
    from people P, disease_suffered D
    where P.hid = D.hid and P.hid in
    (select B.hid
    from disease_list B
    where B.name = '{}'
    )
    '''.format(dise)
    cursor.execute(sql)
    ret = cursor.fetchall()
    os.system('cls')
    print('hid\t\tdisease')
    for i in ret:
        print(i[0],'\t\t',i[1])
    a = input('输入任意键回车返回上一级菜单')
    return

def query2(db):
    '''
    给定疾病名称，查询疾病来源地
    db:连接的数据库
    小bug：没有排除空结果
    '''
    os.system('cls')
    dise = input('请输入疾病名称:\n')
    cursor = db.cursor()
    sql = '''
    select P.address
    from people P
    where exists
    (select *
    from disease_list B
    where B.name = '{}' and B.hid = P.hid
    )
    '''.format(dise)
    cursor.execute(sql)
    ret = cursor.fetchall()
    os.system('cls')
    print('address')
    for i in ret:
        print(i[0])
    a = input('输入任意键回车返回上一级菜单')
    return

def query3(db):
    '''
    给定疾病，查询该疾病的患病人数
    db:连接的数据库
    小bug：也没有考虑空结果
    之前的想法要实现略有些麻烦，于是做了点改变（如果脑子还能活下来，就再试试看之前的想法）
    '''
    os.system('cls')
    dise = input('请输入疾病名称:\n')
    cursor = db.cursor()
    sql = '''
    select COUNT(*) AS scount
    from disease_suffered D, people P
    where D.diseaseGet = '{}' and D.hid = P.hid
    '''.format(dise)
    cursor.execute(sql)
    ret = cursor.fetchall()
    os.system('cls')
    print('the number of patients:{}'.format(ret))
    a = input('输入任意键回车返回上一级菜单')
    return

def query4(db):
    '''
    给定疾病，查询患有该病的患者的平均年龄
    db:连接的数据库
    小bug:依旧没排除空结果
    '''
    os.system('cls')
    dise = input('请输入疾病名称:\n')
    cursor = db.cursor()
    sql = '''
    select AVG(P.age)
    from people P
    where exists
    (select *
    from disease_list DL
    where DL.name = '{}' and DL.hid = P.hid
    )
    '''.format(dise)
    cursor.execute(sql)
    ret = cursor.fetchall()
    os.system('cls')
    print('average age:{}'.format(ret))
    a = input('输入任意键回车返回上一级菜单')
    return

def query5(db):
    '''
    给定年龄或职业 查找患者患有的疾病有哪些
    db:连接的数据库
    '''
    os.system('cls')
    # tableName = showTables(db, '查询')
    # cols = showColumns(db, tableName)
    # showTable(db, tableName)

    print("请输入要查询的职业：")
    data_work = input()
    print("请输入要查询的年龄：")
    data_age = eval(input())

    cursor = db.cursor()  # 获 取 游 标
    sql = '''
    Select diseaseGet\
    from people disease_suffered\
    where people.hid=disease_suffered.hid and people.age={}\
    intersect\
    select diseaseGet\
    from people disease_suffered\
    where people.hid=disease_suffered.hid and people.work='{}'\
    '''.format(data_age,data_work)
    print(sql)

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for a in result:
            print(f"该条件下患者患有的疾病有:{a}\n")
    except:
        print('查询失败')
        traceback.print_exc()
        time.sleep(30)
        # 关闭光标对象
        cursor.close()
    return

def query6(db):
    pass


