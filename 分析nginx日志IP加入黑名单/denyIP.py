#! coding:utf-8
import datetime
import linecache
import re

"""
nginx日志格式
46.161.9.44 - - [23/Jun/2017:03:17:37 +0800] "GET /bbs/forum.php?mod=forumdisplay&fid=2 HTTP/1.0" 200 48260 "http://aaaa.bbbbb.com/bbs/forum.php?mod=forumdisplay&fid=2" "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" "-"
46.161.9.44 - - [23/Jun/2017:03:17:39 +0800] "GET /bbs/forum.php?mod=forumdisplay&fid=2 HTTP/1.0" 200 46200 "http://aaaa.bbbbb.com/bbs/forum.php?mod=forumdisplay&fid=2" "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36" "-"
"""


def match_pattern(log_content):
    pattern = '(.*?)[(\d){4}:(\d){2}:(\d){2}:(\d){2}] - - \[(.*?) )\]'
    match = re.findall(pattern, log_content)
    return match[0]  # 因为遍历行，取第一个就行


# 运行，如果没有一个依据，那么每分钟的时间切片就太多了，可以以当前时间为准，往前推10分钟，搜集10分钟前到至今的所有SQL，
# 该脚本本身可放到crontab

def read_log(logPath):
    # 距今10分钟前的时间,datetime.datetime类型
    x_minutes_ago = (datetime.datetime.now()-datetime.timedelta(minutes=10))
    lines = linecache.getlines(logPath)
    oragin_list = []
    for line in lines:
        # 去除空行
        if not line.strip() == '':
            ip_and_time = match_pattern(line)
            ip = ip_and_time[0]
            time_temp1 = ip_and_time[1].splite(' ')[0]  # 去除后面的+800
            time_temp2 = conve_english_to_int_by_month(time_temp1)  # 将Jan等月份转换为数字月份
            log_time = datetime.datetime.strptime(time_temp2, '%d/%m/%Y:%H:%M:%S')  # 转换为datetime.datetime类型
            if log_time < x_minutes_ago:
                oragin_list.append(ip)
    linecache.clearcache()
    return oragin_list


def conve_english_to_int_by_month(time_info):
    month_english_and_int_dict = dict(Jan="01", Feb="02", Mar="03", Apr="04", May="05", June="06", July="07", Aug="08",
                                      Sept="09", Oct="10", Nov="11", Dec="12")
    month = time_info.split('/')[1]
    month_int = month_english_and_int_dict[month]
    time_info = time_info.replace(month, month_int)
    return time_info


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
    logPath = "E:\Python Project\\ryanme\PythonTools\分析nginx日志IP加入黑名单\log\\nginx.log"
    ips = read_log(logPath)
    deny_ips = deny_ip(ips)
    print(deny_ips)

