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
COLUMN_QT = 0
BLOCKS_LIST = []
WITH_DOC = True

def up_update(number, name, real_name):
    global BLOCKS_LIST
    if number > 1:
        for b in BLOCKS_LIST:
            if b.split('_')[1] == str(number-1): # 找到位于上方那个块
                globals()[b].name = f"{number}_{b.split('_')[2]}" # 把它名字开头的数改成自己的数
                globals()[f'dyn_block_{globals()[b].name.split("_")[1]}'].destroy()
                globals()[b].number += 1 # 把它的数加1
                BLOCKS_LIST[globals()[b].number-2] = f'block_{globals()[b].name}' # 更新档案里它的名字
                BLOCKS_LIST[globals()[b].number-1] = f"block_{number-1}_{name.split('_')[1]}" # 更新档案里自己的名字
                store_name = BLOCKS_LIST[globals()[b].number-2]
                BLOCKS_LIST[globals()[b].number-2] = BLOCKS_LIST[globals()[b].number-1]
                BLOCKS_LIST[globals()[b].number-1] = store_name

def down_update(number, name, real_name):
    global BLOCKS_LIST
    if number < len(BLOCKS_LIST):
        for b in BLOCKS_LIST:
            if b.split('_')[1] == str(number+1):
                globals()[b].name = f"{number}_{b.split('_')[2]}"
                globals()[f'dyn_block_{globals()[b].name.split("_")[1]}'].destroy()
                globals()[b].number -= 1
                BLOCKS_LIST[globals()[b].number] = f'block_{globals()[b].name}'
                BLOCKS_LIST[globals()[b].number-1] = f"block_{number+1}_{name.split('_')[1]}"
                store_name = BLOCKS_LIST[globals()[b].number]
                BLOCKS_LIST[globals()[b].number] = BLOCKS_LIST[globals()[b].number-1]
                BLOCKS_LIST[globals()[b].number-1] = store_name
       
class Block(object):

    def __init__(self, name):
        global BLOCKS_LIST
        BLOCKS_LIST.append(f'block_{name}')
        self.name = name
        self.real_name = name.split('_')[1]
        self.number = int(name.split('_')[0])

    def display(self, parent):
        globals()[f'dyn_block_{self.real_name}'] = Frame(parent)
        globals()[f'dyn_block_{self.real_name}'].pack(side=LEFT)
        def up():
            up_update(self.number, self.name, self.real_name)
            globals()[f'dyn_block_{self.real_name}'].destroy()
            self.number -= 1
            self.name = f"{self.number}_{self.name.split('_')[1]}"
            globals()[BLOCKS_LIST[self.number-1]] = Block(BLOCKS_LIST[self.number-1].split('block_')[1])
            globals()[BLOCKS_LIST[self.number-1]].display(globals()[f'bl_{(self.number-1)//10}_{(self.number-1)%10}'])
            globals()[BLOCKS_LIST[self.number]] = Block(BLOCKS_LIST[self.number].split('block_')[1])
            globals()[BLOCKS_LIST[self.number]].display(globals()[f'bl_{(self.number)//10}_{(self.number)%10}'])
            del BLOCKS_LIST[-1]
            del BLOCKS_LIST[-1]

        globals()[f'bt1_{self.name}'] = Button(globals()[f'dyn_block_{self.real_name}'], command=up, text='↑')
        globals()[f'bt1_{self.name}'].pack(side=LEFT)
        if self.number == 1:
            globals()[f'bt1_{self.name}']['state'] = 'disabled'
        def down():
            down_update(self.number, self.name, self.real_name)
            globals()[f'dyn_block_{self.real_name}'].destroy()
            self.number += 1
            self.name = f"{self.number}_{self.name.split('_')[1]}"
            globals()[BLOCKS_LIST[self.number-1]] = Block(BLOCKS_LIST[self.number-1].split('block_')[1])
            globals()[BLOCKS_LIST[self.number-1]].display(globals()[f'bl_{(self.number-1)//10}_{(self.number-1)%10}'])
            globals()[BLOCKS_LIST[self.number-2]] = Block(BLOCKS_LIST[self.number-2].split('block_')[1])
            globals()[BLOCKS_LIST[self.number-2]].display(globals()[f'bl_{(self.number-2)//10}_{(self.number-2)%10}'])
            del BLOCKS_LIST[-1]
            del BLOCKS_LIST[-1]
        globals()[f'bt2_{self.name}'] = Button(globals()[f'dyn_block_{self.real_name}'], command=down, text='↓')
        globals()[f'bt2_{self.name}'].pack(side=LEFT)
        if self.number == len(BLOCKS_LIST):
            globals()[f'bt2_{self.name}']['state'] = 'disabled'
        globals()[f'block_num_{self.real_name}'] = StringVar()
        globals()[f'block_num_{self.real_name}'].set(self.number)
        globals()[f'num_lb_{self.real_name}'] = Label(globals()[f'dyn_block_{self.real_name}'], textvariable=globals()[f'block_num_{self.real_name}'])
        globals()[f'num_lb_{self.real_name}'].pack(side=LEFT)
        globals()[f'block_var_{self.real_name}'] = StringVar()
        globals()[f'block_var_{self.real_name}'].set(self.real_name)
        globals()[self.real_name] = Label(globals()[f'dyn_block_{self.real_name}'], textvariable=globals()[f'block_var_{self.real_name}'], font=('Arial', int(font_size/2)), width=int(font_size*0.75))
        globals()[self.real_name].pack(side=RIGHT)

