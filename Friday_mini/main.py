#/usr/bin/env python3
# -*- coding: utf-8 -*-

'Pomodoro + binaryclock for my Surface Go'

__author__ = 'QidiLiu'

import win32api

from win32con import KEYEVENTF_KEYUP
from time import sleep, time, strftime, localtime
from tkinter import Frame, IntVar, StringVar, Label, Tk, Button, PhotoImage, Toplevel, Entry, LEFT, RIGHT
from threading import Thread
from random import choice
from os import _exit, listdir
from json import load, dumps
from pygame import mixer
from binary_clock import Create_blocks
from blogger import blogging
from mission import Mission

with open('settings.json', 'r') as f:
    settings = load(f)
WAIT_TIME = settings['WAIT_TIME']
PAUSE = settings['PAUSE']
WINDOW_STATUS = True
CLOCK_STATUS = False
MUSIC_FOLDER = 'music'
POMODORO_STATUS = 'off'
PLAYING = False
BLOGGER_STATUS = False
REST_TIME = 0
COLUMN_1 = [0, 0, 0, 0]
COLUMN_2 = [0, 0, 0, 0]
COLUMN_3 = [0, 0, 0, 0]
COLUMN_4 = [0, 0, 0, 0]
REST_TMD = False
FULL_SCREEN = True

# 定位文件夹中音乐的位置
musics = [MUSIC_FOLDER + '/' + music
          for music in listdir(MUSIC_FOLDER)
          if music.endswith(('.mp3', '.wav', '.ogg'))]
# 初始化混音器设备
mixer.init()


def timer():  # 番茄钟的计时器
    global POMODORO_STATUS, REST_TIME, REST_TMD, PLAYING
    while WINDOW_STATUS:
        if POMODORO_STATUS == 'off':
            pass
        elif POMODORO_STATUS == 'working' and REST_TIME < 0:
            def rest_button():
                global REST_TMD
                REST_TMD = True
                rest_button.destroy()
            if FULL_SCREEN:
                OK_img = PhotoImage(file='assets/ok.gif')
            else:
                OK_img = PhotoImage(file='assets/ok_small.gif')
            rest_button = Button(info_frame, image=OK_img, command=rest_button, height=block_size*x, width=block_size*x)
            rest_button.place(x=block_size*1.5, y=block_size*3.5 , anchor='center')
            pomodoro_info.set('歇会儿吧')
            PLAYING = True # 开启音乐播放器
            while REST_TMD is False:
                info_frame.config(bg='gray')
                status_label.config(bg='gray')
                blogger_label.config(bg='gray')
                sleep(0.5)
                info_frame.config(bg='white')
                status_label.config(bg='white')
                blogger_label.config(bg='white')
                sleep(0.5)
            if FULL_SCREEN:
                cup_img = PhotoImage(file='assets/coffee_cup.gif')
            else:
                cup_img = PhotoImage(file='assets/coffee_cup_small.gif')
            cup_label = Label(info_frame, image=cup_img, height=block_size*x, width=block_size*x)
            cup_label.place(x=block_size*1.5, y=block_size*3.5, anchor='center')
            POMODORO_STATUS = 'resting'
        elif POMODORO_STATUS == 'resting':
            info_frame.config(bg=original_bg)
            status_label.config(bg=original_bg)
            blogger_label.config(bg=original_bg)
            sleep(PAUSE*60)
            PLAYING = False # 关闭音乐播放器
            mixer.music.stop()
            REST_TMD = False
            pomodoro_info.set('继续？')
            cup_label.destroy()
            POMODORO_STATUS = 'off'
            pomodoro_button['state'] = 'normal'
        else:
            REST_TIME = ((WAIT_TIME * 60) - (time() - START_TIME))
            pomodoro_info.set(str(int(REST_TIME/60)) + '分' +
                              str(int(REST_TIME - ((int(REST_TIME/60)) * 60))) + '秒')
            sleep(0.3)  # 这步是为了防止计时循环过于频繁导致的卡顿

def refresh():  # 实时获取时间并将其转化16个正方形的颜色组合
    global bc
    while WINDOW_STATUS:
        if CLOCK_STATUS:
            bc.get_time()
        else:
            pass

