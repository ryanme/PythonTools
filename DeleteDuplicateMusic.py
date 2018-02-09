#/usr/bin/env python3
#coding:utf8

import os

__author__ = 'Ryan'

"""
比对两个目录音乐文件，删除其中一个文件夹中名字相同的
"""

music_path = u'/Users/ryan/Music/音乐'
netease_music_path = u'/Users/ryan/Music/网易云音乐'

def get_name_list(music_path):
    list = os.listdir(music_path)
    music_name_list = []
    for line in list:
        templist=line.split('.')
        if len(templist)==2:
            name = templist[0]
        else:
            name = ','
            tempnamelist = templist[:-1]
            name = name.join(tempnamelist)
        music_name_list.append(name)
    return music_name_list

def delete_duplicate_music(musicname):
    list = os.listdir(music_path)
    music_name_list = []
    for line in list:
        if musicname in line:
            refer_music_path = os.path.join(music_path, line)
            os.remove(refer_music_path)

music_name_list1 = get_name_list(music_path)
music_name_list2 = get_name_list(netease_music_path)
music_name_list = music_name_list1 + music_name_list2

a = {}
for i in music_name_list:
  if music_name_list.count(i)>1:
    a[i] = music_name_list.count(i)
for i in a:
    delete_duplicate_music(i)
