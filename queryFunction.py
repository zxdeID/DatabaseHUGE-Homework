import os
import pymysql
import time

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
    pass

def query4(db):
    pass

def query5(db):
    pass

def query6(db):
    pass




