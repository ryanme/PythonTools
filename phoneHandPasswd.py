# coding:utf8
# author: ryan
import random
from math import sqrt
list_a = [1,2,3,4,5,6,7,8,9]
L = len(list_a)
# 每一行个数
g = int(sqrt(L) )
c = L/g
 # 四个角
corner_list = [1,g,1+2*g,L]
# 除角落外的边界数字
middle_list = []
for i in range(2,g):
    # 首行
    middle_list.append(i)
    # 末行
    middle_list.append(i+2*g)
for i in range(1+g,1+2*g,g):
    # 左侧
    middle_list.append(i)
    # 右侧
    middle_list.append(i+g-1)

# 角落数字推算下一个数
def corner_make_nextnum(x):
    temp_list =[]
    # 边角数字固定只有四个，分两种, 1 和最大值 (也就是L))往前-1或者往后+1，不在1到L之间间，是一类。 另外两个是另一类
    if x-1 not in list_a or x+1 not in list_a:
        # 1 和 len, x-1不在list_a里，是左上角，反之是右下角
        if x-1 not in list_a:
            # 左上角，符合数字，右，下，右下
            x_right = x + 1
            x_down = x + g
            x_right_down = x + g + 1
            temp_list.append(x_right)
            temp_list.append(x_down)
            temp_list.append(x_right_down)
        else:
            # 右下角，符合数字，左，上，左上
            x_left = x - 1
            x_up = x - g
            x_left_up = x - g - 1
            temp_list.append(x_left)
            temp_list.append(x_up)
            temp_list.append(x_left_up)
    else:
        # 如果x-g还在list_a里，是左下角，反之是右上角
        if x-g in list_a:
            # 左下角，符合数字：上，右上，右
            x_up = x - g
            x_right_down = x - g + 1
            x_right = x + 1
            temp_list.append(x_up)
            temp_list.append(x_right_down)
            temp_list.append(x_right)
        else:
            # 右上角，符合数字：左，左下，下
            x_left = x - 1
            x_left_down = x + g - 1
            x_down = x + g
            temp_list.append(x_left)
            temp_list.append(x_left_down)
            temp_list.append(x_down)
    #next_num = random.choice(temp_list)
    temp_list.sort()
    return temp_list

# 每行中间数推算下一个数
def line_without_corner(x):
    temp_list = []
    # 如果+g，-g不在list_a中，那就是横向的
    if x+g not in list_a or x-g not in list_a:
        x_left = x - 1
        x_right = x + 1
        # 如果x比g小，那说明是第一行的，反之是最后一行的
        if x < g:
            # 第一行符合数字为左，右，下，临近的左下，右下
            x_down = x + g
            x_left_down = x + g - 1
            x_right_down = x + g + 1
            temp_list.append(x_down)
            temp_list.append(x_left_down)
            temp_list.append(x_right_down)
        else:
            # 最后一行符合数字为左，右，上，临近的左上，右上
            x_up= x - g
            x_left_up = x - g - 1
            x_right_up = x - g + 1
            temp_list.append(x_up)
            temp_list.append(x_left_up)
            temp_list.append(x_right_up)
        temp_list.append(x_left)
        temp_list.append(x_right)
     # 纵向的,且如果是g的倍数，则表示是在右侧边界，若不是则表示在左侧边界
    else:
        # 自然数，横竖个数相同的这种排列，上下相差始终为g
        x_up = x - g
        x_down = x + g
        # 右侧边界，可以除了上下还有临近的左侧，左上，左下
        if x%g == 0:
            x_left = x - 1
            x_left_up = x - g - 1
            x_left_dwwn = x + g - 1
            temp_list.append(x_left)
            temp_list.append(x_left_up)
            temp_list.append(x_left_dwwn)
        # 左侧边界，可以除了上下还有右临近的右侧，右上，右下
        else:
            x_right = x + 1
            x_right_up = x - g + 1
            x_right_dwwn = x + g + 1
            temp_list.append(x_right)
            temp_list.append(x_right_up)
            temp_list.append(x_right_dwwn)
        temp_list.append(x_up)
        temp_list.append(x_down)
    #next_num = random.choice(temp_list)
    temp_list.sort()
    return temp_list

# 中间的数字推算下一个数，上，下，左，右，左上，左下，右上，右上，固定有8个
def middle_make_nextnum(x):
    temp_list = [x-1, x+1, x-g, x+g, x-g-1, x-g+1, x+g-1, x+g+1]
    # next_num = random.choice(temp_list)
    return temp_list

# 根据已有数字推测下一可能数字集合
def available_next(x):
    if x in corner_list:
        temp_list = corner_make_nextnum(x)
    elif x in middle_list:
        temp_list = line_without_corner(x)
    else:
        temp_list = middle_make_nextnum(x)
    temp_list.sort()
    return temp_list

def choice_one(temp_list):
    next_num = random.choice(temp_list)
    return next_num

def random_make_num(n):
    head_num = random.choice(list_a)
    temp_list = available_next(head_num)
    passwd_list = [head_num]
    i = 1
    remove_list = []
    while i <n:
        if temp_list == []:
            return passwd_list
        next_num = choice_one(temp_list)
        if next_num in passwd_list:
            if temp_list == []:
                num = passwd_list[-1]
                remove_list.append(num)
                temp_list = available_next(num)
                passwd_list.remove(remove_list)
                temp_list.remove(remove_list)
            else:
                temp_list.remove(next_num)
        else:
            i+=1
            passwd_list.append(next_num)
            temp_list = available_next(next_num)
    return passwd_list

if __name__ == "__main__":
    passwd_list = random_make_num(3)
    print(passwd_list)