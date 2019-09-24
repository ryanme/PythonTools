# -*- coding: utf-8 -*-
# @Author  : guowr
# @Time    : 2019/9/18 1:09
#
import requests
# from bs4 import BeautifulSoup


def download_img():
    url = "https://9uu22.com/pic/201909/9-7/A-005/"
    for i in range(20, 21):
        if i<10:
            nums = '0'+str(i)+'.jpg'
        else:
            nums = str(i)+'.jpg'
        ttt = url + nums
        content = requests.get(ttt).content
        with open(nums, 'wb') as file:
            file.write(content)


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
req_url = "https://9uu.com/picture/detail?id=8670"
"https://9uu.com/picture/detail?id=6899"
chrome_options=Options()
#设置chrome浏览器无界面模式
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(chrome_options=chrome_options)
# 开始请求
browser.get(req_url)
#打印页面源代码
print(browser.page_source)
#关闭浏览器
browser.close()
#关闭chreomedriver进程


# url = "https://9uu.com/picture/detail?id=8670"
#
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"}
#
# res = requests.get(url,headers=headers).content
# # title
# xpath='//body//div[@class="info-text size_s"]/p[1]/text()'
#
# img='//body//img[@class="bg_important ng-star-inserted"]["src"]'
#
# soup = BeautifulSoup(res, 'lxml')
# title = soup.select_one("div.info-text")
# print(title)
# print(dir(title))