# /usr/bin/env python3
# -*- coding: utf-8 -*-

'pdf滤镜'

__author__ = 'QidiLiu'

from tkinter import filedialog, Tk, Label, Button, StringVar, Menu
from PIL import Image
from os import listdir, remove, path, makedirs, _exit
from time import sleep
from threading import Thread
from json import dumps, load
import PIL.ImageOps
import fitz
import glob

WINDOW_STATUS = True
FILTER_STATUS = False

# 初始化设置（根据上次使用保存的settings.json)
with open('settings.json', 'r', encoding='utf-8') as f:
    settings = load(f)
RESOLUTION = settings['RESOLUTION']
FILTER_MODE = settings['FILTER_MODE']
RESOL_MODE = settings['RESOL_MODE']

# 修改分辨率设置的函数
def change_resol(n): # tkinter的菜单栏command居然无法直接传入参数，太菜了
    global RESOLUTION
    info_var.set(f'滤镜：{FILTER_MODE}\n清晰：{RESOL_MODE}') # 刷新设置
    RESOLUTION = n

# 菜单各个选项调用的函数
def change_resol_low():
    global RESOL_MODE
    RESOL_MODE = '低清'
    change_resol(1)

def change_resol_normal():
    global RESOL_MODE
    RESOL_MODE = '一般'
    change_resol(1.5)

def change_resol_high():
    global RESOL_MODE
    RESOL_MODE = '高清'
    change_resol(2)

def change_filter_invert():
    global FILTER_MODE
    FILTER_MODE = '反色'
    info_var.set(f'滤镜：{FILTER_MODE}\n清晰：{RESOL_MODE}') # 刷新设置

def change_filter_grayscale():
    global FILTER_MODE
    FILTER_MODE = '灰度'
    info_var.set(f'滤镜：{FILTER_MODE}\n清晰：{RESOL_MODE}') # 刷新设置

def change_filter_crop():
    global FILTER_MODE
    FILTER_MODE = '去边'
    info_var.set(f'滤镜：{FILTER_MODE}\n清晰：{RESOL_MODE}') # 刷新设置

def change_filter_autocontrast():
    global FILTER_MODE
    FILTER_MODE = '增强'
    info_var.set(f'滤镜：{FILTER_MODE}\n清晰：{RESOL_MODE}') # 刷新设置

def change_filter_posterize():
    global FILTER_MODE
    FILTER_MODE = '跳阶'
    info_var.set(f'滤镜：{FILTER_MODE}\n清晰：{RESOL_MODE}') # 刷新设置

# 滤镜处理函数
def pdf_filter():
    global FILTER_STATUS
    # 等待被触发
    while WINDOW_STATUS:
        if FILTER_STATUS:
            FILTER_STATUS = False
            # 取消Button功能，触发进度提示
            bt['state'] = 'disabled'
            progress = 0
            var_01.set('正在处理，请稍候...')
            var_10.set(f'处理进度：{progress}%')

            # pdf转png
            try:
                input_pdf = filedialog.askopenfile(title='选择pdf文档').name
            except:
                close_window()
            input_doc = fitz.open(input_pdf)
            toc = input_doc.getToC() # 获取待处理pdf的目录
            page_sum = input_doc.pageCount
            for i in range(0, page_sum):
                page = input_doc[i]
                zoom = 100 * RESOLUTION # 缩放
                rotate = 0 # 无转动
                trans = fitz.Matrix(zoom/100.0, zoom/100.0).preRotate(rotate)
                pm = page.getPixmap(matrix=trans, alpha=False)
                if(i+1<10):
                    page_num = '000' + str(i+1)
                elif(i+1<100):
                    page_num = '00' + str(i+1)
                elif(i+1<1000):
                    page_num = '0' + str(i+1)
                else:
                    page_num = str(i+1)
                pm.writePNG('pdf2png/%s.png' % page_num)
                progress = int(40 * (i/page_sum))
                var_10.set(f'处理进度：{progress}%')
            input_doc.close()

            # png图片处理
            m = page_sum
            path = ('pdf2png/')
            f = listdir(path)
            for i in f:
                if i=='0000.png':
                    continue
                img = Image.open(path+i)
                if FILTER_MODE == '反色':
                    inv_img = PIL.ImageOps.invert(img)
                elif FILTER_MODE == '灰度':
                    inv_img = PIL.ImageOps.grayscale(img)
                elif FILTER_MODE == '去边':
                    inv_img = PIL.ImageOps.crop(img, border=10)
                elif FILTER_MODE == '增强':
                    inv_img = PIL.ImageOps.autocontrast(img, cutoff=10)
                else: # FILTER_MODE == '跳阶'
                    inv_img = PIL.ImageOps.posterize(img, 2)
                inv_img.save(path+i)
                m -= 1
                progress = int(40 + 30 * (page_sum-m)/page_sum)
                var_10.set(f'处理进度：{progress}%')

            # png转pdf
            n = page_sum
            output_doc = fitz.open()
            for img in sorted(glob.glob('pdf2png/*')):
                imgdoc = fitz.open(img)
                pdfbytes = imgdoc.convertToPDF()
                imgpdf = fitz.open('pdf', pdfbytes)
                output_doc.insertPDF(imgpdf)
                n -= 1
                progress = int(70 + 30 * (page_sum-n)/page_sum)
                var_10.set(f'处理进度：{progress}%')
            var_01.set('处理完成！')
            #output_path = filedialog.askdirectory(title='请选择保存位置')+'/'
            output_path = filedialog.asksaveasfilename(title='另存为输出pdf文档', defaultextension='.pdf', initialfile=f'{FILTER_MODE} - '+input_pdf.split('/')[-1], filetypes=[('PDF','*.pdf')])
            output_doc.setToC(toc) # 将原pdf的目录加入新pdf中
            output_doc.save(output_path)
            output_doc.close()
            close_window()
        else:
            sleep(0.3)

