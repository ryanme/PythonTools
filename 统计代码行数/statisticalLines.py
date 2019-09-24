# coding:utf-8

import os
import re

__author__ = 'Ryan'

'''
不知不觉你已经写了很多python代码了，代码全部都放在e盘下面的my_code文件夹中，突然突发奇想，想统计了一下总共写了多少行代码，包括空行和注释，
要把代码的行数、空行数、注释行数都统计出来。

我不是win环境，这里目录就用我当前目录了
'''


def get_files(DirPath):
    FileList = os.listdir(DirePath)
    pattern = r'^(\S)+.py$'
    PyFileList = []

    for i in FileList:
        if re.search(pattern, i) and i != '__init__.py':
            PyFileList.append(i)

    return PyFileList


def statistical(filePath):
    print(filePath)
    codeline = 0
    expline = 0
    blankline = 0
    fp =open(filePath, encoding='utf8')
    while fp.tell()!=os.path.getsize(filePath):
        try:
            temp = fp.readline()
            print (temp)
            if temp.startswith('#'):
                expline += 1
                print (expline)
            elif temp == '/n':
                blankline += 1
                print (blankline)
            elif temp.startswith(''''''''):
                expline += 1
                print (expline)
                while True:
                    temp = fp.readline()
                    expline += 1
                    print (expline)
                    if temp.endswith('''''''/n'):
                        break
                else:
                    codeline += 1
            else:
                print('the codingline is: ' + str(codeline))
                print('the expline is: ' + str(expline))
                print('the blankline is: ' + str(blankline))
        except Exception as e:
            raise e
    fp.close()


DirePath = os.getcwd()  # 我不是win环境，这里目录就用我当前目录了,DirePath这个可以直接指定
FileList = get_files(DirePath)
# for file in FileList:
#     filePath = DirePath+'/'+str(file)
#     print(file)
#     statistical(filePath)


def temp(path):
    totallines = 0
    blocklines = 0
    explines = 0
    codelines = 0
    fp = open(path, encoding='utf8')
    for line in fp.readlines():
        totallines += 1
        if line.startswith('#'):
            blocklines += 1
        elif line.startswith('/n'):
            explines += 1
        elif line.startswith(''''''''):
            blocklines += 1
            if line.endswith('''''''/n'):
                break
            # while True:
            #     temp = fp.readline()
            #     explines += 1
            #     print(explines)
            #     if temp.endswith('\''''):
            #         print('xxxxxxxxxx')
            #         break
        else:
            codelines += 1
    print ('totallines: %s, blocklines: %s, explines: %s, codelines: %s',(totallines, blocklines, explines, codelines))


temp('E:\Python Project\TestDemo\Sum_of_OnetoHundred.py')
