# -*- encoding:utf-8 -*-
import os

import jieba.analyse
import matplotlib.pyplot as plt
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator

__author__ = 'Ryan'

'''
生成词云图
'''

if __name__ == "__main__":
    # FONT_PATH = os.environ.get("FONT_PATH", os.path.join(os.path.dirname(__file__), "simhei.ttf"))
    # mpl.rcParams['font.sans-serif'] = ['Hei']

    content = open("comments.txt", "rb").read()

    tags = jieba.analyse.extract_tags(content, topK=100, withWeight=False)
    text = " ".join(tags)
    text1 = unicode(text)

    nowpath = os.getcwd()
    trump_coloring = imread(os.path.join(nowpath, "huge.png"))
    wc1 = WordCloud(font_path='/System/Library/fonts/PingFang.ttc',  # 设置字体
                    background_color="white",  # 背景颜色
                    max_words=300,  # 词云显示的最大词数
                    mask=trump_coloring,  # 设置背景图片
                    max_font_size=40,  # 字体最大值
                    random_state=42, )

    # 生成词云
    wc2 = wc1.generate(text1)

    # 从背景图片生成颜色值
    image_colors = ImageColorGenerator(trump_coloring)

    # 以下代码显示图片
    plt.imshow(wc2)
    plt.axis("off")
    plt.show()
    # 保存图片
    wc2.to_file(os.path.join(nowpath, "weibo2.png"))
