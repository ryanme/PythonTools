# -*- coding: utf-8 -*-
# @Author  : guowr
# @Time    : 2019/8/21 10:29
import asyncio
import aiohttp
import requests
import re
import os


class DownloadTsAndMerge:

    def __init__(self):
        self.ts_url = "https://example.com"
        self.headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
        self.full_file_path = self.check_directory()

    @staticmethod
    def check_directory():
        """
        检查目录，如果不存在就创建，最后返回路径
        :param path_name:    directory name
        :return:
        """
        download_path = os.path.dirname(os.path.realpath(__file__)) + '\\ts_download\\'
        if not os.path.exists(download_path):
            os.mkdir(download_path)
        return download_path

    def remove_ts_and_txt(self, list_txt_path):
        """
        合并完成后，删除ts和txt文件
        :param list_txt_path:
        :return:
        """
        f_list = os.listdir(self.full_file_path)
        try:
            for fileNAME in f_list:
                if os.path.splitext(fileNAME)[1] == '.ts':
                    os.remove(self.full_file_path + '\\' + fileNAME)
            os.remove(list_txt_path)
            return True
        except Exception as e:
            print("删除文件失败: {0}".format(str(e)))
            return False

    def get_ts_list(self, m3u8_url):
        """
        下载m3u8，分析得到ts文件
        :param m3u8_url:
        :return:
        """
        res = requests.get(m3u8_url, headers=self.headers)
        # pattern = re.compile(r'index_.*.ts')
        pattern = re.compile(r'/.*')
        m = pattern.findall(res.text)
        print("一共 %s 个" % str(len(m)))
        return m

    async def download_ts(self, sem, ts, list_txt_path):
        """
        异步下载ts，通过sem控制协程数量
        :param sem:
        :param ts:
        :param list_txt_path:
        :return:
        """
        async with sem:
            async with aiohttp.ClientSession() as session:
                full_ts_url = self.ts_url + ts
                ts_name = ts.split('/')[-1]
                f = open(list_txt_path, 'a')
                f.write('file ' + ts_name + '\n')
                f.close()
                downloadfile = os.path.join(self.full_file_path, ts_name)
                if not os.path.exists(downloadfile):
                    async with session.get(full_ts_url, headers=self.headers) as response:
                        content = response.content
                        chunk_size = content.total_bytes
                        await self.write_to_local(downloadfile, content, chunk_size)
                        return True
                return True

    async def write_to_local(self, downloadfile, content, chunk_size):
        """
        ts文件保存到本地
        :param downloadfile:
        :param content:
        :param chunk_size:
        :return:
        """
        # 普通bytes类型写入方法
        # with open(downloadfile, 'wb') as fileHandler:
        #     print("{0} download finishe".format(downloadfile))
        #     fileHandler.write(content)  # ts文件写入到本地
        # return True

        # aiohttp.streams.StreamReader写入方法
        with open(downloadfile, 'wb') as fd:
            while True:
                chunk = await content.read(chunk_size)
                if not chunk:
                    break
                fd.write(chunk)
                print("{0} 写入完成".format(downloadfile))

    def merge_ts_to_mp4(self, video_name):
        """
        合并ts文件为mp4格式，COPY命令不知道为什么只有音频,改用ffmpeg
        :param full_file_path:
        :return:
        """
        try:
            print("开始组合资源...")
            convert_command = 'ffmpeg -f concat -i '+video_name+'.txt -acodec copy -vcodec copy -absf aac_adtstoasc ' + video_name + '.mp4'
            os.chdir(self.full_file_path)
            os.system(convert_command)
            return True
        except Exception as e:
            return False

    def start(self, m3u8_url, video_name):
        """
        开始
        :param m3u8_url:
        :param video_name:
        :return:
        """
        m = self.get_ts_list(m3u8_url)
        list_txt_path = self.full_file_path+"\\"+video_name+".txt"
        sem = asyncio.Semaphore(5)  # 限制协程数量
        tasks = [asyncio.ensure_future(self.download_ts(sem, ts, list_txt_path)) for ts in m]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        print("%s is download over" % video_name)
        # 这里为了支持批量下载，loop不要手动close
        if self.merge_ts_to_mp4(video_name):    # 合并
            print("合并成功")
        else:
            print("合并失败")

        if self.remove_ts_and_txt(list_txt_path):
            print("删除下载文件成功")
        else:
            print("删除下载文件失败")


if __name__ == "__main__":
    # value是视频名称，记住不要有空格，否则ffmpeg重命名的时候会报错
    file_dict = {
        # "https://example.com/xxx/xxx/index.m3u8": "xxxxxxxxxx"
        }
    dtm = DownloadTsAndMerge()
    for m3u8_url in file_dict:
        video_name = file_dict[m3u8_url]
        dtm.start(m3u8_url, video_name)