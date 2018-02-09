#!/usr/bin/python
#encoding:utf-8

__author__ = 'Ryan'

"""
比较两个nginx配置文件的差异,生成html
"""

import difflib
import sys

try:
    # textfile1 = "/Users/ryan/jinght1402429109.sql";
    # textfile2 = "/Users/ryan/std_config.sql";
    textfile1=sys.argv[1]
    textfile2=sys.argv[2]
except Exception,e:
    print "Error:"+str(e)
    print "Usage: diffNginxConf.py filename1 filename2"
    sys.exit()


def readfile(filename):  #文件读取分隔函数
    try:
        fileHandle = open(filename,'rb')
        text=fileHandle.read().splitlines()   #读取后进行分隔
        fileHandle.close()
        return text
    except IOError as error:
        print ('Read file Error:'+str(error))
        sys.exit()

if textfile1=="" or textfile2=="":
    print "Usage: diffNginxConf.py filename1 filename2"
    sys.exit()

text1_lines = readfile(textfile1)    #调用readfile函数,获取分隔符后的字符串
text2_lines = readfile(textfile2)

d=difflib.HtmlDiff()            #创建HtmlDiff()类对象
print d.make_file(text1_lines,text2_lines)     #通过make_file 方法输出HTML格式的对比结果

