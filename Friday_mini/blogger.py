#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'Blogger modul for Friday_mini'

__author__ = 'QidiLiu'

from os import system, chdir, listdir, stat, mkdir
from shutil import copy2
from time import strftime, localtime

def formating(file_tag):  # 定义加开头的函数formating
    for f in listdir('.'):  # 读取当前所在文件夹中所有文件

        # 获取当前所处理文件的修改时间，将其格式化并以str格式赋值到modified_time上
        t = localtime(stat(f).st_mtime)
        y = strftime('%Y', t)
        m = strftime('%m', t)
        d = strftime('%d', t)
        H = strftime('%H', t)
        M = strftime('%M', t)
        modified_time = '{y}-{m}-{d} {H}:{M}'.format(
            y=y, m=m, d=d, H=H, M=M)

        with open(f, 'r+', encoding='utf-8') as working_file:  # 打开当前所处理文件
            old = working_file.read()  # 暂存文章正文
            working_file.seek(0)  # 写针归零
            file_title = f[:-3]  # 去掉文件后缀“.md”
            working_file.write('---\n\nlayout: post\ntitle: "{title}"\ndate: {modified_time}\ncomments: true\ntags: \n▸ - {tag}\n---\n\n'.format(
                title=file_title, modified_time=modified_time, tag=file_tag))  # 加开头声明
            working_file.write(old)  # 加入正文

def blogging():  # 用来推送博文的函数
    # 推送状态：开始推送
    blogging_status.set('正在推送博文……')

    # 删除备份文件夹和_posts文件夹中所有文件                                                         
    system('rmdir /s/q C:\\Users\\Qidi\\Work\\blog_backup')
    mkdir('C:\\Users\\Qidi\\Work\\blog_backup')
    mkdir('C:\\Users\\Qidi\\Work\\blog_backup\\ML')  # 创建机器学习文件夹
    mkdir('C:\\Users\\Qidi\\Work\\blog_backup\\NB')  # 创建胡扯文件夹
    mkdir('C:\\Users\\Qidi\\Work\\blog_backup\\PY')  # 创建Python文件夹
    system('rmdir /s/q C:\\Users\\Qidi\\Work\\blog\\source\\_posts')
    mkdir('C:\\Users\\Qidi\\Work\\blog\\source\\_posts')

    # 打开学业文章所在文件夹
    chdir('C:\\Users\\Qidi\\Work\\ZF')
    for position in ['NB']:  # 复制胡扯相关文件夹中所有.md格式文件到备份文件夹
        for f in listdir('.\\'+position):
            if f.endswith('.md'):
                chdir('.\\'+position)
                copy2(f, 'C:\\Users\\Qidi\\Work\\blog_backup\\NB')
                chdir('..')
    for position in ['ML']:  # 复制机器学习相关文件夹中所有.md格式文件到备份文件夹
        for f in listdir('.\\'+position):
            if f.endswith('.md'):
                chdir('.\\'+position)
                copy2(f, 'C:\\Users\\Qidi\\Work\\blog_backup\\ML')
                chdir('..')
    for position in ['PY']:  # 复制Python相关文件夹中所有.md格式文件到备份文件夹
        for f in listdir('.\\'+position):
            if f.endswith('.md'):
                chdir('.\\'+position)
                copy2(f, 'C:\\Users\\Qidi\\Work\\blog_backup\\PY')
                chdir('..')

    # 打开备份文件夹并分别给各种文章加开头声明
    chdir('C:\\Users\\Qidi\\Work\\blog_backup\\NB')
    formating(u'胡扯')
    chdir('C:\\Users\\Qidi\\Work\\blog_backup\\ML')
    formating(u'机器学习')
    chdir('C:\\Users\\Qidi\\Work\\blog_backup\\PY')
    formating(u'Python')

    # 将备份文件夹中所有文章复制到_post文件夹中
    chdir('C:\\Users\\Qidi\\Work\\blog_backup')
    for position in ['NB', 'ML', 'PY']:
        for f in listdir('.\\'+position):
            chdir('.\\'+position)
            copy2(f, 'C:\\Users\\Qidi\\Work\\blog\\source\\_posts')
            chdir('..')

    # 发表文章
    chdir('C:\\Users\\Qidi\\Work\\blog')
    system('hexo clean')
    system('hexo g')
    system('hexo d')

