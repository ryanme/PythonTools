#/usr/bin/env python3
#coding:utf8


import xlrd
import os
import pymysql
from xlwt import *


__author__ = 'Ryan'

'''
对比数据库里和Excel里的数据，获取相同id的情况下，其他信息不一致的条数(这里是公司名字)
'''

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

def select(code):
    data = "select t.chiname from bnd_basicinfo t where t.TRADINGCODE='" + code + "'"
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(data)
    rerults = cursor.fetchall()
    conn.close()
    return rerults[0][0]

# 数据库配置
def get_conn():
    mysql_dev_host = '192.168.1.110'
    mysql_dev_port = 3306
    mysql_dev_user = 'test'
    mysql_dev_passwd = 'test'
    mysql_dev_db = 'testdb'
    conn  = pymysql.connect(
        host=mysql_dev_host,
        port=mysql_dev_port,
        user=mysql_dev_user,
        passwd=mysql_dev_passwd,
        db=mysql_dev_db)
    return conn

def read_excel():
    ExcelFile=xlrd.open_workbook(r'D:\Users\ryan\Desktop\test.xlsx') # 读取文件
    sheet=ExcelFile.sheet_by_index(0) # 第一个sheet
    nrows = sheet.nrows # 行数
    # 指定file以utf-8的格式打开
    file = Workbook(encoding='utf-8')
    # 指定打开的文件名
    table = file.add_sheet('对比公司信息')
    table.write(0, 0, '公司code')
    table.write(0, 1, 'Excel里公司名字')
    table.write(0, 2, '数据库里公司名字')

    for i in range(1, nrows): # 遍历行
        codecontent = sheet.cell(i,0).value.encode('utf-8')
        code = codecontent.split('.')[0]
        chiname = sheet.cell(i,1).value.encode('utf-8')
        namefromsql = select(code)
        # 打印公司名可能不一致的,这里是粗略判断，得出的值还需要在进行确认下
        if chiname in namefromsql:
            pass
        else:
            print('第' + str(i) + '行: 公司code:' + str(code) + ' , Excel: ' + str(chiname) + ', 数据库: ' + str(
                namefromsql) + '')
        #print '第'+str(i)+'行: 公司code:'+str(code)+' , Excel: '+str(chiname)+', 数据库: '+str(namefromsql)+''
        table.write(i,0,code)
        table.write(i,1,chiname)
        table.write(i,2 ,namefromsql)
    file.save('D:\Users\ryan\Desktop\CompanyNameCompare.xls') # 比对结果保存为excel


if __name__ =='__main__':
    read_excel()
