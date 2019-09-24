# -*- coding: utf-8 -*-
# @Author  : guowr
# @Time    : 2019/8/21 10:29

import requests
import re
import os

heads = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}
ts_url = "https://2.ddyunbo.com/"

def check_directory():
    """
    检查目录，如果不存在就创建，最后返回路径
    :param path_name:    directory name
    :return:
    """
    download_path = os.path.dirname(os.path.realpath(__file__)) + '\\..\\ts_download\\'
    # full_file_path = download_path + path_name
    # if not os.path.exists(full_file_path):
    #     os.mkdir(full_file_path)
    # return full_file_path
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    return download_path


def get_ts_list(m3u8_url):
    """
    下载m3u8，分析得到ts文件
    :param path_name:
    :return:
    """
    # url = ts_url + path_name
    res = requests.get(m3u8_url, headers=heads)
    pattern = re.compile(r'index_.*.ts')
    m = pattern.findall(res.text)
    print("一共 %s 个" % str(len(m)))
    return m


async def download_ts(ts, ts_url, full_file_path):
    """
    下载ts文件
    :param ts:
    :param full_file_path:
    :return:
    """
    # ts_url = ""
    full_ts_url = ts_url + str(ts)
    res_body = requests.get(full_ts_url, headers=heads).content
    downloadfile = os.path.join(full_file_path, ts)
    with open(downloadfile, 'wb') as fileHandler:
        print("download %s" % ts)
        fileHandler.write(res_body)  # ts文件写入到本地


def merge_ts_to_mp4(full_file_path, path_name):
    """
    合并ts文件为mp4
    :param full_file_path:
    :return:
    """
    try:
        print("开始组合资源...")
        # CMD下  copy/b  E:\temps\*.ts  E:\temps\new.ts
        exec_str = r'copy /b "' + full_file_path + r'*.ts" "' + full_file_path + path_name + '.mp4"'
        os.system(exec_str)  # 使用cmd命令将资源整合
        # exec_str = r'del "' + full_file_path + r'*.ts"'
        # os.system(exec_str)  # 删除原来的文件
        print("资源组合成功!")
    except Exception as e:
        print("资源组合失败")


def main():
    """
    主方法
    :return:
    """
    m3u8_url="https://2.ddyunbo.com/20190823/RiVzH1jp//800kb/hls/index.m3u8"
    ts_url = " https://2.ddyunbo.com/"
    path_name = "index.m3u8"
    m = get_ts_list(m3u8_url)
    full_file_path = check_directory()
    for ts in m:
        download_ts(ts, ts_url, full_file_path)
    # 合并
    merge_ts_to_mp4(full_file_path, path_name)
    print("%s is download over" % path_name)

main()