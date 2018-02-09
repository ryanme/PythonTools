#!/usr/bin/env python3
# encoding:utf-8
from wxpy import *
import time

__author__ = 'Ryan'

'''
msg.type
Text  文本
Picture 图片包括动图
Video   视频
Sharing 分享包括收藏
Map     地图，位置
Card    名片
Recording   语音信息
'''
# 实例化,console_qr=True表示在控制台打印二维码
bot = Bot(console_qr=True)
#bot = Bot(console_qr=False, cache_path=True) # 启用缓存，保存登陆状
tuling = Tuling(api_key='')  # 这里填写你的图灵机器人id，需要申请

addfriend_request = '加好友'  #自动添加好友的条件
@bot.register(msg_types=FRIENDS, enabled=True)
# 自动接受验证信息中包含 'wxpy' 的好友请求
def auto_accept_friends(msg):
    # 判断好友请求中的验证文本
    if addfriend_request in msg.text.lower():
        # 接受好友 (msg.card 为该请求的用户对象)
        new_friend = bot.accept_friend(msg.card)
        # 或 new_friend = msg.card.accept()
        # 向新的好友发送消息
        new_friend.send('机器人自动接受了你的请求,你可以任意回复获取功能菜单，若机器人没回复菜单则表明机器人尚未工作，请等待')

# 回复发送给自己的消息，可以使用这个方法来进行测试机器人而不影响到他人
@bot.register(bot.self, except_self=False) #TEXT
def reply_self(msg):
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    info = '【自动回复' + str(date) + '】'
    print(msg.sender, msg.text, msg.type)
    if msg.type == 'Text':
        #tuling.do_reply(msg)
        msg.reply(info)
    elif msg.type == 'Picture':
        msg.reply('你给我发图我也是看不到的啦 ~' + ' 【自动回复' + str(date) + '】')
    elif msg.type == 'Video':
        msg.reply('别乱发羞羞的东西哦 ~' + ' 【自动回复' + str(date) + '】')
    elif msg.type == 'Sharing':
        msg.reply('这是什么东西? ~' + ' 【自动回复' + str(date) + '】')
    elif msg.type == 'Recording':
        msg.reply('这个我处理不了，请说人话 ~' + ' 【自动回复' + str(date) + '】')
    elif msg.type == 'Map':
        msg.reply('这个地方我还没去过哦 ~' + ' 【自动回复' + str(date) + '】')
    elif msg.type == 'Card':
        msg.reply('消息已记录，小主人看到后会处理的 ~' + ' 【自动回复' + str(date) + '】')
    else:
        tuling.do_reply(msg)
        msg.reply('!$SGDGA#$$#$&$@#&@ ~' + ' 【自动回复' + str(date) + '】')
    #return 'received: {} ({})'.format(msg.text, msg.type)

# 回复 my_friend 发送的消息
@bot.register(Friend, except_self=True)
def reply_my_friend(msg):
     date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
     info = '【自动回复'+str(date)+'】'
     print(msg.sender, msg.text)
     if msg.type == 'Text':
        tuling.do_reply(msg)
        msg.reply(info)
     elif msg.type == 'Picture':
        msg.reply('你给我发图我也是看不到的啦 ~'+' 【自动回复'+str(date)+'】')
     elif msg.type == 'Video':
        msg.reply('别乱发羞羞的东西哦 ~' + ' 【自动回复' + str(date) + '】')
     elif msg.type == 'Sharing':
        msg.reply('这是什么东西? ~' + ' 【自动回复' + str(date) + '】')
     elif msg.type == 'Recording':
        msg.reply('这个我处理不了，请说人话 ~' + ' 【自动回复' + str(date) + '】')
     elif msg.type == 'Map':
        msg.reply('这个地方我还没去过哦 ~' + ' 【自动回复' + str(date) + '】')
     elif msg.type == 'Card':
        msg.reply('消息已记录，小主人看到后会处理的 ~' + ' 【自动回复' + str(date) + '】')
     else:
        msg.reply('!$SGDGA#$$#$&$@#&@ ~' + ' 【自动回复' + str(date) + '】')


# 定义一个群，根据群名搜索的
test_group = bot.groups(update=True).search()[0]
#ypp = test_group.members.search(' 。')[0] # 从群里获取一个人

# 群管理员
group_admin = test_group.members.search('Ryan')[0]

@bot.register(test_group, TEXT, except_self=False)
def gi_ren(msg):
    if '踢' in msg.text:
        #sender = test_group.members.search(msg.sender)[0]
        # if msg.member == group_admin:
        temp = msg.text.split('\u2005')[0]
        ti_name = temp.split('@')[1]
        member = test_group.members.search(ti_name)[0]
        print(dir(member))
        ti_ren(member)

# 打印出聊天信息中所有@自己的消息，并且自动回复
@bot.register(Group, TEXT)
def print_group_msg(msg):
    word1 = '开黑'
    word2 = '上车'
    word3 = '爸爸'
    word4 = '爷爷'
    word5 = '老子'
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if msg.is_at:
        info = '你@ 的人不是在搬砖就是在搬砖的路上，有什么事私信留言哦～【自动回复'+str(date)+'】'
        print(msg.sender, msg.text)
        if judge_dirty_word(msg.text):
            msg.reply('请文明用语。【自动回复' + str(date) + '】')
        elif word3 in msg.text or word4 in msg.text or word5 in msg.text:
            msg.reply('叫你爷爷干嘛？？？【自动回复' + str(date) + '】')
        elif word1 in msg.text or word2 in msg.text:
            msg.reply('开开开！就知道开黑，就不能好好读点书吗！！！【自动回复'+str(date)+'】')
        else:
            tuling.do_reply(msg)
            msg.reply(info)

def judge_dirty_word(msg):
    dirty_words_list = ['傻逼', '二逼', '2B', '2b', '白痴', '脑残', '狗', 'CNM']
    for word in dirty_words_list:
        if word in msg:
            return True
        else:
            return False

def ti_ren(member):
    member.remove()
    test_group.send('已将{}移除群聊'.format(member.name))
    test_group.add_members(member)
    test_group.send('已将{}加入群聊'.format(member.name))

embed()
# 开始运行
bot.join()