def merge(path, doc):
    """
    @author: Yuanyang Shao
    merge pdf files
    """
    # 找到所有pdf并排序
    pattern =r"\.pdf$"
    if doc:
        fs_order = {}
    else:
        fs_order = {0: '没有Word文档'}
    fs_with_order = []
    fs_without_order = [path + "\\" + f for f in listdir(path) if search(pattern, f, IGNORECASE) and not search(r'merged_file.pdf', f)]
    for f in fs_without_order:
        fs_order[int(f.split('\\')[-1].split('/')[-1].split('_')[0])] = f
    if doc:
        for i in range(len(fs_without_order)):
            fs_with_order.append(fs_order[i])
    else:
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
        word_var.set(f'已选中word文档：{word_location}')
        DOC = word_location
        word_bt.destroy()
word_bt = Button(row1, text='                  选择待合并Word文档（.doc或.docx格式都行）                ', command=find_word, font=('Arial', font_size))
word_bt.pack(side=RIGHT)
row2 = Frame(info_fr)
row2.pack(fill='x') # 第二行
pdf_var = StringVar()
pdf_lb = Label(row2, textvariable=pdf_var, font=('Arial', font_size))
pdf_lb.pack(side=LEFT)
def find_pdfs():
    global PDFS_PATH, COLUMN_QT
    pdfs_qt = 0
    wf = filedialog.askdirectory()
    if wf != None:
        PDFS_PATH = wf
        pdf_var.set(f'已选标书pdf所在目录：{wf}')
        for f in listdir(wf):
            if f.split('.')[-1] == 'pdf':
                pdfs_qt += 1
                if len(f.split('_')) > 1: # 防止文件名自带下划线对后面重命名的过程造成影响
                    new_name = []
                    new = ''
                    for u in f.split('_'):
                        new_name.append(u)
                    new = new.join(new_name)
                    name_str = f'{pdfs_qt}_{new}'
                else:
                    name_str = f'{pdfs_qt}_{f}'
                globals()[f"block_{name_str.split('.pdf')[0]}"] = Block(name_str.split('.pdf')[0])
        pdfs_quantity.set(f'共选中{pdfs_qt}个pdf文档，点击文件名前的箭头为其排序↓↓↓')
        COLUMN_QT = pdfs_qt//10 + 1
        for c in range(COLUMN_QT):
            if c < 13:
                globals()[f'column{c}'] = Frame(row4)
                globals()[f'column{c}'].pack(side=LEFT)
                for r in range(10):
                    globals()[f'bl_{c}_{r}'] = Frame(globals()[f'column{c}'])
                    globals()[f'bl_{c}_{r}'].pack()
            else:
                globals()[f'column{c}'] = Frame(row5)
                globals()[f'column{c}'].pack(side=LEFT)
                for r in range(10):
                    globals()[f'bl_{c}_{r}'] = Frame(globals()[f'column{c}'])
                    globals()[f'bl_{c}_{r}'].pack()
        for b in BLOCKS_LIST:
            globals()[b].display(globals()[f"bl_{(int(b.split('_')[1])-1)//10}_{(int(b.split('_')[1])-1)%10}"])
        pdf_bt.destroy()
