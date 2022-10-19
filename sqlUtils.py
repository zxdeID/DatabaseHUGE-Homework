from sqlite3 import SQLITE_ANALYZE
from unittest import result
import pymysql
import os
import time

def showColumns(db,tableName):
    '''
    返回表中列的名称和数据类型
    db:连接的数据库
    tableName:表名
    '''
    cursor = db.cursor()
    sql = "show columns from {}".format(tableName)
    cursor.execute(sql)
    columns = cursor.fetchall()
    ls = []
    for col in columns:
        ls.append((col[0],col[1]))
    return ls


def showTables(db,op):
    '''
    这个函数用于展示当前数据库中的表，并返回用户选择的表名
    db:连接的数据库
    op:对表的操作，如修改或者查询
    '''
    os.system('cls')
    cursor = db.cursor()
    sql = 'show tables'
    cursor.execute(sql)
    tables = cursor.fetchall()
    print('    -------------------------------------\n')
    print('    请选择您要进行{}的表'.format(op))
    for id,i in enumerate (tables):
        print('    ',id+1,i[0])
    print('    -------------------------------------\n')
    j = eval(input())
    os.system('cls')
    return tables[j-1][0]

def showTable(db,tableName):
    '''
    打印表内内内容
    db:连接的数据库
    tableName:要打印的表的名称
    '''
    cursor = db.cursor()
    sql = 'select * from {}'.format(tableName)
    cursor.execute(sql)
    values = cursor.fetchall()
    columnName = showColumns(db,tableName)
    print("{:-^50}".format(tableName))
    for j in columnName:
        print(j[0],end='\t\t')
    print('')
    for i in values:
        for k in i:
            print('{}'.format(k),end='\t\t')
        print('')
    print("{:-^50}".format(''))
    return