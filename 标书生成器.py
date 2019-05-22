#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"Combine a word document into one or more pdf files to ease my dad's work load"

__author__ = 'QidiLiu'

from tkinter import Tk, Label, Button, filedialog, StringVar, Frame, LEFT, RIGHT
from json import load, dumps
from os import path, remove, chdir, listdir, rename
from win32com.client import DispatchEx
from PyPDF2 import PdfFileMerger
from re import IGNORECASE, search
from shutil import copy2

program_path = path.abspath(path.dirname(__file__))
data_path = f'{program_path}/data/'
DOC = ''
PDFS_PATH = data_path

def merge(path):
    """
    @author: Yuanyang Shao
    merge pdf files
    """
    # 找到所有pdf并排序
    pattern =r"\.pdf$"
    fs_order = {}
    fs_with_order = []
    fs_without_order = [path + "\\" + f for f in listdir(path) if search(pattern, f, IGNORECASE) and not search(r'merged_file.pdf', f)]
    for f in fs_without_order:
        fs_order = {int(f.split('_')[0]):f}
    for i in range(len(fs_without_order)):
        fs_with_order.append(fs_order[i+1])

    # merge the file
    opened_file = [open(file_name, 'rb') for file_name in fs_with_order]
    pdfFM = PdfFileMerger()
    for file in opened_file:
        pdfFM.append(file)

    # output the file
    with open(path + "\\merged_file.pdf", 'wb') as write_out_file:
        pdfFM.write(write_out_file)

    # close all the input files
    for file in opened_file:
        file.close()

def make_order(path, order):
    pass
    
def doc2pdf(doc_name, pdf_name):
    """
    :word文件转pdf
    :param doc_name word文件名称
    :param pdf_name 转换后pdf文件名称

    作者：天道酬勤_业道酬信 
    来源：CSDN 
    原文：https://blog.csdn.net/qq_16645423/article/details/79468122 
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
    global DOC
    wf = filedialog.askopenfile()
    if wf != None:
        word_location = wf.name
        word_bt.config(text='更改', bg='blue')
        word_var.set(word_location)
        DOC = word_location
word_bt = Button(row1, text='    选择要转的Word文档（.doc或.docx格式都行）    ', command=find_word, font=('Arial', font_size))
word_bt.pack(side=RIGHT)
row2 = Frame(info_fr)
row2.pack(fill='x') # 第二行
pdf_var = StringVar()
pdf_lb = Label(row2, textvariable=pdf_var, font=('Arial', font_size))
pdf_lb.pack(side=LEFT)
def find_pdfs():
    global PDFS_PATH
    pdfs_qt = 0
    wf = filedialog.askdirectory()
    if wf != None:
        PDFS_PATH = wf
        pdf_var.set(wf)
        pdf_bt.config(text='更改', bg='red')
        for f in listdir(wf):
            if f.split('.')[-1] == 'pdf':
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

row4 = Frame(info_fr)
row4.pack(fill='x') # 第四行


Label(wd).pack(fill='x') # 用于排版的空标签
Label(wd).pack(fill='x') # 用于排版的空标签
Label(wd).pack(fill='x') # 用于排版的空标签
Label(wd).pack(fill='x') # 用于排版的空标签

def mg_them():
    make_bt['state'] = 'disabled'
    copy2(DOC, data_path)
    doc2pdf(DOC, f'{DOC.split(".")[-2]}.pdf')
    for f in listdir(PDF_PATH):
        if f.split('.')[-1] == 'pdf':
            copy2(PDF_PATH+f, data_path)
    make_order(data_path, final_order)
    merge(data_path)
    save_name = filedialog.asksaveasfilename(title='标书另存为', defaultextension='.pdf', initialfile='整合版文档名称', filetypes=[('PDF','*.pdf')])
    new_file_name = save_name.split('/')[-1]
    save_path = save_name.split(new_file_name)[-1]
    copy2(data_path+'merged_file.pdf', save_path)
    chdir(save_path)
    rename('merged_file.pdf', new_file_name)
    for f in data_path:
        if f.name != 'settings.json':
            remove(data_path+f.name)
    make_bt['state'] = 'normal'
make_bt = Button(wd, text='  生成标书  ', command=mg_them, font=('Arial', font_size*2))
make_bt.pack()

wd.mainloop()
