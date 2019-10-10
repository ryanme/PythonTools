#!/usr/bin/env python3
#-*-coding:utf-8-*-__

__author__ = 'Ryan'

import requests, os, math
from urllib3 import request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

'''
下载一个人所有发过的微博的图片
i['text']是发过的文字，若要用到，自行拓展
cookies 填写自己的cookies
可以把uid提前准备好
'''


class Get_All_Weibo:

    def __init__(self ,uid):
        self.uid = uid
        self.cookies = {}
        self.total = self.total_weibo_nums(uid)
        self.total_page = self.make_pages(self.total)
        print('共有'+str(self.total_page)+'页')
        self.containerid = self.origin_first_request(uid)['containerid']  # 得到containerid
        self.screen_name = self.origin_first_request(uid)['screen_name']  # 得到用户名，用于创建目录

    # 获取微博页containerid以及发过的微博总数,从这里得到了containerid
    def origin_first_request(self, uid):
        left_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value='
        url = left_url + str(uid)
        headers = {
            'Content-Type':'application/json; charset=utf-8'}
        res = requests.get(url=url,cookies=self.cookies,headers=headers)
        res = res.json()['data']
        containerid = res['tabsInfo']['tabs'][1]['containerid']
        screen_name = res['userInfo']['screen_name']
        user_map = {'containerid':containerid, 'screen_name':screen_name }
        return user_map

    # 得到发过的微博总数
    def total_weibo_nums(self, uid):
        contained = self.origin_first_request(uid)['containerid']
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value='+str(uid)+'&containerid='+str(contained)+'&page=1'
        weibo_request = self.weibo_request(url)['data']
        total_weibo_nums = int(weibo_request['cardlistInfo']['total'])
        return total_weibo_nums

    # 计算得到请求的pages最大值
    def make_pages(self, total):
        if (total%10.0==0):
            pages = int(total/10)
        else:
            pages = int(math.ceil(total/10.0))
        return pages

    # 构造获request请求
    def weibo_request(self, url):
        headers = {
            'Content-Type':'application/json; charset=utf-8'}
        res = requests.get(url=url,cookies=self.cookies,headers=headers)
        res = res.json()
        return res

    # 创建文件夹
    def create_folder(self, screen_name):
        nowpath = os.getcwd()
        path = nowpath + '\\' + screen_name  # 拼接目录
        if not os.path.exists(path):  # 目录存在就不建立，不存在就创建
            os.mkdir(path)
        return path # 返回完整文件夹路径

    # 循环调用方法。
    def get_all_pages(self, uid, page=1, t=0, imgNums=0):
        path = self.create_folder(self.screen_name)  # 创建目录，有则返回，没有则创建在返回完整目录
        left_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value='+str(uid)+'&containerid='+str(self.containerid)+'&page='
        url = left_url + str(page)
        weibo_request = self.weibo_request(url)['data']
        dict_cards = weibo_request['cards']
        print('开始下载第'+str(page)+'页.......')
        for i in dict_cards:
            if i['card_type'] == 9:  # 类型9是原创微博
                t = int(t) + 1  # 累加发过的微博数
                try: # 有的纯文本的，没有i['mblog']['pics']，使用try
                    for n in i['mblog']['pics']:  # 图片是有多张的
                        img_url = str(n['large']['url'])  # 得到图片地址
                        imgNums = imgNums + 1
                        self.save_to_path(path, img_url)  # 保存图片
                except:
                    pass
        print('第'+str(page)+'页下载完毕,当前累计下载'+str(t)+'条')
        if int(page) == int(self.total_page): # 所有page都下载好,跳出循环
            print('*'*30)
            print ('用户' + str(self.screen_name) + '的图片下载完毕。用户微博总数'+str(self.total)+'条，其中原创微博'+str(t)+'条,共下载图片'+str(imgNums)+'张。')
        else:
            page = int(page) + 1  # 当还没到总数，继续累加页数
            self.get_all_pages(uid, page, t, imgNums)  # 调用自身，传回页数和发过的微博累加数，拉取新的页内容

    # 保存图片
    def save_to_path(self, path, img_url):
        temp_list = img_url.split('/')
        img_name = temp_list[len(temp_list)-1]  # 得到原始文件名
        full_img_path = path + '\\' + str(img_name)
        res = requests.get(img_url)
        if not os.path.exists(full_img_path):  # 已有则不保存
            with open(full_img_path, 'wb') as file:
                file.write(res.content)
            # request.urlretrieve(img_url, full_img_path) #py3
            print('The download of '+str(img_name) +' is completed ! ')


f = open('uid.txt')
uid_list = f.readlines()
for uid in uid_list:
    print('开始uid为'+str(uid))
    t = Get_All_Weibo(uid)
    t.get_all_pages(uid)
os._exit(0)