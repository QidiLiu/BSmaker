#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"Combine a word document into one or more pdf files to ease my dad's work load"

__author__ = 'QidiLiu'

from tkinter import Tk, Label, Button, filedialog, StringVar, Frame, LEFT, RIGHT
from json import load, dumps
from os import path, remove, chdir, listdir
from win32com.client import DispatchEx
from pdfs_merge import merge

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
        chdir(data_path)
        worddoc.SaveAs(pdf_name, FileFormat = 17)
        chdir(program_path)
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

Label(wd).pack(fill='x') # 用于排版的空标签

info_fr = Frame(wd) # 信息显示和设置区域
info_fr.pack(fill='x')
row1 = Frame(info_fr)
row1.pack(fill='x') # 第一行
word_var = StringVar()
word_lb = Label(row1, textvariable=word_var, font=('Arial', font_size))
word_lb.pack(side=LEFT)
def find_word():
    wf = filedialog.askopenfile()
    if wf != None:
        word_location = wf.name
        word_bt.config(text='更改', bg='blue')
        word_var.set(word_location)
    #doc2pdf(word_location, f'{word_location.split(".")[-2]}.pdf')
word_bt = Button(row1, text='    选择要转的Word文档（.doc或.docx格式都行）    ', command=find_word, font=('Arial', font_size))
word_bt.pack(side=RIGHT)
row2 = Frame(info_fr)
row2.pack(fill='x') # 第二行
pdf_var = StringVar()
pdf_lb = Label(row2, textvariable=pdf_var, font=('Arial', font_size))
pdf_lb.pack(side=LEFT)
def find_pdfs():
    pdfs_qt = 0
    wf = filedialog.askdirectory()
    if wf != None:
        pdf_var.set(wf)
        pdf_bt.config(text='更改', bg='red')
        for f in listdir(wf):
            pdfs_qt += 1
        pdfs_quantity.set(f'共选中{pdfs_qt}个pdf文档')
pdf_bt = Button(row2, text='选择待合并pdf文档所在目录（要先确保该目录下没有其他pdf文档）', command=find_pdfs, font=('Arial', font_size))
pdf_bt.pack(side=RIGHT)
row3 = Frame(info_fr)
row3.pack(fill='x') # 第三行
pdfs_quantity = StringVar()
count_lb = Label(row3, textvariable=pdfs_quantity, font=('Arial', font_size))
count_lb.pack()

Label(wd).pack(fill='x') # 用于排版的空标签

def mg_them():
    merge(data_path)
make_bt = Button(wd, text='  生成标书  ', command=mg_them, font=('Arial', font_size*2))
make_bt.pack()

wd.mainloop()
