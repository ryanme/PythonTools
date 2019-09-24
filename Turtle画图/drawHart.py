# coding:utf-8


import time
import turtle as tt

import pygame

file = 'D:\个人简介.mp3'   # mp3 的路径
pygame.mixer.init() # 初始化音频
# track = pygame.mixer.music.load(file)  # 载入音乐文件
pygame.mixer.music.play()  # 开始播放

tt.title('dalao 带带我')  # 设置标题栏文字
tt.hideturtle()  # 隐藏箭头
tt.getscreen().bgcolor('#f0f0f0')  # 背景色
tt.color('#c1e6c6', 'red')  # 设置画线颜色、填充颜色，可以直接写 green，
tt.pensize(2)  # 笔的大小
tt.speed(2)  # 图形绘制的速度,1~10
tt.up()  # 移动，不画线
tt.goto(0, -150)


tt.down() # 移动，画线
tt.begin_fill() # 开始填充
tt.goto(0, -150)
tt.goto(-175.12, -8.59)
tt.left(140)
pos = []
for i in range(19):
    tt.right(10)
    tt.forward(20)
    pos.append((-tt.pos()[0], tt.pos()[1]))
for item in pos[::-1]:
    tt.goto(item)
tt.goto(175.12, -8.59)
tt.goto(0, -150)
tt.left(50)
tt.end_fill()  # 结束填充，显示填充效果


tt.color("black") # 设置颜色
tt.up()
tt.goto(0,220)
tt.write("大佬，带带我~", font=(u"方正舒体", 36, "normal"), align="center")
tt.goto(200, -250)
tt.write('by ryan', font=(u"方正舒体", 10, "bold"))
time.sleep(10)  # 画完后再播放 10 秒音乐，可以修改时间
pygame.mixer.music.fadeout(100)  # 停止播放
tt.done()