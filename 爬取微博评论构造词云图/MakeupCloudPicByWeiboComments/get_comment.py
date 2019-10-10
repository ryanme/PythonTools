#!/usr/bin/env python
# !coding:utf-8
__author__ = 'Ryan'

"""
获取微博某条微博的所有回复信息
信息包括：用户名，设备，点赞数，内容，回复人ID，回复人头像URL，回复人微博主页URL
        默认采集用户名，设备，点赞数，内容，其他的看需要加减注释吧
其中，当内容包含消息体，则采集消息体，只有当纯emoji时，才采集emoji
"""
# reload(sys)
# sys.setdefaultencoding('utf-8')
import requests, json, math
from lxml import etree
# 忽略requests关于https警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# reload(sys)
# sys.setdefaultencoding('utf-8')
import json
import math
import requests
from lxml import etree
# 忽略requests关于https警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class GetWeiboRefer():

    def __init__(self, id):
        self.id = id

    # 得到所有分页地址
    def make_url(self, id):
        if type(id) == int:
            left = "https://m.weibo.cn/api/comments/show?id=" + str(id) + "&page="
        elif type(id) == str:
            left = "https://m.weibo.cn/api/comments/show?id=" + id + "&page="
        else:
            return '请传正确的id!'
        default_url = "https://m.weibo.cn/api/comments/show?id=" + id + "&page=1"
        res = self.get_orign_content(default_url)
        # 微博total_number是所有评论，然而经过验证，总评论可能少于这个数，猜错是部分评论被删除，这个变量没减去删除的评论数
        total_numbers = res['total_number']
        url_list = []
        # 微博每个单页返回的条数不固定，首页收录了热评，返回的正常条数不足10条，其他页没有热评的时候有时候8-10条都有可能
        # 所以这里先不去计算一共多少页，给一个假设值，最大页数。遍历的时候判断下，当调到无评论的页（接口只返回一个OK）的时候，跳出遍历即可。
        max_page_num = int(total_numbers) / 9.0
        if max_page_num < 1:
            max_page_num = 1
        else:
            max_page_num = int(math.ceil(max_page_num))  # 向上取整,再转换为int
        for i in range(1, max_page_num):
            url = left + str(i)
            url_list.append(url)
        return url_list

    # 构造访问器，返回原始接口值
    def get_orign_content(self, url):
        # 获取评论 貌似不需要校验身份，需要的话再加cookies，chrome的network里随意查看接口返回的cookies贴过来就行，key:value格式对应即可
        # cookies = {}

        params = {
            'id': '4156138637306137',
            'page': '1'
        }

        headers = {'content-type': 'application/json',
                   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
                   }
        session = requests.session()
        try:
            res = session.get(url, data=params, headers=headers, verify=False, timeout=30)
            content = json.loads(res.content)
        except Exception as e:
            raise e
        return content

    # 处理返回值，有内容返回内容，无内容纯emoji则返回emoji
    def make_refer(self, refer):
        selector = etree.HTML(refer, parser=etree.HTMLParser(encoding='utf-8'))
        tempinfo = selector.xpath('string(.)')
        refer = tempinfo.replace('\n', '').replace(' ', '')
        if refer == '':
            content = selector.xpath('//span[@class="url-icon"]')
            for i in range(0, len(content)):
                childrens = content[i].getchildren()  # span下的<img>标签
                for j in range(0, len(childrens)):
                    children = childrens[j]
                    emj = children.get('alt')
                    refer = str(refer) + str(emj)
        return refer

    # 构造自定义格式信息格式[{'name':'用户名','source':'设备','content':'回复内容'}]
    def make_res_list(self, content):
        try:
            content_data = content['data']
            refer_info_list = []
            for i in range(0, len(content_data)):
                refer_info_dict = {}
                refer_info_dict['name'] = content_data[i]['user']['screen_name']  # 用户名
                # refer_info_dict['userid']= content_data[i]['user']['id'] # 回复人的user id，方便后续进一步爬数据
                # refer_info_dict['profile_image_url'] = content_data['user']['profile_image_url'] # 回复人头像地址
                # refer_info_dict['profile_url'] = content_data['user']['profile_url'] # 回复人微博主页地址
                refer_info_dict['source'] = content_data[i]['source']  # 设备
                refer_info_dict['content'] = self.make_refer(content_data[i]['text'])  # 回复内容
                refer_info_dict['like'] = str(content_data[i]['like_counts'])  # 点赞数
                refer_info_list.append(refer_info_dict)
            return refer_info_list
        except Exception as e:
            # 没有获取到['data']则表示已经获取到最后一页了，不需要继续
            return 0

    # 遍历page list，得到所有信息
    def all_refer(self):
        id = self.id
        all_list = self.make_url(id)  # 得到所有页码列表
        full_list = []
        for i in all_list:
            orign_content = self.get_orign_content(i)  # 原始值
            temp_list = self.make_res_list(orign_content)  # 单页按照预订格式处理后的list
            if temp_list == 0:  # 0是make_res_list得知已经爬到最后一页了没有回复的时候返回的，上面方法定义
                return full_list  # 无更多评论了，则返回
            else:
                full_list.extend(temp_list)
        return full_list

# 调用方法
# t = GetWeiboRefer('4156152113716396')
# refer_info_list =t.all_refer()
# for i in refer_info_list:
#     print '用户:'+i['name'] + ' 使用:' + i['source'] + ' 点赞数:' + i['like'] + ' 回复:'+ i['content']
