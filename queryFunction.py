import os
import pymysql
import time

def query1(db):
    '''
    给定疾病名称，查询疾病数据贡献来源的人所患有的所有疾病（基于集合操作）
    '''
    os.system('cls')
    dise = input('请输入疾病名称:\n')
    sql = '''
    这一个作用是给定某人的id查询它患有的所有的疾病
    select P.hid, D.diseaseGet
    from people P, disease_suffered D
    where P.hid = D.hid
    '''

    pass

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




