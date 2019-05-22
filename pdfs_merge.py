#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'A simple python script to merge pdf files'

__author__ = 'Yuanyang Shao'

from PyPDF2 import PdfFileMerger
from os import listdir
from re import IGNORECASE, search

def merge(path):
    # find all pdfs
    pattern =r"\.pdf$"
    file_names_1st = [path + "\\" + f for f in listdir(path) if search(pattern, f, IGNORECASE) and not search(r'整合版文档.pdf', f)]

    # merge the file
    opened_file = [open(file_name, 'rb') for file_name in file_names_1st]
    pdfFM = PdfFileMerger()
    for file in opened_file:
        pdfFM.append(file)

    # output the file
    with open(path + "\\整合版文档.pdf", 'wb') as write_out_file:
        pdfFM.write(write_out_file)

    # close all the input files
    for file in opened_file:
        file.close()
