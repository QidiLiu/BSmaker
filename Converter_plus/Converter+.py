#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread
from time import sleep
from json import dumps, load
from os import _exit
from tkinter import messagebox, Tk, Menu, Label, StringVar, Entry, Button, Listbox

WINDOW_STATUS = False


def mode_setting():
    change = {'CONVERTER_MODE': CONVERTER_MODE}
    json_change = dumps(change)
    file_object = open('function_setting.json', 'w', encoding='utf-8')
    file_object.write(json_change)
    file_object.close()


def arrow():
    while WINDOW_STATUS:
        arrow_string.set('==>  =')
        sleep(0.2)
        arrow_string.set('==>')
        sleep(0.2)
        arrow_string.set('>  ==>')
        sleep(0.2)
        arrow_string.set('=>  ==')
        sleep(0.2)


def close_window():
    main_window.destroy()
    copy_main_window.destroy()
    _exit(0)


def main():
    global ARROW_THREAD
    ARROW_THREAD = Thread(target=arrow)


if __name__ == '__main__':
    main()
    function_file = open('function_setting.json', encoding='utf-8')
    setting = load(function_file)
    # Create main_window
    main_window = Tk()
    main_window.title('Binary Converters')
    main_window.geometry('420x540')
    main_window.resizable(False, False)
    WINDOW_STATUS = True

    # Create a hidden main_window to copy the result to clipboard
    copy_main_window = Tk()
    copy_main_window.withdraw()
    copy_main_window.clipboard_clear()

    # Create a menu_bar_english to change the function and language of this program
    menu_bar_english = Menu(main_window)
    menu_bar_chinese = Menu(main_window)
    menu_bar_german = Menu(main_window)
    main_window.config(menu=menu_bar_english)

    # The initial setting of some text of the functions
    CONVERTER_MODE = setting['CONVERTER_MODE']
    function_file.close()
    SUCCESSFUL_OUTPUT_1 = 'The '
    SUCCESSFUL_OUTPUT_2 = ' binary number of '
    SUCCESSFUL_OUTPUT_3 = ' is '
    SUCCESSFUL_OUTPUT_END = '\nThe Result has been copied'
    FAILED_OUTPUT = 'The number you typed in is wrong, \nplease re-enter and click the button "Confirm"'
    FAILED_TITLE = 'Error'

    def ten_to_sixteen():
        global CONVERTER_MODE
        CONVERTER_MODE = '10 ==> 16'
        input_binary.config(text='10')
        output_binary.config(text='16')
        mode_setting()

    def ten_to_eight():
        global CONVERTER_MODE
        CONVERTER_MODE = '10 ==> 8'
        mode_setting()
        input_binary.config(text='10')
        output_binary.config(text='8')

    def ten_to_two():
        global CONVERTER_MODE
        CONVERTER_MODE = '10 ==> 2'
        mode_setting()
        input_binary.config(text='10')
        output_binary.config(text='2')

    def two_to_sixteen():
        global CONVERTER_MODE
        CONVERTER_MODE = '2 ==> 16'
        mode_setting()
        input_binary.config(text='2')
        output_binary.config(text='16')

    def two_to_eight():
        global CONVERTER_MODE
        CONVERTER_MODE = '2 ==> 8'
        mode_setting()
        input_binary.config(text='2')
        output_binary.config(text='8')

    def two_to_ten():
        global CONVERTER_MODE
        CONVERTER_MODE = '2 ==> 10'
        mode_setting()
        input_binary.config(text='2')
        output_binary.config(text='10')

    def eight_to_sixteen():
        global CONVERTER_MODE
        CONVERTER_MODE = '8 ==> 16'
        mode_setting()
        input_binary.config(text='8')
        output_binary.config(text='16')

    def eight_to_ten():
        global CONVERTER_MODE
        CONVERTER_MODE = '8 ==> 10'
        mode_setting()
        input_binary.config(text='8')
        output_binary.config(text='10')

    def eight_to_two():
        global CONVERTER_MODE
        CONVERTER_MODE = '8 ==> 2'
        mode_setting()
        input_binary.config(text='8')
        output_binary.config(text='2')

    def sixteen_to_ten():
        global CONVERTER_MODE
        CONVERTER_MODE = '16 ==> 10'
        mode_setting()
        input_binary.config(text='16')
        output_binary.config(text='10')

    def sixteen_to_eight():
        global CONVERTER_MODE
        CONVERTER_MODE = '16 ==> 8'
        mode_setting()
        input_binary.config(text='16')
        output_binary.config(text='8')

    def sixteen_to_two():
        global CONVERTER_MODE
        CONVERTER_MODE = '16 ==> 2'
        mode_setting()
        input_binary.config(text='16')
        output_binary.config(text='2')

    def switch_to_english():
        global SUCCESSFUL_OUTPUT_1, SUCCESSFUL_OUTPUT_2, SUCCESSFUL_OUTPUT_3, SUCCESSFUL_OUTPUT_END, FAILED_OUTPUT, \
            FAILED_TITLE
        main_window.title('Binary Converters')
        main_window.config(menu=menu_bar_english)
        explain_label.config(
            text='Please enter an integer below,\nand then click the button "Confirm"')
        confirm_button.config(text='Confirm')
        SUCCESSFUL_OUTPUT_1 = 'The '
        SUCCESSFUL_OUTPUT_2 = ' binary number of '
        SUCCESSFUL_OUTPUT_3 = ' is '
        SUCCESSFUL_OUTPUT_END = '\nThe Result has been copied'
        FAILED_OUTPUT = 'The number you typed in is wrong, \nplease re-enter'
        FAILED_TITLE = 'Error'
        change = {'language': 'english'}
        json_change = dumps(change)
        file_object = open('language_setting.json', 'w', encoding='utf-8')
        file_object.write(json_change)
        file_object.close()

    def switch_to_chinese():
        global SUCCESSFUL_OUTPUT_1, SUCCESSFUL_OUTPUT_2, SUCCESSFUL_OUTPUT_3, SUCCESSFUL_OUTPUT_END, FAILED_OUTPUT, \
            FAILED_TITLE
        main_window.title('进制转换器')
        main_window.config(menu=menu_bar_chinese)
        explain_label.config(text='请在下方输入需转换整数，并点击“确认”键')
        confirm_button.config(text='确认')
        SUCCESSFUL_OUTPUT_1 = ''
        SUCCESSFUL_OUTPUT_2 = '进制转换（被转换数：'
        SUCCESSFUL_OUTPUT_3 = '）的结果为'
        SUCCESSFUL_OUTPUT_END = '\n结果已被复制'
        FAILED_OUTPUT = '输入有误，请重新输入'
        FAILED_TITLE = '错误'
        change = {'language': 'chinese'}
        json_change = dumps(change)
        file_object = open('language_setting.json', 'w', encoding='utf-8')
        file_object.write(json_change)
        file_object.close()

    def switch_to_german():
        global SUCCESSFUL_OUTPUT_1, SUCCESSFUL_OUTPUT_2, SUCCESSFUL_OUTPUT_3, SUCCESSFUL_OUTPUT_END, FAILED_OUTPUT, \
            FAILED_TITLE
        main_window.title('Binary Converter')
        main_window.config(menu=menu_bar_german)
        explain_label.config(text='Bitte geben Sie unten einen Integer ein,\n'
                                  'bitte wieder eingeben \nund auf den Button "Bestätigen" klicken')
        confirm_button.config(text='Bestätigen')
        SUCCESSFUL_OUTPUT_1 = 'Die '
        SUCCESSFUL_OUTPUT_2 = ' binäre Anzahl von '
        SUCCESSFUL_OUTPUT_3 = ' ist '
        SUCCESSFUL_OUTPUT_END = '\nDas Ergebnis wurde kopiert'
        FAILED_OUTPUT = 'Die Nummer, die Sie eingegeben haben, ist falsch,\n' \
                        'bitte wieder eingeben'
        FAILED_TITLE = 'Fehler'
        change = {'language': 'german'}
        json_change = dumps(change)
        file_object = open('language_setting.json', 'w', encoding='utf-8')
        file_object.write(json_change)
        file_object.close()

    # Create an english menu bar for function and language selection
    function_menu = Menu(master=menu_bar_english, tearoff=0)
    menu_bar_english.add_cascade(label='Function setting', menu=function_menu)
    function_menu.add_command(label='From 10 to 16', command=ten_to_sixteen)
    function_menu.add_command(label='From 10 to 8', command=ten_to_eight)
    function_menu.add_command(label='From 10 to 2', command=ten_to_two)
    function_menu.add_command(label='From 2 to 16', command=two_to_sixteen)
    function_menu.add_command(label='From 2 to 8', command=two_to_eight)
    function_menu.add_command(label='From 2 to 10', command=two_to_ten)
    function_menu.add_command(label='From 8 to 16', command=eight_to_sixteen)
    function_menu.add_command(label='From 8 to 10', command=eight_to_ten)
    function_menu.add_command(label='From 8 to 2', command=eight_to_two)
    function_menu.add_command(label='From 16 to 10', command=sixteen_to_ten)
    function_menu.add_command(label='From 16 to 8', command=sixteen_to_eight)
    function_menu.add_command(label='From 16 to 2', command=sixteen_to_two)
    language_menu = Menu(master=menu_bar_english, tearoff=0)
    menu_bar_english.add_cascade(label='Language/语言', menu=language_menu)
    language_menu.add_command(label='English', command=switch_to_english)
    language_menu.add_command(label='Deutsch', command=switch_to_german)
    language_menu.add_command(label='中文（简体）', command=switch_to_chinese)

    # Create an chinese menu bar for function and language selection
    function_menu = Menu(master=menu_bar_chinese, tearoff=0)
    menu_bar_chinese.add_cascade(label='功能设置', menu=function_menu)
    function_menu.add_command(label='10进制转16进制', command=ten_to_sixteen)
    function_menu.add_command(label='10进制转8进制', command=ten_to_eight)
    function_menu.add_command(label='10进制转2进制', command=ten_to_two)
    function_menu.add_command(label='2进制转16进制', command=two_to_sixteen)
    function_menu.add_command(label='2进制转8进制', command=two_to_eight)
    function_menu.add_command(label='2进制转10进制', command=two_to_ten)
    function_menu.add_command(label='8进制转16进制', command=eight_to_sixteen)
    function_menu.add_command(label='8进制转10进制', command=eight_to_ten)
    function_menu.add_command(label='8进制转2进制', command=eight_to_two)
    function_menu.add_command(label='16进制转10进制', command=sixteen_to_ten)
    function_menu.add_command(label='16进制转8进制', command=sixteen_to_eight)
    function_menu.add_command(label='16进制转2进制', command=sixteen_to_two)
    language_menu = Menu(master=menu_bar_chinese, tearoff=0)
    menu_bar_chinese.add_cascade(label='Language/语言', menu=language_menu)
    language_menu.add_command(label='English', command=switch_to_english)
    language_menu.add_command(label='Deutsch', command=switch_to_german)
    language_menu.add_command(label='中文（简体）', command=switch_to_chinese)

    # Create an german menu bar for function and language selection
    function_menu = Menu(master=menu_bar_german, tearoff=0)
    menu_bar_german.add_cascade(
        label='Funktions Einstellung', menu=function_menu)
    function_menu.add_command(label='Von 10 bis 16', command=ten_to_sixteen)
    function_menu.add_command(label='Von 10 bis 8', command=ten_to_eight)
    function_menu.add_command(label='Von 10 bis 2', command=ten_to_two)
    function_menu.add_command(label='Von 2 bis 16', command=two_to_sixteen)
    function_menu.add_command(label='Von 2 bis 8', command=two_to_eight)
    function_menu.add_command(label='Von 2 bis 10', command=two_to_ten)
    function_menu.add_command(label='Von 8 bis 16', command=eight_to_sixteen)
    function_menu.add_command(label='Von 8 bis 10', command=eight_to_ten)
    function_menu.add_command(label='Von 8 bis 2', command=eight_to_two)
    function_menu.add_command(label='Von 16 bis 10', command=sixteen_to_ten)
    function_menu.add_command(label='Von 16 bis 8', command=sixteen_to_eight)
    function_menu.add_command(label='Von 16 bis 2', command=sixteen_to_two)
    language_menu = Menu(master=menu_bar_german, tearoff=0)
    menu_bar_german.add_cascade(label='Language/语言', menu=language_menu)
    language_menu.add_command(label='English', command=switch_to_english)
    language_menu.add_command(label='Deutsch', command=switch_to_german)
    language_menu.add_command(label='中文（简体）', command=switch_to_chinese)

    # Create a label to show how to use it
    explain_label = Label(main_window,
                          text='Please enter an integer below,\nand then click the button "Confirm"',
                          font=('Arial', 12))
    explain_label.place(x=210, y=27, anchor='center')

    # Create two label controls to show the calculation mode
    if (CONVERTER_MODE == '10 ==> 16') or (CONVERTER_MODE == '10 ==> 8') or (CONVERTER_MODE == '10 ==> 2'):
        input_binary = Label(main_window, text='10')
        input_binary.place(x=25, y=70, anchor='center')
    elif (CONVERTER_MODE == '16 ==> 10') or (CONVERTER_MODE == '16 ==> 8') or (CONVERTER_MODE == '16 ==> 2'):
        input_binary = Label(main_window, text='16')
        input_binary.place(x=25, y=70, anchor='center')
    elif (CONVERTER_MODE == '8 ==> 10') or (CONVERTER_MODE == '8 ==> 16') or (CONVERTER_MODE == '8 ==> 2'):
        input_binary = Label(main_window, text='8')
        input_binary.place(x=25, y=70, anchor='center')
    else:
        input_binary = Label(main_window, text='2')
        input_binary.place(x=25, y=70, anchor='center')
    arrow_string = StringVar()
    Label(main_window, textvariable=arrow_string).place(
        x=62.5, y=70, anchor='center')
    ARROW_THREAD.start()
    if (CONVERTER_MODE == '10 ==> 16') or (CONVERTER_MODE == '8 ==> 16') or (CONVERTER_MODE == '2 ==> 16'):
        output_binary = Label(main_window, text='16')
        output_binary.place(x=100, y=70, anchor='center')
    elif (CONVERTER_MODE == '16 ==> 10') or (CONVERTER_MODE == '8 ==> 10') or (CONVERTER_MODE == '2 ==> 10'):
        output_binary = Label(main_window, text='10')
        output_binary.place(x=100, y=70, anchor='center')
    elif (CONVERTER_MODE == '16 ==> 8') or (CONVERTER_MODE == '10 ==> 8') or (CONVERTER_MODE == '2 ==> 8'):
        output_binary = Label(main_window, text='8')
        output_binary.place(x=100, y=70, anchor='center')
    else:
        output_binary = Label(main_window, text='2')
        output_binary.place(x=100, y=70, anchor='center')

    # Create an entry and place it
    entry = Entry(main_window, width=23, show=None)
    entry.place(x=210, y=70, anchor='center')

    def is_hex(input_string):
        sixteen_binary_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'A', 'B',
                               'C', 'D', 'E', 'F']
        check_list = list(input_string)
        if len(check_list) == 0:
            return None
        elif (list(input_string)[0] == '0' and list(input_string)[1] == 'x') or (
                list(input_string)[0] == '0' and list(input_string)[1] == 'X'):
            del check_list[0]
            del check_list[0]
        for n in check_list:
            if sixteen_binary_list.count(n) == 0:
                return False
        return True

    def is_oct(input_string):
        sixteen_binary_list = ['0', '1', '2', '3', '4', '5', '6', '7']
        check_list = list(input_string)
        if len(check_list) == 0:
            return None
        elif (list(input_string)[0] == '0' and list(input_string)[1] == 'o') or (
                list(input_string)[0] == '0' and list(input_string)[1] == 'O'):
            del check_list[0]
            del check_list[0]
        for n in check_list:
            if sixteen_binary_list.count(n) == 0:
                return False
        return True

    def is_bin(input_string):
        sixteen_binary_list = ['0', '1']
        check_list = list(input_string)
        if len(check_list) == 0:
            return None
        elif (list(input_string)[0] == '0' and list(input_string)[1] == 'b') or (
                list(input_string)[0] == '0' and list(input_string)[1] == 'B'):
            del check_list[0]
            del check_list[0]
        for n in check_list:
            if sixteen_binary_list.count(n) == 0:
                return False
        return True

    # Define the function of the button

    def get_number():
        # Get the strings that user typed in
        global INPUT_STRING
        INPUT_STRING = entry.get()
        if CONVERTER_MODE == '10 ==> 16' or CONVERTER_MODE == '10 ==> 8' or CONVERTER_MODE == '10 ==> 2':
            # Check if it's an integer and then set the result
            if INPUT_STRING.isdigit():
                if CONVERTER_MODE == '10 ==> 16':
                    output_string.set(
                        SUCCESSFUL_OUTPUT_1 + '16' + SUCCESSFUL_OUTPUT_2 + INPUT_STRING + SUCCESSFUL_OUTPUT_3 + hex(
                            int(INPUT_STRING)) + SUCCESSFUL_OUTPUT_END)
                    history_listbox.insert(
                        0, [INPUT_STRING, hex(int(INPUT_STRING))])
                    copy_main_window.clipboard_clear()
                    main_window.clipboard_append(hex(int(INPUT_STRING)))
                elif CONVERTER_MODE == '10 ==> 8':
                    output_string.set(
                        SUCCESSFUL_OUTPUT_1 + '8' + SUCCESSFUL_OUTPUT_2 + INPUT_STRING + SUCCESSFUL_OUTPUT_3 + oct(
                            int(INPUT_STRING)) + SUCCESSFUL_OUTPUT_END)
                    history_listbox.insert(
                        0, [INPUT_STRING, oct(int(INPUT_STRING))])
                    main_window.clipboard_append(oct(int(INPUT_STRING)))
                else:
                    output_string.set(
                        SUCCESSFUL_OUTPUT_1 + '2' + SUCCESSFUL_OUTPUT_2 + INPUT_STRING + SUCCESSFUL_OUTPUT_3 + bin(
                            int(INPUT_STRING)) + SUCCESSFUL_OUTPUT_END)
                    history_listbox.insert(
                        0, [INPUT_STRING, bin(int(INPUT_STRING))])
                    main_window.clipboard_append(bin(int(INPUT_STRING)))
            elif INPUT_STRING == '':
                output_string.set('')
            else:
                messagebox.showerror(
                    title=FAILED_TITLE, message=FAILED_OUTPUT)
        elif CONVERTER_MODE == '2 ==> 16' or CONVERTER_MODE == '2 ==> 8' or CONVERTER_MODE == '2 ==> 10':
            if is_bin(INPUT_STRING):
                if CONVERTER_MODE == '2 ==> 16':
                    output_string.set(
                        SUCCESSFUL_OUTPUT_1 + '16' + SUCCESSFUL_OUTPUT_2 + INPUT_STRING + SUCCESSFUL_OUTPUT_3 + hex(
                            int(INPUT_STRING, 2)) + SUCCESSFUL_OUTPUT_END)
                    history_listbox.insert(
                        0, [INPUT_STRING, hex(int(INPUT_STRING, 2))])
                    copy_main_window.clipboard_clear()
                    main_window.clipboard_append(hex(int(INPUT_STRING, 2)))
                elif CONVERTER_MODE == '2 ==> 8':
                    output_string.set(
                        SUCCESSFUL_OUTPUT_1 + '8' + SUCCESSFUL_OUTPUT_2 + INPUT_STRING + SUCCESSFUL_OUTPUT_3 + oct(
                            int(INPUT_STRING, 2)) + SUCCESSFUL_OUTPUT_END)
                    history_listbox.insert(
                        0, [INPUT_STRING, oct(int(INPUT_STRING, 2))])
                    main_window.clipboard_append(oct(int(INPUT_STRING, 2)))
                else:
                    output_string.set(
                        SUCCESSFUL_OUTPUT_1 + '10' + SUCCESSFUL_OUTPUT_2 + INPUT_STRING + SUCCESSFUL_OUTPUT_3 + str(
                            int(INPUT_STRING, 2)) + SUCCESSFUL_OUTPUT_END)
                    history_listbox.insert(
                        0, [INPUT_STRING, int(INPUT_STRING, 2)])
                    main_window.clipboard_append(str(int(INPUT_STRING, 2)))
            elif is_bin(INPUT_STRING) is False:
                messagebox.showerror(
                    title=FAILED_TITLE, message=FAILED_OUTPUT)
            elif INPUT_STRING == '':
                output_string.set('')
        elif CONVERTER_MODE == '8 ==> 16' or CONVERTER_MODE == '8 ==> 2' or CONVERTER_MODE == '8 ==> 10':
            if is_oct(INPUT_STRING):
                if CONVERTER_MODE == '8 ==> 16':
                    output_string.set(
                        SUCCESSFUL_OUTPUT_1 + '16' + SUCCESSFUL_OUTPUT_2 + INPUT_STRING + SUCCESSFUL_OUTPUT_3 + hex(
                            int(INPUT_STRING, 8)) + SUCCESSFUL_OUTPUT_END)
                    history_listbox.insert(
                        0, [INPUT_STRING, hex(int(INPUT_STRING, 8))])
                    copy_main_window.clipboard_clear()
                    main_window.clipboard_append(hex(int(INPUT_STRING, 8)))
                elif CONVERTER_MODE == '8 ==> 2':
                    output_string.set(
                        SUCCESSFUL_OUTPUT_1 + '2' + SUCCESSFUL_OUTPUT_2 + INPUT_STRING + SUCCESSFUL_OUTPUT_3 + bin(
                            int(INPUT_STRING, 8)) + SUCCESSFUL_OUTPUT_END)
                    history_listbox.insert(
                        0, [INPUT_STRING, bin(int(INPUT_STRING, 8))])
                    main_window.clipboard_append(bin(int(INPUT_STRING, 8)))
                else:
                    output_string.set(
                        SUCCESSFUL_OUTPUT_1 + '10' + SUCCESSFUL_OUTPUT_2 + INPUT_STRING + SUCCESSFUL_OUTPUT_3 + str(
                            int(INPUT_STRING, 8)) + SUCCESSFUL_OUTPUT_END)
                    history_listbox.insert(
                        0, [INPUT_STRING, int(INPUT_STRING, 8)])
                    main_window.clipboard_append(str(int(INPUT_STRING, 8)))
            elif is_oct(INPUT_STRING) is False:
                messagebox.showerror(
                    title=FAILED_TITLE, message=FAILED_OUTPUT)
            elif INPUT_STRING == '':
                output_string.set('')
        else:
            if is_hex(INPUT_STRING):
                if CONVERTER_MODE == '16 ==> 2':
                    output_string.set(
                        SUCCESSFUL_OUTPUT_1 + '2' + SUCCESSFUL_OUTPUT_2 + INPUT_STRING + SUCCESSFUL_OUTPUT_3 + bin(
                            int(INPUT_STRING, 16)) + SUCCESSFUL_OUTPUT_END)
                    history_listbox.insert(
                        0, [INPUT_STRING, bin(int(INPUT_STRING, 16))])
                    copy_main_window.clipboard_clear()
                    main_window.clipboard_append(bin(int(INPUT_STRING, 16)))
                elif CONVERTER_MODE == '16 ==> 8':
                    output_string.set(
                        SUCCESSFUL_OUTPUT_1 + '8' + SUCCESSFUL_OUTPUT_2 + INPUT_STRING + SUCCESSFUL_OUTPUT_3 + oct(
                            int(INPUT_STRING, 16)) + SUCCESSFUL_OUTPUT_END)
                    history_listbox.insert(
                        0, [INPUT_STRING, oct(int(INPUT_STRING, 16))])
                    main_window.clipboard_append(oct(int(INPUT_STRING, 16)))
                else:
                    output_string.set(
                        SUCCESSFUL_OUTPUT_1 + '10' + SUCCESSFUL_OUTPUT_2 + INPUT_STRING + SUCCESSFUL_OUTPUT_3 + str(
                            int(INPUT_STRING, 16)) + SUCCESSFUL_OUTPUT_END)
                    history_listbox.insert(
                        0, [INPUT_STRING, int(INPUT_STRING, 16)])
                    main_window.clipboard_append(str(int(INPUT_STRING, 16)))
            elif is_hex(INPUT_STRING) is False:
                messagebox.showerror(
                    title=FAILED_TITLE, message=FAILED_OUTPUT)
            elif INPUT_STRING == '':
                output_string.set('')

        # Delete the results that listbox can't show
        history_listbox.delete(20)
        entry.delete(0, 'end')

    def number_enter(n):
        get_number()

    # Create a button and bind the function to it
    confirm_button = Button(
        main_window, text='Confirm', command=get_number)
    confirm_button.place(x=360, y=70, anchor='center')
    entry.bind('<Return>', number_enter)

    # Create a label to show the result
    output_string = StringVar()
    result_label = Label(
        main_window, textvariable=output_string, font=('Arial', 12))
    result_label.place(x=210, y=110, anchor='center')

    # Create a listbox to show the results of the most recent calculations
    history_listbox = Listbox(main_window, width=50, height=20)
    history_listbox.place(x=210, y=350, anchor='center')

    language_file = open('language_setting.json', encoding='utf-8')
    setting_2 = load(language_file)
    language = setting_2['language']
    if language == 'english':
        switch_to_english()
    elif language == 'chinese':
        switch_to_chinese()
    else:
        switch_to_german()
    language_file.close()

    main_window.protocol('WM_DELETE_WINDOW', close_window)

    # The loop of the main_window
    main_window.mainloop()
