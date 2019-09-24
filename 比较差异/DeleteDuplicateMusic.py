# coding: utf-8

import os

"""
比对两个目录音乐文件，删除其中一个文件夹中名字相同的
"""

music_path = "E:/Users\\ryan\Music\音乐\Music"
netease_music_path = "E:/Users\\ryan\Music\音乐\音乐"


def get_name_list(music_path):
    list = os.listdir(music_path)
    music_name_list = []
    for line in list:
        templist = line.split('.')
        if len(templist) == 2:
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
            # os.remove(refer_music_path)
            print(refer_music_path)


# if __name__ == "__main__":
    # music_name_list1 = get_name_list(music_path)
    # music_name_list2 = get_name_list(netease_music_path)
    # music_name_list = music_name_list1 + music_name_list2
    #
    # a = {}
    # for i in music_name_list:
    #     if music_name_list.count(i) > 1:
    #         a[i] = music_name_list.count(i)
    # for i in a:
    #     delete_duplicate_music(i)

import time
import datetime
timeStamp = 1563724800
timeArray = time.localtime(timeStamp)
otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
print(otherStyleTime)
# # 使用datetime
# timeStamp = 1381419600
# dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
# otherStyleTime = dateArray.strftime("%Y--%m--%d %H:%M:%S")
# print(otherStyleTime)