def keep_awake():  # 模拟按键输入的线程
    while WINDOW_STATUS:
        win32api.keybd_event(20, 0, 0, 0)
        win32api.keybd_event(20, 0, KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(20, 0, 0, 0)
        win32api.keybd_event(20, 0, KEYEVENTF_KEYUP, 0)
        sleep(270)

def play():  # 音乐播放模块
    while WINDOW_STATUS:
        # 用random函数定位下一首音乐以实现随机播放功能
        while PLAYING:
            if not mixer.music.get_busy():
                next_music = choice(musics)
                mixer.music.load(next_music.encode())
                mixer.music.play(1)
            else:
                sleep(0.1)

def blogger():  # 用于推送博文并修改推送显示状态
    global BLOGGER_STATUS
    while WINDOW_STATUS:
        if BLOGGER_STATUS:
            blogging_status.set('正在准备推送博文……')
            blogging()
            blogging_status.set('已成功推送博文√')
            BLOGGER_STATUS = False
        else:
            sleep(0.3)

def main():  # 多线程安排一哈
    Thread(target=timer).start()
    Thread(target=refresh).start()
    Thread(target=keep_awake).start()
    Thread(target=play).start()
    Thread(target=blogger).start()

def close_window(n):  # 关闭程序时终止进程
    global CLOCK_STATUS, WINDOW_STATUS, PLAYING
    CLOCK_STATUS = False
    WINDOW_STATUS = False
    PLAYING = False
    mixer.music.stop()
    sleep(0.3)
    main_window.destroy()
    _exit(0)

if __name__ == '__main__':
    main()

    # 窗口main_window的开头
    main_window = Tk()
    main_window.title('星期五+')
    if FULL_SCREEN:
        block_size = int(main_window.winfo_screenheight()/4)
        main_window.geometry(str(block_size*6)+'x'+str(block_size*4))
        main_window.overrideredirect(True)

    # 16个时间显示正方形
    bc = Create_blocks(main_window, block_size)

    # 开启二进制钟
    CLOCK_STATUS = True

    # 信息和按键展示框
    info_frame = Frame(main_window, height=block_size*4, width=block_size*2)
    info_frame.place(x=block_size*5, y=block_size*2, anchor='center')
    original_bg = info_frame.cget('bg')

    # 博文推送信息框和番茄钟信息框
    blogging_status = StringVar()
    blogger_label = Label(info_frame, textvariable=blogging_status)
    blogger_label.place(x=block_size, y=block_size*0.5, anchor='center')
    pomodoro_info = StringVar()
    status_label = Label(info_frame, textvariable=pomodoro_info, font=('Helvetica', 24))
    status_label.place(x=block_size, y=block_size, anchor='center')

    # 设置
    def setting_time():
        setting_wd = Toplevel()
        setting_wd.title('番茄钟设置')
        row1 = Frame(setting_wd)
        row1.pack(fill='x')
        setting_lb_1 = Label(row1, text='番茄钟时长：')
        setting_lb_1.pack(side=LEFT)
        time_entry_var = IntVar()
        time_entry_var.set(WAIT_TIME)
        time_entry = Entry(row1, textvariable=time_entry_var, width=20)
        time_entry.pack(side=LEFT)
        row2 = Frame(setting_wd)
        row2.pack(fill='x')
        setting_lb_2 = Label(row2, text='休息的时长：')
        setting_lb_2.pack(side=LEFT)
        pause_entry_var = IntVar()
        pause_entry_var.set(PAUSE)
        pause_entry= Entry(row2, textvariable=pause_entry_var, width=20)
        pause_entry.pack(side=LEFT)
        row3 = Frame(setting_wd)
        row3.pack(fill='x')
        def cancel_change():
            setting_wd.destroy()
        cancel_button = Button(row3, text='      取消      ', command=cancel_change)
        cancel_button.pack(side=LEFT)
        def confirm_change():
            global WAIT_TIME, PAUSE
            WAIT_TIME = int(time_entry.get()) 
            PAUSE = int(pause_entry.get())
            settings['WAIT_TIME'] = WAIT_TIME
            settings['PAUSE'] = PAUSE
            with open('settings.json', 'w') as f:
                f.write(dumps(settings))
            setting_wd.destroy()
        confirm_button = Button(row3, text='      确定      ', command=confirm_change)
        confirm_button.pack(side=RIGHT)
    x = 0.97 # 这个系数用于微调4个键的大小
    setting_img = PhotoImage(file='assets/setting.gif')
    setting_button = Button(info_frame, image=setting_img, command=setting_time, height=block_size*x, width=block_size*x)
    setting_button.place(x=block_size*0.5, y=block_size*2.5, anchor='center')

    # 待办事项
    reminder_img = PhotoImage(file='assets/reminder.gif')
    def dp_wd():
        dp_wd = Toplevel()
        dp_wd.title('待办事项')
        to_do_list = Frame(dp_wd)
        to_do_list.pack(fill='x')
        add_mission = Frame(dp_wd)
        add_mission.pack(fill='x')

        with open('data.json', 'r') as f:
            data = load(f)

        for i in range(len(data)):
            locals()[data[i]['MID']] = Mission(data[i]['content'], 'Top')
            locals()[data[i]['MID']].display(to_do_list)

        new_mission_entry = Entry(add_mission, width=20)
        new_mission_entry.pack(side=LEFT)
        def add_mission_button():
            locals()['MS'+strftime('%Y%m%d%H%M%S', localtime())] = Mission(new_mission_entry.get(), 'Top')
            locals()['MS'+strftime('%Y%m%d%H%M%S', localtime())].display(to_do_list)
            def is_MS(s):
                if list(s)[0] == 'M' and list(s)[1] == 'S':
                    return s
            new_list = list(filter(is_MS, list(locals())))
            def ms2dict(ms):
                return {
                        'MID': 'MS'+ms.MID,
                        'content': ms.content
                        }
            for i in range(len(new_list)):
                new_list[i] = ms2dict(locals()[new_list[i]])
            with open('data.json', 'w') as f:
                f.write(dumps(new_list))

        Button(add_mission, text='添加', command=add_mission_button).pack(side=RIGHT)

        test_list = [{'MID': 'MS002', 'content': 'Test suceed!'}, {'MID': 'MS003', 'content': 'Succed again!'}]
    reminder_button = Button(info_frame, image=reminder_img, command=dp_wd, height=block_size*x, width=block_size*x)
    reminder_button.place(x=block_size*1.5, y=block_size*2.5, anchor='center')

    # 关闭
    close_img = PhotoImage(file='assets/cancel.gif')
    def close_wd():
        close_window(0)
    close_button = Button(info_frame, image=close_img, command=close_wd, height=block_size*x, width=block_size*x)
    close_button.place(x=block_size*0.5, y=block_size*3.5, anchor='center')
    main_window.protocol('WM_DELETE_WINDOW', close_wd)

    # 番茄钟
    def start_pomodoro():  # 按键pomodoro_button
        global REST_TIME, START_TIME, POMODORO_STATUS
        REST_TIME = 0
        START_TIME = time()
        POMODORO_STATUS = 'working'
        pomodoro_button['state'] = 'disabled'
    tomato_img = PhotoImage(file='assets/tomato.gif')
    pomodoro_button = Button(info_frame, image=tomato_img, command=start_pomodoro, height=block_size*x, width=block_size*x)
    pomodoro_button.place(x=block_size*1.5, y=block_size*3.5, anchor='center')

    # 推送博文按F1键
    def deploy_blog():
        global BLOGGER_STATUS
        BLOGGER_STATUS = True
    main_window.bind('<F1>', deploy_blog)

    # 设回车键为全屏转换键
    def refresh():
        global bc
        main_window.geometry(str(block_size*6)+'x'+str(block_size*4))
        main_window.overrideredirect(FULL_SCREEN)
        bc = Create_blocks(main_window, block_size)
        info_frame.config(height=block_size*4, width=block_size*2)
        info_frame.place(x=block_size*5, y=block_size*2, anchor='center')
        blogger_label.place(x=block_size, y=block_size*0.5, anchor='center')
        status_label.place(x=block_size, y=block_size, anchor='center')
        status_label.config(font=('Helvetica', int(block_size/10)))
        setting_button.place(x=block_size*0.5, y=block_size*2.5, anchor='center')
        setting_button.config(image=setting_img, height=block_size*x, width=block_size*x)
        reminder_button.place(x=block_size*1.5, y=block_size*2.5, anchor='center')
        reminder_button.config(image=reminder_img, height=block_size*x, width=block_size*x)
        close_button.place(x=block_size*0.5, y=block_size*3.5, anchor='center')
        close_button.config(image=close_img, height=block_size*x, width=block_size*x)
        pomodoro_button.place(x=block_size*1.5, y=block_size*3.5, anchor='center')
        pomodoro_button.config(image=tomato_img, height=block_size*x, width=block_size*x)

    def change_size(n):
        global block_size, FULL_SCREEN, close_img, tomato_img, setting_img, reminder_img
        if FULL_SCREEN:
            FULL_SCREEN = False
            block_size = int(main_window.winfo_screenheight()/8)
            close_img = PhotoImage(file='assets/cancel_small.gif')
            tomato_img = PhotoImage(file='assets/tomato_small.gif')
            setting_img = PhotoImage(file='assets/setting_small.gif')
            reminder_img = PhotoImage(file='assets/reminder_small.gif')
            refresh()
        else:
            FULL_SCREEN = True
            block_size = int(main_window.winfo_screenheight()/4)
            close_img = PhotoImage(file='assets/cancel.gif')
            tomato_img = PhotoImage(file='assets/tomato.gif')
            setting_img = PhotoImage(file='assets/setting.gif')
            reminder_img = PhotoImage(file='assets/reminder.gif')
            refresh()
    main_window.bind('<Return>', change_size)

    # 关闭程序的原本方式
    main_window.bind('<Escape>', close_window)

    # 窗口main_window的结尾
    main_window.mainloop()
