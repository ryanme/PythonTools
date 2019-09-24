#!/usr/bin/env python
#!coding:utf-8
__author__ = 'Ryan'

"""
获取微博某条微博的所有回复信息
信息包括：用户名，设备，点赞数，内容，回复人ID，回复人头像URL，回复人微博主页URL
        默认采集用户名，设备，点赞数，内容，其他的看需要加减注释吧
其中，当内容包含消息体，则采集消息体，只有当纯emoji时，才采集emoji
"""

import requests, json
# 忽略requests关于https警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



class GetWeiboRefer():

    def __init__(self, id):
        self.id = id


    # 构造访问器，返回原始接口值
    def get_orign_content(self,url):
        # 获取评论 貌似不需要校验身份，需要的话再加cookies，chrome的network里随意查看接口返回的cookies贴过来就行，key:value格式对应即可
        # cookies = {}

        params = {
                'id':'4156138637306137',
                'page':'1'
                }

        headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
               }
        session = requests.session()
        try:
            res = session.get(url,data=params,headers=headers, verify=False, timeout=30)
            content = json.loads(res.content)
        except Exception as e:
            raise e
        return content

id = "4156138637306137"
url = "https://m.weibo.cn/api/comments/show?id=4156138637306137&page=1"
t = GetWeiboRefer(id)
res = t.get_orign_content(url)
for i in res['data']['hot_data']:
    print(i)

