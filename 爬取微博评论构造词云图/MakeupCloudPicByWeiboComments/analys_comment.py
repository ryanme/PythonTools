#!/usr/bin/env python
#!coding:utf-8
__author__ = 'Ryan'

import os

from PythonCrawler.MakeupCloudPicByWeiboComments.get_comment import GetWeiboRefer

t = GetWeiboRefer('4154417035431509')
refer_info_list =t.all_refer()
comment_list = []
for i in refer_info_list:
    comment_list.append(i['content'])
now_path = os.getcwd()
filepath = os.path.join(now_path,'comments.txt')
fp = open('comments.txt','wa')
for i in comment_list:
    fp.writelines(i+'\n')
fp.close()
