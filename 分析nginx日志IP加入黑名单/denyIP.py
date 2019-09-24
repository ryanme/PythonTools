#! coding:utf-8

import linecache
import re

__author__ = 'Ryan'

"""
公司服务器，经常被别人攻击，要写个监控nginx日志的脚本，每分钟运行一次，如果这一分钟内同一个ip请求次数超过200次，加入黑名单，nginx日志每一行的格式如下：

46.161.9.44 - - [23/Jun/2017:03:17:37 +0800] "GET /bbs/forum.php?mod=forumdisplay&fid=2 HTTP/1.0" 200 48260 "http://aaaa.bbbbb.com/bbs/forum.php?mod=forumdisplay&fid=2" "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" "-"
46.161.9.44 - - [23/Jun/2017:03:17:39 +0800] "GET /bbs/forum.php?mod=forumdisplay&fid=2 HTTP/1.0" 200 46200 "http://aaaa.bbbbb.com/bbs/forum.php?mod=forumdisplay&fid=2" "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" "-"

"""

def match_ip(line):
    ipPattern = '^(\d){1,3}.(\d){1,3}.(\d){1,3}.(\d){1,3}'
    match = re.match(ipPattern, line)
    if match:
        return match.group()

def match_time(line):
    timePattern = '(\d){4}:(\d){2}:(\d){2}:(\d){2}'
    match = re.search(timePattern, line)
    if match:
        return match.group()


# 运行，如果没有一个依据，那么每分钟的时间切片就太多了，可以以当前时间为准，



def read_log(logPath):
    lines = linecache.getlines(logPath)
    oragin_list = []
    for line in lines:
        # 去除空行
        if not line.strip() == '':
            tempDict = {}
            ip = match_ip(line)
            time = match_time(line)
            tempDict[0] = ip
            tempDict[1] = time
            oragin_list.append(tempDict)
    linecache.clearcache()
    return oragin_list

def deny_ip(ips):

    temp_list = []
    temp_dict = {}

    deny_ip_list = []
    for i in ips:
        ip = i[0]
        if ip not in temp_list:
            temp_list.append(ip)
            temp_dict[ip] = 1
        else:
            temp_dict[ip] = temp_dict[ip] + 1

    keys_list = list(temp_dict.keys())
    values_list = list(temp_dict.values())

    for num in range(0, len(temp_list)):
        if values_list[num] >= 10:
            deny_ip_list.append(keys_list[num])
    return deny_ip_list


if __name__ == '__main__':
    logPath = "D:\Python Project\TestDemo\log\\nginx.log"
    ips = read_log(logPath)
    deny_ips = deny_ip(ips)
    print(deny_ips)



