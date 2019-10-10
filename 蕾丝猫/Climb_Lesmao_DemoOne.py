# coding:utf-8
import re
import os
import requests
from bs4 import BeautifulSoup


'''
下载蕾丝猫图片，不入库
'''


# 从首页开始获取写真链接
def getAllLinks():
    oriUrl = 'http://www.lesmao.com/portal.php?page='
    alllinks = []
    for i in range(0, 1):
        realUrl = oriUrl+str(i)
        response = requests.get(realUrl).text
        soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')
        links = soup.find_all('a', href=re.compile(r'http://www.lesmao.com/thread-\d+-\d+-\d+.html'))
        # 去重
        links = list(set(links))
        for link in links:
            alllinks.append(link)
        alllinks = list(set(alllinks))
    return alllinks


# 通用方法一次请求返回标题和页数
def vivistUrl(firstUrl):
    response = requests.get(firstUrl).text
    soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')
    links = soup.find_all('a', href=re.compile(r'http://www.lesmao.com/\w+-\d+-\d+-\d+.html'))
    title = soup.find_all('a', href=firstUrl)
    return links, title


# 获取总页数
def getPageLength(firstUrl):
    links = vivistUrl(firstUrl)[0]
    pages = 0
    for link in links:
        if(link.get_text()):
            pages = link.get_text()
        else:
            continue
    return pages


# 获取标题
def saveToLocal(firstUrl):
    title = vivistUrl(firstUrl)[1]
    if len(title) == 1:
        title = title[0].get_text()
    return title


# 在本地创建文件,存在则不创建
def createDocument(firstUrl):
    filepath = '/Users/ryan/Documents/python-crawler/lesmao/'
    title = saveToLocal(firstUrl)
    # 切割
    nameSplit = title.split(' ')
    # 外层文件夹名字
    documentName = nameSplit[0].encode('utf-8')
    # 写真文件夹名
    if len(nameSplit)==4:
        secondName = (nameSplit[1] + nameSplit[3]).encode('utf-8')
    elif len(nameSplit)==7:
        secondName = (nameSplit[2] + nameSplit[1] + nameSplit[4] + nameSplit[5]).encode('utf-8')
    elif len(nameSplit) == 3:
        secondName = (nameSplit[1] + nameSplit[2]).encode('utf-8')
    elif len(nameSplit) == 2:
        secondName = (nameSplit[0]).encode('utf-8')
    else:
        secondName = (nameSplit[2] + nameSplit[1] + nameSplit[4]).encode('utf-8')
    # 拼接目录
    path = os.path.join(os.path.join(filepath, documentName), secondName)
    isExists = os.path.exists(path)
    if not isExists:
        print(path + ' 创建成功')
        os.makedirs(path)
    else:
        pass
    return path

def savePictures(firstUrl):
    alllinks = getAllLinks()
    pages = range(1, int(getPageLength(firstUrl)))
    for x in alllinks:
        path = createDocument(x['href'])
        for y in pages:
            strinfo = re.compile('\d+-1.html')
            after = str(y)+'-1.html'
            b = strinfo.sub(str(x['href']), after)
            url2 = b
            response2 = requests.get(url2).text
            soup2 = BeautifulSoup(response2, 'html.parser', from_encoding='utf-8')
            imgs = soup2.find_all('img', src=re.compile(r'\d+/\d+_\d+_\w+_\d+_\d+.jpg'))

            for img in imgs:
                img_name = re.search('\d+_\d+_\w+_\d+_\d+.jpg', img['src']).group()
                imgPath = os.path.join(path, img_name.encode('utf-8'))
                exist = os.path.exists(imgPath)
                if exist:
                    print(imgPath + "已存在")
                else:
                    # 按原文件名命名保存
                    try:
                        img_body = requests.get(img['src']).text
                        with open(imgPath, 'wb') as file:
                            file.write(img_body)
                        print(imgPath + "保存成功")
                    except Exception as e:
                        print(e)
                        continue


if __name__ == "__main__":
    allUrls = getAllLinks()
    for firstUrl in allUrls:
        firstUrl = firstUrl['href']
        savePictures(firstUrl)

