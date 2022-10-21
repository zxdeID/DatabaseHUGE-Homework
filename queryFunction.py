import os
import pymysql
import time

def query1(db):
    '''
    给定疾病名称，查询疾病数据贡献来源的人所患有的所有疾病
    db:拦截的书库
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
    pass

def query3(db):
    pass

def query4(db):
    pass

def query5(db):
    pass

def query6(db):
    pass




