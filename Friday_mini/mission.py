#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'Class and functions for data and data display'

__author__ = 'QidiLiu'

from time import time
from time import localtime, strftime
from tkinter import Frame, Label, LEFT, RIGHT

import tkinter

class Mission(object):

    def __init__(self, content, master):
        self.content = content
        self.master = master
        self.birth = time()
        self.life = None
        self.MID = strftime('%Y%m%d%H%M%S', localtime())

    def display(self, parent):
        locals()[self.MID] = Frame(parent)
        locals()[self.MID].pack(fill='x')
        Label(locals()[self.MID], text=self.content).pack(side=LEFT)
