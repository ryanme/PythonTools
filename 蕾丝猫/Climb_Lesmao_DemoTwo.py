# coding=utf8
from __future__ import unicode_literals

import os
import re
import socket
import urllib
import requests
import MySQLdb
from bs4 import BeautifulSoup
import requests

__author__ = 'Ryan'

'''
下载蕾丝猫图片，按写真集归档
URL存于数据库
'''


# 通用连接方法
def create_conn():
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='3862441ll',
        db='lesmao',
        charset='utf8'
    )
    return conn


# 通用response
def get_response(url):
    send_headers = {
        'Host': 'www.lesmao.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive'
    }
    while True:
        try:
            response = requests.get(url=url, headers=send_headers).text
            return response
        except socket.error:
            continue


# 插入page地址
def insert_page_urls():
    left_url = 'http://www.lesmao.com/portal.php?page='
    conn = create_conn()
    cur = conn.cursor()
    for right_nums in range(1, 114):
        url = left_url + str(right_nums)
        sql = "insert into pages_url values(%s,%s,%s)"
        cur.execute(sql, (right_nums, url, 0))
        conn.commit()
    cur.close()
    conn.close()


# 计算张数,得到单张专辑有几页
def excute_url_nums(firsturl):
    res = get_response(firsturl)
    soup = BeautifulSoup(res, 'html.parser', from_encoding='utf-8')
    try:
        res = soup.find('div', class_='picvip').get_text()
        temp_img_num = int(re.search(r'\d+', res).group(0))
    except:
        pattern = re.compile(r'\d+')
        temp = soup.find('div', class_='thread-down-data').find('span').next_sibling
        temp_img_num = int(pattern.match(temp).group())
    temp_num_a = temp_img_num / 5
    temp_num_b = temp_img_num % 5
    img_nums = temp_num_a + temp_num_b
    return img_nums


# 传入page那页url,得到所有链接和标题
def get_pages_allurls(pageurl):
    firsturls = []
    res = get_response(pageurl)
    soup = BeautifulSoup(res, 'html.parser', from_encoding='utf-8')
    res_data = soup.find_all('div', class_='title')
    for x in res_data:
        firsturls.append(x.a['href'])
    return firsturls


# 传入首页获得标题
def get_title(url):
    res_data = get_response(url)
    soup = BeautifulSoup(res_data, 'html.parser', from_encoding='utf-8')
    try:
        title = soup.find('div', id='thread-title').find('h1').get_text()
    except:
        try:
            title = soup.find('div', class_='thread-down-c').find('h2').get_text()
        except:
            title = None
    return title


# 得到总的pages页地址
def get_firsturl(id):
    conn = create_conn()
    cur = conn.cursor()
    get_url = 'select url from pages_url where is_download=0 and id=%s' % id
    cur.execute(get_url)
    url = cur.fetchone()[0]
    return url


# 传入首页和页数得到某一专辑所有网址
def get_all_urls(nums, frist_url):
    full_urls=[]
    patten = re.compile(r'http://www.lesmao.com/thread-\d+')
    left = patten.match(frist_url).group()
    for right_num in range(1, nums+1):
        right_url =str(right_num)+'-1.html'
        full_url=left+'-'+right_url
        full_urls.append(full_url)
    return full_urls


# 向数据库插入标题,标题id与pages_url关联
def insert_title(id):
    pageurl = get_firsturl(id)
    allurls = get_pages_allurls(pageurl)
    conn = create_conn()
    cur = conn.cursor()
    num = 1
    for firsturl in allurls:
        title = get_title(firsturl)
        if(title==None):
            pass
        else:
            pages = excute_url_nums(firsturl)
            sql = "insert into titles_url(title, has_pages, start_url, id, is_download) values (%s, %s, %s, %s, %s);"
            temp = (title, pages, str(firsturl), id, 0)
            try:
                cur.execute(sql, temp)
                conn.commit()
                print('Query OK,The num is %s,' % num)
                num = num + 1
            except Exception as e:
                print(e)


# 向数据库插入图片地址
def insert_img_url(title, firsturl, nums):
    conn = create_conn()
    cur = conn.cursor()
    all_url = get_all_urls(nums, firsturl)
    for url in all_url:
        res = get_response(url)
        soup = BeautifulSoup(res, 'html.parser', from_encoding='utf-8')
        imgs = soup.find_all('img', src=re.compile(r'\d+/\d+_\d+_\w+_\d+_\d+.jpg'))
        for img in imgs:
            img_url = img['src']
            sql = "insert into img_url(title,url,is_download) values(%s, %s, %s)"
            try:
                cur.execute(sql, (title, img_url, 0))
                conn.commit()
                print("%s插入成功" % img_url)
            except Exception as e:
                print(e)
    cur.close()
    conn.close()


# 每次从库里获取一个url去获取图片链接调用insert_img_url保存到库里
def select_title_url():
    conn = create_conn()
    while True:
        cur = conn.cursor()
        sql = "select title, start_url, has_pages from titles_url where is_download=0 limit 1;"
        cur.execute(sql)
        temp = cur.fetchone()
        title = temp[0]
        frist_url = temp[1]
        nums = temp[2]
        try:
            insert_img_url(title, frist_url, nums)
            sql2 = "update titles_url set is_download=1 where start_url=%s;"
            cur.execute(sql2, (frist_url,))
            conn.commit()
            cur.close()
        except Exception as e:
            print(e)
    conn.close()


# 判断图片存不存在
def check(path ,img_urls, title):
    conn = create_conn()
    cur = conn.cursor()
    update_state1 = "update img_url set is_download=1 where url=%s;"
    for x in img_urls:
        img_url = str(x[0])
        pattern = re.compile('\d+_\d+_\S+_\d+_\d+.jpg')
        img_name = pattern.search(img_url).group()
        img_path = path+'/'+img_name
        if not os.path.exists(img_path):
            try:
                img_body = requests.get(img_url).content
                with open(img_path, 'wb') as img_file:
                    img_file.write(img_body)
                print('保存%s成功' % img_path)
            except Exception as e:
                print(e)
        else:
            print('%s已存在' % img_path)
        cur.execute(update_state1, (img_url, ))
    cur.close()
    conn.close()


# 从标题库每次取一个标题,然后去图片路径库匹配找出改标题下的所以图片路径下载到指定目录
def save_img_tolocal():
    xpath = '/Users/ryan/Documents/lsm'
    title_sql = "select title from titles_url where is_download=1 limit 1;"
    img_sql = "select url from img_url where title=%s and is_download=0;"
    update_state2 = "update titles_url set is_download=2 where title=%s;"
    conn = create_conn()
    cur = conn.cursor()
    while True:
        cur.execute(title_sql)
        title = cur.fetchone()[0]
        path = xpath+'/' + title
        cur.execute(img_sql, (title,))
        img_urls = cur.fetchall()
        if not os.path.exists(path):
            os.mkdir(path)
            print('创建目录%s成功' % path)
        else:
            print('目录%s已存在' % path)
        check(path, img_urls, title)
        cur.execute(update_state2, (title, ))
        conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    save_img_tolocal()