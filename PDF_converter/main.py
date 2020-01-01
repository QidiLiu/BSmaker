#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'Convert pdf flies to images with a tkinter GUI'

__author__ = 'QidiLiu'

from tkinter import Tk, Button, Label, Frame, StringVar, filedialog
from json import load, dumps
from pdf2image import convert_from_path
from time import sleep
from os import path, listdir, chdir

from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

LOCAL_SETTINGS = ['','',300]
original_path = path.abspath(path.dirname(__file__))

def ip_conf():
    global LOCAL_SETTINGS
    tem = filedialog.askdirectory()
    if tem != '':
        LOCAL_SETTINGS[0] = tem
    with open('settings.json', 'w') as f:
        f.write(dumps(LOCAL_SETTINGS))
    st.set('')
    ip_fd.set('PDF所在目录为'+LOCAL_SETTINGS[0])

def op_conf():
    global LOCAL_SETTINGS
    tem = filedialog.askdirectory()
    if tem != '':
        LOCAL_SETTINGS[1] = tem
    with open('settings.json', 'w') as f:
        f.write(dumps(LOCAL_SETTINGS))
    st.set('')
    op_fd.set('图片保存到'+LOCAL_SETTINGS[1])

def converter():
    pdf_names = []
    cr_pdfs = []
    cv_button['state'] = 'disabled'
    for file in listdir(LOCAL_SETTINGS[0]):
        if len(file.split('.')) > 1:
            if file.split('.')[1] == 'pdf' or file.split('.')[1] == 'PDF':
                cr_pdfs.append(LOCAL_SETTINGS[0]+'/'+file)
                pdf_names.append(file.split('.')[0])
    for i in range(len(cr_pdfs)):
        images = convert_from_path(cr_pdfs[i], dpi=LOCAL_SETTINGS[2], thread_count=1) 
        for j in range(0, len(images)):
            chdir(LOCAL_SETTINGS[1])
            images[j].save(f'{pdf_names[i]}_{j+1}.png', 'PNG')
            chdir(original_path)
    pdf_names = []
    cr_pdfs = []
    st.set('转换完成')
    cv_button['state'] = 'normal'

def main():
    with open('settings.json', 'r') as f:
        settings = load(f)
        LOCAL_SETTINGS[0] = settings[0]
        if LOCAL_SETTINGS[0] == '':
            LOCAL_SETTINGS[0] = path.abspath(path.dirname(__file__))
        LOCAL_SETTINGS[1] = settings[1]
        if LOCAL_SETTINGS[1] == '':
            LOCAL_SETTINGS[1] = path.abspath(path.dirname(__file__))
        LOCAL_SETTINGS[2] = settings[2]

if __name__ == '__main__':
    main()

    wd = Tk()
    wd.title('PDF转图片（批量处理版） —— github.com/QidiLiu')
    w = wd.winfo_screenwidth()
    h = wd.winfo_screenheight()
    font_size = int(h/67.5)
    wd.geometry(str(int(w/2))+'x'+str(int(h/2)))
    
    info_display = Frame(wd, width=3/8*w)
    info_display.place(x=3/16*w, y=1/8*h, anchor='center')

    ip_fd = StringVar()
    ip_fd.set('PDF所在目录为'+LOCAL_SETTINGS[0])
    ip_folder = Label(info_display, textvariable=ip_fd, font=('Arial', font_size))
    ip_folder.pack()

    op_fd = StringVar()
    op_fd.set('图片保存到'+LOCAL_SETTINGS[1])
    op_folder = Label(info_display, textvariable=op_fd, font=('Arial', font_size))
    op_folder.pack()

    config_frame = Frame(wd, width=1/8*w)
    config_frame.place(x=7/16*w, y=1/8*h, anchor='center')

    ch_ip = Button(config_frame, text='PDF位置设置', command=ip_conf, font=('Arial', font_size))
    ch_ip.pack()

    ch_op = Button(config_frame, text='图片位置设置', command=op_conf, font=('Arial', font_size))
    ch_op.pack()

    st = StringVar()
    status = Label(wd, textvariable=st, font=('Arial', font_size))
    status.place(x=1/4*w, y=1/4*h, anchor='center')
 
    cv_button = Button(wd, text='都neng好了，转吧', command=converter, font=('Arial', font_size))
    cv_button.place(x=1/4*w, y=3/8*h, anchor='center')

    wd.mainloop()
