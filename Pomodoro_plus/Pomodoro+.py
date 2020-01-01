#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 音乐播放方案抄自“音乐播放器v1.0---董付国”
# Music playback program copied from "music player v1.0---Dong Fuguo"

from threading import Thread
from time import sleep, time
from os import listdir, _exit
from json import dumps, load
from random import choice
from pygame import mixer
from tkinter import messagebox, filedialog, Tk, Menu, Label, StringVar, Entry, Button, Checkbutton
from os import _exit
from win32con import KEYEVENTF_KEYUP
import win32api

MUSIC_FOLDER = 'music'
MISSION_QUANTITY = 0
COMPLETED_MISSION = 0
WINDOW_STATUS = True
PLAYING = False
TIMER_STATUS = 'off'
TOTAL_TIME = 0
REST_TIME = 0
window_geometry = '350x90'
CHECK_1 = 0
CHECK_2 = 0
CHECK_3 = 0
CHECK_4 = 0
CHECK_5 = 0
CHECK_6 = 0
CHECK_7 = 0
CHECK_8 = 0
CHECK_9 = 0
CHECK_10 = 0
CHECK_11 = 0
CHECK_12 = 0


def folder_finder():
    global MUSIC_FOLDER
    MUSIC_FOLDER = filedialog.askdirectory()
    json_setting()


def folder_reset():
    global MUSIC_FOLDER
    MUSIC_FOLDER = 'music'
    json_setting()


def json_setting():
    change = {'MUSIC_POSITION': MUSIC_FOLDER}
    json_change = dumps(change)
    setting_file = open('setting.json', 'w', encoding='utf-8')
    setting_file.write(json_change)
    setting_file.close()


def play():
    while WINDOW_STATUS:
        # 定位文件夹中音乐的位置
        musics = [MUSIC_FOLDER + '/' + music
                  for music in listdir(MUSIC_FOLDER)
                  if music.endswith(('.mp3', '.wav', '.ogg'))]
        # 初始化混音器设备
        mixer.init()
        # 用random函数定位下一首音乐以实现随机播放功能
        while PLAYING:
            if not mixer.music.get_busy():
                next_music = choice(musics)
                mixer.music.load(next_music.encode())
                mixer.music.play(1)
            else:
                sleep(0.3)


def timer():
    global TIMER_STATUS, REST_TIME, PLAYING
    while WINDOW_STATUS:
        if TIMER_STATUS == 'off':
            pass
        elif TIMER_STATUS == 'working' and REST_TIME < 0:
            TIMER_STATUS = 'resting'
            pause()
        elif TIMER_STATUS == 'resting':
            information.set('歇一会吧~')
            PLAYING = True
            sleep(5*60)
            PLAYING = False
            mixer.music.stop()
            ask_prepared.place(x=150, y=40, anchor='center')
            prepared_button.place(x=300, y=40, anchor='center')
            main_window.bind('<Return>', prepared_enter)
            TIMER_STATUS = 'preparing'
        elif TIMER_STATUS == 'preparing':
            pass
        elif TIMER_STATUS == 'ending':
            information.set('KEEP CALM AND CARRY ON\n\n_(:3」∠)_')
            sleep(5)
            close_program()
        else:
            REST_TIME = ((WAIT_TIME * 60) - (time() - START_TIME))
            information.set('任务进行中，距离提醒还有：' + str(int(REST_TIME / 60)) + '分' + str(
                int(REST_TIME - ((int(REST_TIME / 60)) * 60))) + '秒')
            sleep(0.1)


def pause():
    global TOTAL_TIME
    stop_time = time()
    TOTAL_TIME += (stop_time - START_TIME)


def prepared_enter(n):
    prepared()


def prepared():
    ask_prepared.place(x=175, y=-50, anchor='center')
    prepared_button.place(x=175, y=-50, anchor='center')
    remind()


def remind():
    global TIMER_STATUS, START_TIME, REST_TIME
    REST_TIME = 0
    START_TIME = time()
    TIMER_STATUS = 'working'


