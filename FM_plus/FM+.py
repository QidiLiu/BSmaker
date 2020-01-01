#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 音乐播放方案抄自“音乐播放器v1.0---董付国”
# Music playback program copied from "music player v1.0---Dong Fuguo"

import os
import pygame
import random
import time
import tkinter.filedialog
import threading
import json


def folder_finder():
    global MUSIC_FOLDER
    MUSIC_FOLDER = tkinter.filedialog.askdirectory()
    json_setting()


def folder_reset():
    global MUSIC_FOLDER
    MUSIC_FOLDER = 'music'
    json_setting()


def json_setting():
    change = {'MUSIC_POSITION': MUSIC_FOLDER}
    json_change = json.dumps(change)
    setting_file = open('setting.json', 'w', encoding='utf-8')
    setting_file.write(json_change)
    setting_file.close()


def play():
    # 定位文件夹中音乐的位置
    musics = [MUSIC_FOLDER + '/' + music
              for music in os.listdir(MUSIC_FOLDER)
              if music.endswith(('.mp3', '.wav', '.ogg'))]
    # 初始化混音器设备
    pygame.mixer.init()
    # 用random函数定位下一首音乐以实现随机播放功能
    while PLAYING:
        if not pygame.mixer.music.get_busy():
            next_music = random.choice(musics)
            pygame.mixer.music.load(next_music.encode())
            pygame.mixer.music.play(1)
            music_name.set('PLAYING - ' + next_music)
        else:
            time.sleep(0.3)


# 关闭窗口时执行的操作
def close_window():
    global PLAYING
    PLAYING = False
    pygame.mixer.music.stop()
    time.sleep(0.3)
    main_window.destroy()
    os._exit(0)


if __name__ == '__main__':
    setting_file = open('setting.json', encoding='utf-8')
    setting = json.load(setting_file)

    main_window = tkinter.Tk()
    main_window.title('FM+')
    main_window.geometry('280x70+400+300')
    main_window.resizable(False, False)

    # 设置音乐文件夹位置
    MUSIC_FOLDER = setting['MUSIC_POSITION']
    setting_file.close()

    # 创建菜单栏以定义音乐文件夹路径
    folder_menu = tkinter.Menu(main_window)
    main_window.config(menu=folder_menu)
    folder_setting = tkinter.Menu(master=folder_menu, tearoff=0)
    folder_menu.add_cascade(label='音乐文件夹设置', menu=folder_setting)
    folder_setting.add_command(label='音乐文件夹路径', command=folder_finder)
    folder_setting.add_command(label='重置为默认路径', command=folder_reset)

    music_name = tkinter.StringVar(main_window, value='暂时没有播放音乐...')
    label_name = tkinter.Label(main_window, textvariable=music_name)
    label_name.place(x=0, y=40, width=270, height=20)

    pause_resume = tkinter.StringVar(main_window, value='NotSet')
    PLAYING = False

    # 播放按钮

    def play_click():
        global PLAYING
        PLAYING = True

        # 创建一个线程来播放音乐，当前主线程用来接收用户操作
        play_thread = threading.Thread(target=play)
        play_thread.start()

        # 根据情况禁用和启用相应按钮
        play_button['state'] = 'disabled'
        stop_button['state'] = 'normal'
        pause_button['state'] = 'normal'
        next_button['state'] = 'normal'

        pause_resume.set('Pause')

    play_button = tkinter.Button(main_window, text='Play', command=play_click)
    play_button.place(x=20, y=10, width=50, height=20)

    # 停止按钮

    def stop_click():
        global PLAYING
        PLAYING = False

        pygame.mixer.music.stop()
        music_name.set('暂时没有播放音乐')

        play_button['state'] = 'normal'
        stop_button['state'] = 'disabled'
        pause_button['state'] = 'disabled'
        next_button['state'] = 'disabled'

    stop_button = tkinter.Button(main_window, text='Stop', command=stop_click)
    stop_button.place(x=80, y=10, width=50, height=20)
    stop_button['state'] = 'disabled'

    # 暂停与恢复键

    def pause_click():
        if pause_resume.get() == 'Pause':
            pygame.mixer.music.pause()
            pause_resume.set('Resume')
        elif pause_resume.get() == 'Resume':
            pygame.mixer.music.unpause()
            pause_resume.set('Pause')

    pause_button = tkinter.Button(
        main_window, textvariable=pause_resume, command=pause_click)
    pause_button.place(x=140, y=10, width=50, height=20)
    pause_button['state'] = 'disabled'

    # 下一首音乐

    def next_click():
        global PLAYING
        PLAYING = False
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        play_click()

    next_button = tkinter.Button(main_window, text='Next', command=next_click)
    next_button.place(x=200, y=10, width=50, height=20)
    next_button['state'] = 'disabled'

    main_window.protocol('WM_DELETE_WINDOW', close_window)

    # 启动消息循环
    main_window.mainloop()