# 单独为滤镜处理安排一个线程
def main():
    Thread(target=pdf_filter).start()

def close_window():
    global WINDOW_STATUS
    WINDOW_STATUS = False
    for f in listdir('pdf2png/'):
        remove('pdf2png/'+f)
    with open('settings.json', 'w', encoding='utf-8') as f:
        settings['RESOLUTION'] = RESOLUTION
        settings['FILTER_MODE'] = FILTER_MODE
        settings['RESOL_MODE'] = RESOL_MODE
        f.write(dumps(settings, ensure_ascii=False))
    sleep(0.3)
    _exit(0)
    
if __name__ == "__main__":
    # 判断目录是否存在
    if_path = 'pdf2png/'
    if not path.exists(if_path):
        makedirs(if_path)
    else:
        for f in listdir('pdf2png/'):
            remove('pdf2png/'+f)
    
    main() # 多线程

    # tkinter窗口
    wd = Tk()
    wd.title('pdf滤镜')
    w = wd.winfo_screenwidth()
    h = wd.winfo_screenheight()
    font_size = int(h/67.5)

    # 菜单栏
    menu_bar = Menu(wd)
    wd.config(menu=menu_bar)
    resolution_menu = Menu(master=menu_bar, tearoff=0) # 分辨率选项
    menu_bar.add_cascade(label='分辨率', menu=resolution_menu)
    resolution_menu.add_command(label='低清（输出pdf占用空间较少）', command=change_resol_low)
    resolution_menu.add_command(label='一般（默认）', command=change_resol_normal)
    resolution_menu.add_command(label='高清（接近原画）', command=change_resol_high)
    filter_menu = Menu(master=menu_bar, tearoff=0) # 滤镜选项
    menu_bar.add_cascade(label='滤镜', menu=filter_menu)
    filter_menu.add_command(label='反色', command=change_filter_invert)
    filter_menu.add_command(label='灰度', command=change_filter_grayscale)
    filter_menu.add_command(label='去边', command=change_filter_crop)
    filter_menu.add_command(label='增强', command=change_filter_autocontrast)
    filter_menu.add_command(label='跳阶', command=change_filter_posterize)

    # Settings Label
    info_var = StringVar()
    info_var.set(f'滤镜：{FILTER_MODE}\n清晰：{RESOL_MODE}')
    info_lb = Label(wd, textvariable=info_var, font=('Arial', font_size))
    info_lb.grid(row=0, column=0)

    # 按键
    def start_filter():
        global FILTER_STATUS
        FILTER_STATUS = True

    bt = Button(wd, text='确认本设置,\n选择pdf文档', font=('Arial', font_size), command=start_filter)
    bt.grid(row=1, column=1)

    # 转换状态展示Label
    var_01 = StringVar()
    var_01.set('↓↓↓')
    var_10 = StringVar()
    var_10.set('生发剂类广告位\n长年招租 :)')
    Label(wd, textvariable=var_01).grid(row=0, column=1)
    Label(wd, textvariable=var_10, font=('Arial', int(font_size/2))).grid(row=1, column=0)

    wd.protocol('WM_DELETE_WINDOW', close_window)
    wd.mainloop()
    