def keep_awake():  # 模拟按键输入的线程
    while WINDOW_STATUS:
        win32api.keybd_event(20, 0, 0, 0)
        win32api.keybd_event(20, 0, KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(20, 0, 0, 0)
        win32api.keybd_event(20, 0, KEYEVENTF_KEYUP, 0)
        sleep(270)


def main():
    Thread(target=timer).start()
    Thread(target=play).start()
    Thread(target=keep_awake).start()


def close_program():
    global WINDOW_STATUS, PLAYING
    WINDOW_STATUS = False
    PLAYING = False
    mixer.music.stop()
    sleep(0.3)
    main_window.destroy()
    _exit(0)


if __name__ == '__main__':
    main()

    setting_file = open('setting.json', encoding='utf-8')
    setting = load(setting_file)

    # 生成一个窗口
    main_window = Tk()
    main_window.title('番茄钟+')
    main_window.geometry(window_geometry)
    main_window.resizable(False, False)

    # 设置音乐文件夹位置
    MUSIC_FOLDER = setting['MUSIC_POSITION']
    setting_file.close()

    # 创建菜单栏以定义音乐文件夹路径
    folder_menu = Menu(main_window)
    main_window.config(menu=folder_menu)
    folder_setting = Menu(master=folder_menu, tearoff=0)
    folder_menu.add_cascade(label='音乐文件夹设置', menu=folder_setting)
    folder_setting.add_command(label='音乐文件夹路径', command=folder_finder)
    folder_setting.add_command(label='重置为默认路径', command=folder_reset)

    Label(main_window, text='任务描述').place(x=35, y=20, anchor='center')

    def vote_1():
        global CHECK_1, TOTAL_TIME, COMPLETED_MISSION, TIMER_STATUS
        if CHECK_1 == 0:
            CHECK_1 = 1
            COMPLETED_MISSION += 1
            if MISSION_QUANTITY == COMPLETED_MISSION:
                TIMER_STATUS = 'ending'
            else:
                TIMER_STATUS = 'resting'
            pause()
            mission_1_time.set(
                str(int(TOTAL_TIME / 60)) + '分' + str(int(TOTAL_TIME - ((int(TOTAL_TIME / 60)) * 60))) + '秒')
            TOTAL_TIME = 0
        else:
            CHECK_1 = 0
            COMPLETED_MISSION -= 1

    def vote_2():
        global CHECK_2, TOTAL_TIME, COMPLETED_MISSION, TIMER_STATUS
        if CHECK_2 == 0:
            CHECK_2 = 1
            COMPLETED_MISSION += 1
            if MISSION_QUANTITY == COMPLETED_MISSION:
                TIMER_STATUS = 'ending'
            else:
                TIMER_STATUS = 'resting'
            pause()
            mission_2_time.set(
                str(int(TOTAL_TIME / 60)) + '分' + str(int(TOTAL_TIME - ((int(TOTAL_TIME / 60)) * 60))) + '秒')
            TOTAL_TIME = 0
        else:
            CHECK_2 = 0
            COMPLETED_MISSION -= 1

    def vote_3():
        global CHECK_3, TOTAL_TIME, COMPLETED_MISSION, TIMER_STATUS
        if CHECK_3 == 0:
            CHECK_3 = 1
            COMPLETED_MISSION += 1
            if MISSION_QUANTITY == COMPLETED_MISSION:
                TIMER_STATUS = 'ending'
            else:
                TIMER_STATUS = 'resting'
            pause()
            mission_3_time.set(
                str(int(TOTAL_TIME / 60)) + '分' + str(int(TOTAL_TIME - ((int(TOTAL_TIME / 60)) * 60))) + '秒')
            TOTAL_TIME = 0
        else:
            CHECK_3 = 0
            COMPLETED_MISSION -= 1

    def vote_4():
        global CHECK_4, TOTAL_TIME, COMPLETED_MISSION, TIMER_STATUS
        if CHECK_4 == 0:
            CHECK_4 = 1
            COMPLETED_MISSION += 1
            if MISSION_QUANTITY == COMPLETED_MISSION:
                TIMER_STATUS = 'ending'
            else:
                TIMER_STATUS = 'resting'
            pause()
            mission_4_time.set(
                str(int(TOTAL_TIME / 60)) + '分' + str(int(TOTAL_TIME - ((int(TOTAL_TIME / 60)) * 60))) + '秒')
            TOTAL_TIME = 0
        else:
            CHECK_4 = 0
            COMPLETED_MISSION -= 1

    def vote_5():
        global CHECK_5, TOTAL_TIME, COMPLETED_MISSION, TIMER_STATUS
        if CHECK_5 == 0:
            CHECK_5 = 1
            COMPLETED_MISSION += 1
            if MISSION_QUANTITY == COMPLETED_MISSION:
                TIMER_STATUS = 'ending'
            else:
                TIMER_STATUS = 'resting'
            pause()
            mission_5_time.set(
                str(int(TOTAL_TIME / 60)) + '分' + str(int(TOTAL_TIME - ((int(TOTAL_TIME / 60)) * 60))) + '秒')
            TOTAL_TIME = 0
        else:
            CHECK_5 = 0
            COMPLETED_MISSION -= 1

    def vote_6():
        global CHECK_6, TOTAL_TIME, COMPLETED_MISSION, TIMER_STATUS
        if CHECK_6 == 0:
            CHECK_6 = 1
            COMPLETED_MISSION += 1
            if MISSION_QUANTITY == COMPLETED_MISSION:
                TIMER_STATUS = 'ending'
            else:
                TIMER_STATUS = 'resting'
            pause()
            mission_6_time.set(
                str(int(TOTAL_TIME / 60)) + '分' + str(int(TOTAL_TIME - ((int(TOTAL_TIME / 60)) * 60))) + '秒')
            TOTAL_TIME = 0
        else:
            CHECK_6 = 0
            COMPLETED_MISSION -= 1

    def vote_7():
        global CHECK_7, TOTAL_TIME, COMPLETED_MISSION, TIMER_STATUS
        if CHECK_7 == 0:
            CHECK_7 = 1
            COMPLETED_MISSION += 1
            if MISSION_QUANTITY == COMPLETED_MISSION:
                TIMER_STATUS = 'ending'
            else:
                TIMER_STATUS = 'resting'
            pause()
            mission_7_time.set(
                str(int(TOTAL_TIME / 60)) + '分' + str(int(TOTAL_TIME - ((int(TOTAL_TIME / 60)) * 60))) + '秒')
            TOTAL_TIME = 0
        else:
            CHECK_7 = 0
            COMPLETED_MISSION -= 1

    def vote_8():
        global CHECK_8, TOTAL_TIME, COMPLETED_MISSION, TIMER_STATUS
        if CHECK_8 == 0:
            CHECK_8 = 1
            COMPLETED_MISSION += 1
            if MISSION_QUANTITY == COMPLETED_MISSION:
                TIMER_STATUS = 'ending'
            else:
                TIMER_STATUS = 'resting'
            pause()
            mission_8_time.set(
                str(int(TOTAL_TIME / 60)) + '分' + str(int(TOTAL_TIME - ((int(TOTAL_TIME / 60)) * 60))) + '秒')
            TOTAL_TIME = 0
        else:
            CHECK_8 = 0
            COMPLETED_MISSION -= 1

    def vote_9():
        global CHECK_9, TOTAL_TIME, COMPLETED_MISSION, TIMER_STATUS
        if CHECK_9 == 0:
            CHECK_9 = 1
            COMPLETED_MISSION += 1
            if MISSION_QUANTITY == COMPLETED_MISSION:
                TIMER_STATUS = 'ending'
            else:
                TIMER_STATUS = 'resting'
            pause()
            mission_9_time.set(
                str(int(TOTAL_TIME / 60)) + '分' + str(int(TOTAL_TIME - ((int(TOTAL_TIME / 60)) * 60))) + '秒')
            TOTAL_TIME = 0
        else:
            CHECK_9 = 0
            COMPLETED_MISSION -= 1

    def vote_10():
        global CHECK_10, TOTAL_TIME, COMPLETED_MISSION, TIMER_STATUS
        if CHECK_10 == 0:
            CHECK_10 = 1
            COMPLETED_MISSION += 1
            if MISSION_QUANTITY == COMPLETED_MISSION:
                TIMER_STATUS = 'ending'
            else:
                TIMER_STATUS = 'resting'
            pause()
            mission_10_time.set(
                str(int(TOTAL_TIME / 60)) + '分' + str(int(TOTAL_TIME - ((int(TOTAL_TIME / 60)) * 60))) + '秒')
            TOTAL_TIME = 0
        else:
            CHECK_10 = 0
            COMPLETED_MISSION -= 1

    def vote_11():
        global CHECK_11, TOTAL_TIME, COMPLETED_MISSION, TIMER_STATUS
        if CHECK_11 == 0:
            CHECK_11 = 1
            COMPLETED_MISSION += 1
            if MISSION_QUANTITY == COMPLETED_MISSION:
                TIMER_STATUS = 'ending'
            else:
                TIMER_STATUS = 'resting'
            pause()
            mission_11_time.set(
                str(int(TOTAL_TIME / 60)) + '分' + str(int(TOTAL_TIME - ((int(TOTAL_TIME / 60)) * 60))) + '秒')
            TOTAL_TIME = 0
        else:
            CHECK_11 = 0
            COMPLETED_MISSION -= 1

    def vote_12():
        global CHECK_12, TOTAL_TIME, COMPLETED_MISSION, TIMER_STATUS
        if CHECK_12 == 0:
            CHECK_12 = 1
            COMPLETED_MISSION += 1
            if MISSION_QUANTITY == COMPLETED_MISSION:
                TIMER_STATUS = 'ending'
            else:
                TIMER_STATUS = 'resting'
            pause()
            mission_12_time.set(
                str(int(TOTAL_TIME / 60)) + '分' + str(int(TOTAL_TIME - ((int(TOTAL_TIME / 60)) * 60))) + '秒')
            TOTAL_TIME = 0
        else:
            CHECK_12 = 0
            COMPLETED_MISSION -= 1

    # 任务显示栏
    checkbutton_1 = Checkbutton(main_window, command=vote_1)
    mission_1_label = Label(main_window, font=('Arial', 12))
    mission_1_label.place(x=30, y=100, anchor='w')
    mission_1_time = StringVar()
    mission_1_time_label = Label(
        main_window, textvariable=mission_1_time)
    mission_1_time_label.place(x=340, y=100, anchor='e')

    checkbutton_2 = Checkbutton(main_window, command=vote_2)
    mission_2_label = Label(main_window, font=('Arial', 12))
    mission_2_label.place(x=30, y=130, anchor='w')
    mission_2_time = StringVar()
    mission_2_time_label = Label(
        main_window, textvariable=mission_2_time)
    mission_2_time_label.place(x=340, y=130, anchor='e')

    checkbutton_3 = Checkbutton(main_window, command=vote_3)
    mission_3_label = Label(main_window, font=('Arial', 12))
    mission_3_label.place(x=30, y=160, anchor='w')
    mission_3_time = StringVar()
    mission_3_time_label = Label(
        main_window, textvariable=mission_3_time)
    mission_3_time_label.place(x=340, y=160, anchor='e')

    checkbutton_4 = Checkbutton(main_window, command=vote_4)
    mission_4_label = Label(main_window, font=('Arial', 12))
    mission_4_label.place(x=30, y=190, anchor='w')
    mission_4_time = StringVar()
    mission_4_time_label = Label(
        main_window, textvariable=mission_4_time)
    mission_4_time_label.place(x=340, y=190, anchor='e')

    checkbutton_5 = Checkbutton(main_window, command=vote_5)
    mission_5_label = Label(main_window, font=('Arial', 12))
    mission_5_label.place(x=30, y=220, anchor='w')
    mission_5_time = StringVar()
    mission_5_time_label = Label(
        main_window, textvariable=mission_5_time)
    mission_5_time_label.place(x=340, y=220, anchor='e')

    checkbutton_6 = Checkbutton(main_window, command=vote_6)
    mission_6_label = Label(main_window, font=('Arial', 12))
    mission_6_label.place(x=30, y=250, anchor='w')
    mission_6_time = StringVar()
    mission_6_time_label = Label(
        main_window, textvariable=mission_6_time)
    mission_6_time_label.place(x=340, y=250, anchor='e')

    checkbutton_7 = Checkbutton(main_window, command=vote_7)
    mission_7_label = Label(main_window, font=('Arial', 12))
    mission_7_label.place(x=30, y=280, anchor='w')
    mission_7_time = StringVar()
    mission_7_time_label = Label(
        main_window, textvariable=mission_7_time)
    mission_7_time_label.place(x=340, y=280, anchor='e')

    checkbutton_8 = Checkbutton(main_window, command=vote_8)
    mission_8_label = Label(main_window, font=('Arial', 12))
    mission_8_label.place(x=30, y=310, anchor='w')
    mission_8_time = StringVar()
    mission_8_time_label = Label(
        main_window, textvariable=mission_8_time)
    mission_8_time_label.place(x=340, y=310, anchor='e')

    checkbutton_9 = Checkbutton(main_window, command=vote_9)
    mission_9_label = Label(main_window, font=('Arial', 12))
    mission_9_label.place(x=30, y=340, anchor='w')
    mission_9_time = StringVar()
    mission_9_time_label = Label(
        main_window, textvariable=mission_9_time)
    mission_9_time_label.place(x=340, y=340, anchor='e')

    checkbutton_10 = Checkbutton(main_window, command=vote_10)
    mission_10_label = Label(main_window, font=('Arial', 12))
    mission_10_label.place(x=30, y=370, anchor='w')
    mission_10_time = StringVar()
    mission_10_time_label = Label(
        main_window, textvariable=mission_10_time)
    mission_10_time_label.place(x=340, y=370, anchor='e')

    checkbutton_11 = Checkbutton(main_window, command=vote_11)
    mission_11_label = Label(main_window, font=('Arial', 12))
    mission_11_label.place(x=30, y=400, anchor='w')
    mission_11_time = StringVar()
    mission_11_time_label = Label(
        main_window, textvariable=mission_11_time)
    mission_11_time_label.place(x=340, y=400, anchor='e')

    checkbutton_12 = Checkbutton(main_window, command=vote_12)
    mission_12_label = Label(main_window, font=('Arial', 12))
    mission_12_label.place(x=30, y=430, anchor='w')
    mission_12_time = StringVar()
    mission_12_time_label = Label(
        main_window, textvariable=mission_12_time)
    mission_12_time_label.place(x=340, y=430, anchor='e')

    # 在任务添加栏中添加任务

    def mission_enter(n):
        add_mission()

    def add_mission():
        global INPUT_MISSION, MISSION_QUANTITY
        if MISSION_QUANTITY < 12:
            INPUT_MISSION = mission_entry.get()
            if INPUT_MISSION == '':
                messagebox.showerror(
                    title='警告', message='任务输入有误，请重新输入')
            else:
                if MISSION_QUANTITY == 0:
                    mission_1_label.config(text=INPUT_MISSION)
                    checkbutton_1.place(x=10, y=100, anchor='w')
                    main_window.geometry('350x130')
                elif MISSION_QUANTITY == 1:
                    mission_2_label.config(text=INPUT_MISSION)
                    checkbutton_2.place(x=10, y=130, anchor='w')
                    main_window.geometry('350x160')
                elif MISSION_QUANTITY == 2:
                    mission_3_label.config(text=INPUT_MISSION)
                    checkbutton_3.place(x=10, y=160, anchor='w')
                    main_window.geometry('350x190')
                elif MISSION_QUANTITY == 3:
                    mission_4_label.config(text=INPUT_MISSION)
                    checkbutton_4.place(x=10, y=190, anchor='w')
                    main_window.geometry('350x220')
                elif MISSION_QUANTITY == 4:
                    mission_5_label.config(text=INPUT_MISSION)
                    checkbutton_5.place(x=10, y=220, anchor='w')
                    main_window.geometry('350x250')
                elif MISSION_QUANTITY == 5:
                    mission_6_label.config(text=INPUT_MISSION)
                    checkbutton_6.place(x=10, y=250, anchor='w')
                    main_window.geometry('350x280')
                elif MISSION_QUANTITY == 6:
                    mission_7_label.config(text=INPUT_MISSION)
                    checkbutton_7.place(x=10, y=280, anchor='w')
                    main_window.geometry('350x310')
                elif MISSION_QUANTITY == 7:
                    mission_8_label.config(text=INPUT_MISSION)
                    checkbutton_8.place(x=10, y=310, anchor='w')
                    main_window.geometry('350x340')
                elif MISSION_QUANTITY == 8:
                    mission_9_label.config(text=INPUT_MISSION)
                    checkbutton_9.place(x=10, y=340, anchor='w')
                    main_window.geometry('350x370')
                elif MISSION_QUANTITY == 9:
                    mission_10_label.config(text=INPUT_MISSION)
                    checkbutton_10.place(x=10, y=370, anchor='w')
                    main_window.geometry('350x400')
                elif MISSION_QUANTITY == 10:
                    mission_11_label.config(text=INPUT_MISSION)
                    checkbutton_11.place(x=10, y=400, anchor='w')
                    main_window.geometry('350x430')
                else:
                    mission_12_label.config(text=INPUT_MISSION)
                    checkbutton_12.place(x=10, y=430, anchor='w')
                    main_window.geometry('350x460')
                MISSION_QUANTITY += 1
                mission_entry.delete(0, 'end')
        else:
            messagebox.showerror(title='警告', message='任务数量已达上限！')

    # 添加按钮
    add_button = Button(main_window, text='添加+', command=add_mission)
    add_button.place(x=315, y=20, anchor='center')
    # 任务输入框
    mission_entry = Entry(main_window, width=25, show=None)
    mission_entry.place(x=175, y=20, anchor='center')
    # 时间表述标签
    Label(main_window, text='时间（分）').place(x=35, y=60, anchor='center')
    # 时间输入框
    time_entry = Entry(main_window, width=25, show=None)
    time_entry.place(x=175, y=60, anchor='center')
    mission_entry.bind('<Return>', mission_enter)

    def time_enter(n):
        start()

    def start():
        global INPUT_TIME, WAIT_TIME
        if MISSION_QUANTITY > 0:
            INPUT_TIME = time_entry.get()
            if INPUT_TIME.isdigit() is False and INPUT_TIME != '':
                messagebox.showerror(title='警告', message='输入有误，请重新输入')
            elif INPUT_TIME.isdigit():
                if int(INPUT_TIME) > 60:
                    messagebox.showerror(
                        title='警告', message='输入时间过长，请重新输入')
                elif int(INPUT_TIME) < 15:
                    messagebox.showerror(
                        title='警告', message='输入时间过短，请重新输入')
                else:
                    WAIT_TIME = int(INPUT_TIME)
                    initialization()
            else:
                WAIT_TIME = 25
                initialization()
        else:
            messagebox.showerror(title='警告', message='您还没有添加待办任务')

    def initialization():
        global TIMER_STATUS, START_TIME, REST_TIME
        REST_TIME = 0
        START_TIME = time()
        TIMER_STATUS = 'working'
        information_label.place(x=175, y=40, anchor='center')

    time_entry.bind('<Return>', time_enter)
    # 计时开始按键
    start_button = Button(main_window, text='开始！', command=start)
    start_button.place(x=315, y=60, anchor='center')

    # 计时开始后显示的标签
    information = StringVar()
    information_label = Label(
        main_window, textvariable=information, width=50, height=5)

    # 准备下一次任务的标签和开始键
    ask_prepared = Label(main_window, text='准备好继续开工了么？')
    prepared_button = Button(
        main_window, text='准备好了！', command=prepared)

    main_window.protocol('WM_DELETE_WINDOW', close_program)

    main_window.mainloop()