pdf_bt = Button(row2, text='选择待合并pdf文档所在目录（请先确保该目录下没有其他pdf文档）', command=find_pdfs, font=('Arial', font_size))
pdf_bt.pack(side=RIGHT)
row3 = Frame(info_fr)
row3.pack(fill='x') # 第三行

Label(wd).pack(fill='x') # 用于排版的空标签

pdfs_quantity = StringVar()
count_lb = Label(row3, textvariable=pdfs_quantity, font=('Arial', font_size))
count_lb.pack()

Label(wd).pack(fill='x') # 用于排版的空标签

row4 = Frame(info_fr)
row4.pack(fill='x') # 第四行

Label(wd).pack(fill='x') # 用于排版的空标签

row5 = Frame(info_fr)
row5.pack(fill='x') # 第五行

Label(wd).pack(fill='x') # 用于排版的空标签
Label(wd).pack(fill='x') # 用于排版的空标签

def mg_them():
    global PDFS_PATH, WITH_DOC
    pdf_count = 0
    make_bt['state'] = 'disabled'
    for f in listdir(PDFS_PATH): # 把指定文件夹中所有pdf文件复制到data文件夹里
        if f.split('.')[-1] == 'pdf':
            copy2(PDFS_PATH+'/'+f, data_path)
    pdfs_list = listdir(data_path)
    chdir(data_path)
    for f in pdfs_list: # 按已排列表给所有pdf文档重命名
        if f.split('.')[-1] == 'pdf':
            if len(f.split('_')) > 1: # 去掉原文件名中所有下划线
                new_name = []
                new = ''
                for u in f.split('_'):
                    new_name.append(u)
                new = new.join(new_name)
                rename(f, new)
                pdfs_list[pdf_count] = new
        for b in BLOCKS_LIST:
            if f"{b.split('_')[2]}.pdf" == pdfs_list[pdf_count]:
                rename(pdfs_list[pdf_count], f"{b.split('block_')[1]}.pdf")
        pdf_count += 1
    if DOC != '':
        copy2(DOC, data_path)
        chdir(data_path)
        doc_name = DOC.split('/')[-1]
        full_name = f'{data_path}/{doc_name}'
        doc2pdf(full_name, f'{data_path}/0_{doc_name.split(".")[-2]}.pdf')
    else:
        WITH_DOC = False
    merge(data_path, WITH_DOC)
    save_name = filedialog.asksaveasfilename(title='标书另存为', defaultextension='.pdf', initialfile='整合版文档名称', filetypes=[('PDF','*.pdf')])
    new_file_name = save_name.split('/')[-1]
    save_path = save_name.split(new_file_name)[-2]
    copy2(data_path+'merged_file.pdf', save_path)
    chdir(save_path)
    rename('merged_file.pdf', new_file_name)
    with open(f'目录——{new_file_name}.txt', 'a', encoding='UTF-8') as f:
        for i in range(len(BLOCKS_LIST)):
            f.write(BLOCKS_LIST[i].split('block_')[1])
            f.write('\n')
    for f in listdir(data_path):
        if f != 'settings.json':
            remove(data_path+f)
    wd.destroy()
make_bt = Button(wd, text='  设置完毕，生成标书  ', command=mg_them, font=('Arial', font_size*2))
make_bt.pack()

wd.mainloop()
