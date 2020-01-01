#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'A binary clock for tkinter GUI'

__author__ = 'QidiLiu'

from time import strftime, localtime
from tkinter import Frame

def time_recode(x):  # 把时间中的各位数字转为二进制表示并填补为四位
    time_list = list(str(bin(int(x))))
    time_list = time_list[2:]
    while len(time_list) < 4:
        time_list.insert(0, '0')
    return time_list

def blingbling(x):  # 将二进制时间表达中的0和1转化为黑和白
    if x == '0':
        color = 'black'
    else:
        color = 'white'
    return color

class Create_blocks(object):

    def __init__(self, main_window, block_size): # 16个时间显示正方形
        self.block_11 = Frame(main_window, height=block_size, width=block_size)
        self.block_21 = Frame(main_window, height=block_size, width=block_size)
        self.block_31 = Frame(main_window, height=block_size, width=block_size)
        self.block_41 = Frame(main_window, height=block_size, width=block_size)
        self.block_12 = Frame(main_window, height=block_size, width=block_size)
        self.block_22 = Frame(main_window, height=block_size, width=block_size)
        self.block_32 = Frame(main_window, height=block_size, width=block_size)
        self.block_42 = Frame(main_window, height=block_size, width=block_size)
        self.block_13 = Frame(main_window, height=block_size, width=block_size)
        self.block_23 = Frame(main_window, height=block_size, width=block_size)
        self.block_33 = Frame(main_window, height=block_size, width=block_size)
        self.block_43 = Frame(main_window, height=block_size, width=block_size)
        self.block_14 = Frame(main_window, height=block_size, width=block_size)
        self.block_24 = Frame(main_window, height=block_size, width=block_size)
        self.block_34 = Frame(main_window, height=block_size, width=block_size)
        self.block_44 = Frame(main_window, height=block_size, width=block_size)
        self.block_11.place(x=block_size*0.5, y=block_size*0.5, anchor='center')
        self.block_21.place(x=block_size*0.5, y=block_size*1.5, anchor='center')
        self.block_31.place(x=block_size*0.5, y=block_size*2.5, anchor='center')
        self.block_41.place(x=block_size*0.5, y=block_size*3.5, anchor='center')
        self.block_12.place(x=block_size*1.5, y=block_size*0.5, anchor='center')
        self.block_22.place(x=block_size*1.5, y=block_size*1.5, anchor='center')
        self.block_32.place(x=block_size*1.5, y=block_size*2.5, anchor='center')
        self.block_42.place(x=block_size*1.5, y=block_size*3.5, anchor='center')
        self.block_13.place(x=block_size*2.5, y=block_size*0.5, anchor='center')
        self.block_23.place(x=block_size*2.5, y=block_size*1.5, anchor='center')
        self.block_33.place(x=block_size*2.5, y=block_size*2.5, anchor='center')
        self.block_43.place(x=block_size*2.5, y=block_size*3.5, anchor='center')
        self.block_14.place(x=block_size*3.5, y=block_size*0.5, anchor='center')
        self.block_24.place(x=block_size*3.5, y=block_size*1.5, anchor='center')
        self.block_34.place(x=block_size*3.5, y=block_size*2.5, anchor='center')
        self.block_44.place(x=block_size*3.5, y=block_size*3.5, anchor='center')
    
    def get_time(self):  # 获取时刻并转为四个数列，再进一步转化为正方形颜色组合
        H = list(strftime('%H', localtime()))
        M = list(strftime('%M', localtime()))

        COLUMN_1 = time_recode(H[0])
        COLUMN_2 = time_recode(H[1])
        COLUMN_3 = time_recode(M[0])
        COLUMN_4 = time_recode(M[1])
        
        self.block_11.config(bg=blingbling(COLUMN_1[0]))
        self.block_21.config(bg=blingbling(COLUMN_1[1]))
        self.block_31.config(bg=blingbling(COLUMN_1[2]))
        self.block_41.config(bg=blingbling(COLUMN_1[3]))
        self.block_12.config(bg=blingbling(COLUMN_2[0]))
        self.block_22.config(bg=blingbling(COLUMN_2[1]))
        self.block_32.config(bg=blingbling(COLUMN_2[2]))
        self.block_42.config(bg=blingbling(COLUMN_2[3]))
        self.block_13.config(bg=blingbling(COLUMN_3[0]))
        self.block_23.config(bg=blingbling(COLUMN_3[1]))
        self.block_33.config(bg=blingbling(COLUMN_3[2]))
        self.block_43.config(bg=blingbling(COLUMN_3[3]))
        self.block_14.config(bg=blingbling(COLUMN_4[0]))
        self.block_24.config(bg=blingbling(COLUMN_4[1]))
        self.block_34.config(bg=blingbling(COLUMN_4[2]))
        self.block_44.config(bg=blingbling(COLUMN_4[3]))
    
    def destroy(self):
        self.block_11.destroy()
        self.block_21.destroy()
        self.block_31.destroy()
        self.block_41.destroy()
        self.block_12.destroy()
        self.block_22.destroy()
        self.block_32.destroy()
        self.block_42.destroy()
        self.block_13.destroy()
        self.block_23.destroy()
        self.block_33.destroy()
        self.block_43.destroy()
        self.block_14.destroy()
        self.block_24.destroy()
        self.block_34.destroy()
        self.block_44.destroy()
