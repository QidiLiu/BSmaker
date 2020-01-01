# /usr/bin/env python3
# -*- coding: utf-8 -*-

'简易版山东话发音生成器'

__author__ = 'QidiLiu'

import pygame

pygame.mixer.pre_init(44100, -16, 1, 512)

def chinese_to_pinyin(x):
    y = ''
    dic = {}
    with open("unicode_py.txt") as f:
        for i in f.readlines():
            dic[i.split()[0]] = i.split()[1]
    for i in x:
        i = str(i.encode('unicode_escape'))[-5:-1].upper()
        try:
            y += dic[i] + ' '
        except:
            y += 'XXXX '  # 非法字符我们用XXXX代替
    return y
"""
input: 汉字字符串
output: 拼音字符串
from: https://zhuanlan.zhihu.com/p/26726297
"""


def make_voice(x, f):
    table = str.maketrans('1234', '2413')
    pygame.mixer.init()
    voi = chinese_to_pinyin(x).split()
    for i in voi:
        if i == 'XXXX':  # 处理'XXXX'的音，可将其忽略
            continue
        if(f == 0):
            j = i
        else:
            j = i.translate(table)
        pygame.mixer.music.load("pinyin/" + j + ".wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            pass
    return None
"""
input: 拼音字符串， 方言版本（0 - 普通话， 1 - 山东话）
output: 直接发音，无返回参数
from: https://zhuanlan.zhihu.com/p/26726297
"""

while True:
    p = input("请输入文字：")
    print('普通话版')
    make_voice(p, 0)
    print('山东话版')
    make_voice(p, 1)
