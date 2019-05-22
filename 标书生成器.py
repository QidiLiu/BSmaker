#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"Combine a word document into one or more pdf files to ease my dad's work load"

__author__ = 'QidiLiu'

from tkinter import Tk, Label, Button, filedialog, StringVar, Frame, LEFT, RIGHT
from json import load, dumps
from os import path, remove
from win32com.client import DispatchEx

program_path = path.abspath(path.dirname(__file__))
data_path = f'{program_path}/data/'

def doc2pdf(doc_name, pdf_name):
    """
    :word文件转pdf
    :param doc_name word文件名称
    :param pdf_name 转换后pdf文件名称
    """
    try:
        word = DispatchEx("Word.Application")
        if path.exists(pdf_name):
            remove(pdf_name)
        worddoc = word.Documents.Open(doc_name,ReadOnly = 1)
        worddoc.SaveAs(pdf_name, FileFormat = 17)
        worddoc.Close()
        return pdf_name
    except:
        return 1
'''
作者：天道酬勤_业道酬信 
来源：CSDN 
原文：https://blog.csdn.net/qq_16645423/article/details/79468122 
版权声明：本文为博主原创文章，转载请附上博文链接！
'''

wd = Tk()
wd.title('标书生成器 —— github.com/QidiLiu')
w = wd.winfo_screenwidth()
h = wd.winfo_screenheight()
font_size = int(h/67.5)
wd.geometry(str(int(w/4))+'x'+str(int(h/2)))

info_fr = Frame(wd)
info_fr.place(x=3/32*w, y=1/8*h, anchor='center')
word_var = StringVar()
word_lb = Label(info_fr, textvariable=word_var, font=('Arial', font_size))
word_lb.pack(side=LEFT)
def find_word():
    word_location = filedialog.askopenfile()
    doc2pdf(word_location, f'{data_path}{word_location.split(".")[-2]}.pdf')
word_bt = Button(info_fr, text='更改', command=find_word, font=('Arial', font_size))

wd.mainloop()
