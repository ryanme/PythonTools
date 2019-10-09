# -*- coding: utf-8 -*-
# @Author  : guowr
# @Time    : 2017/6/15 21:08
import os

__author__ = 'Ryan'

'''
 下载某网站视频，视频用的索尼的.ts格式，需要先获取表单得到总的ts个数，然后再按名称合并成完整的视频。
 合并视频用到了ffmpeg
 下载视频使用的axel (linux ,mac平台)
'''


class DownloadAndConvertVideo(object):
    def __init__(self):
        self.mainFunc()

    def mainFunc(self):
        middle_url_list = [
            'http://example/xxx/xxx/index.m3u8',
        ]
        for url in middle_url_list:
            os.chdir('/Users/ryan/Documents/Python Project/Download_Sex_Video/')
            path_map = self.anlysis_path(url)
            full_project_path = path_map['full_project_path']
            document_name = path_map['document_name']
            m3u8_download_path = path_map['m3u8_download_path']
            list_path = path_map['list_path']
            ts_left_url = path_map['ts_left_url']
            key = path_map['key']
            if not os.path.exists(full_project_path+'/'+ document_name+'.mp4'):
                downloadList = self.downloadList(key, m3u8_download_path)
                self.mkdirListTxt(list_path, downloadList)
                self.downloadTs(downloadList, ts_left_url, document_name, full_project_path)


    def anlysis_path(self, middle_url):
        nowpath = os.getcwd()
        temp_list = middle_url.split('/')
        document_name = temp_list[3]
        key = temp_list[4]
        m3u8_name = temp_list[5]
        ts_left_url = middle_url.strip(m3u8_name)
        m3u8_download_path = nowpath + '/' + 'm3u8_document/'+ m3u8_name
        #urlretrieve(middle_url, m3u8_download_path)
        m3u8_download_command = '/usr/local/bin/axel -n 5 -o' + ' ' + '/Users/ryan/Documents/Python\ Project/Download_Sex_Video/m3u8_document/'+ m3u8_name + ' ' +middle_url
        os.system(m3u8_download_command)
        if not os.path.exists(m3u8_download_path):
            self.anlysis_path(middle_url)
        full_project_path = nowpath + '/' + document_name
        list_path = full_project_path + '/list.txt'
        if not os.path.exists(full_project_path):
            os.mkdir(full_project_path)
        path = {'m3u8_download_path':m3u8_download_path, 'full_project_path':full_project_path,
                'list_path':list_path, 'ts_left_url':ts_left_url,'key':key,'document_name':document_name}
        return path

    def downloadList(self, key, m3u8_download_path):
        fp = open(m3u8_download_path)
        temp = fp.read()
        temp2 = temp.split(',')
        will_be_down = []
        for ts_list in temp2:
            name = ts_list.split('\n')[1]
            if key in name:
                will_be_down.append(name)
        return will_be_down

    def mkdirListTxt(self, list_path, will_be_down):
        if os.path.exists(list_path):
            os.remove(list_path)
        for tt in will_be_down:
            f = open(list_path, 'a')
            f.write('file '+tt+'\n')
            f.close()

    def downloadTs(self, will_be_down, ts_left_url, document_name , full_project_path):
        miss_url = []
        for i in will_be_down:
            ts_url = ts_left_url + i
            ts_file_path = full_project_path + '/' + i
            if not os.path.exists(ts_file_path):
                #urlretrieve(ts_url, ts_file_path)
                down_command = '/usr/local/bin/axel -n 5 -o' + ' ' + '/Users/ryan/Documents/Python\ Project/Download_Sex_Video/' + document_name  + ' ' + ts_url
                os.system(down_command)
                if not os.path.exists(ts_file_path):
                    miss_url.append(i)
        if len(miss_url)>0:
            self.downloadTs(miss_url, ts_left_url, document_name, full_project_path)
        self.convert_video(full_project_path, document_name)

    def convert_video(self, full_project_path, document_name):
        convert_command = 'ffmpeg -f concat -i list.txt -acodec copy -vcodec copy -absf aac_adtstoasc ' + document_name + '.mp4'
        os.chdir(full_project_path)
        os.system(convert_command)


if __name__ == '__main__':
    DownloadAndConvertVideo()

# origin_path=os.getcwd() # 当前目录
# target_path = os.getcwd()+'/sex_videos'
# list = os.listdir(origin_path) # 当前目录下的文件
# for i in list:
#     if not i=='sex_videos':
#         second_path=origin_path+'/'+i
#         if os.path.isdir(second_path):
#           list2=os.listdir(second_path)  # 二层目录下的文件
#           for m in list2:
#             keyword=os.path.splitext(m)[1]
#             third_path = second_path + '/' + m
#             if keyword == '.ts' or keyword == '.m3u8' or keyword == '.txt':
#               os.remove(third_path)
#             if keyword == '.mp4':
#                 shutil.copyfile(third_path, target_path)

