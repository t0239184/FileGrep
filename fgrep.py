#!/bin/python
# -*- coding: utf-8 -*-
import codecs
import os
import sys
import time

class Color:
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'

    HEADER = '\033[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    ENDC = '\033[0m'


'''
   根据text文件数据类型判断是否是二进制文件UTF-8
   :param ff: 文件名（含路径）
   :return: True或False，返回是否是二进制文件
'''

#: BOMs to indicate that a file is a text file even if it contains zero bytes.
_TEXT_BOMS = (
    codecs.BOM_UTF16_BE,
    codecs.BOM_UTF16_LE,
    codecs.BOM_UTF32_BE,
    codecs.BOM_UTF32_LE,
    codecs.BOM_UTF8,
)


def is_binary_file(file_path):
    with open(file_path, 'rb') as file:
        initial_bytes = file.read(8192)
        file.close()
        for bom in _TEXT_BOMS:
            if initial_bytes.startswith(bom):
                continue
            else:
                if b'\0' in initial_bytes:
                    return True



# 遍歷filepath下所有檔案，包括子目錄
def search(filepath, pattern):
    list = []
    files = os.listdir(filepath)
    for file_name in files:
        file_path = os.path.join(filepath, file_name)
        if os.path.isdir(file_path):
            search(file_path, pattern)
        else:
            # file_total_count += 1
            if is_binary_file(file_path):
                continue
            file_process(file_path, list, pattern)


def file_process(file_path, list, pattern):
    with codecs.open(file_path, 'r', encoding='UTF-8', errors='ignore') as file:
        i = 1
        is_first = True
        for line in file:
            if pattern in line:
                if is_first:
                    # print(f"{color.Color.OK_BLUE}File: {file_path}{color.Color.ENDC}")
                    list.append(f"{Color.OK_BLUE}File: {file_path}{Color.ENDC}")
                    is_first = False
                # print(f"{i}:{line.strip('%n')}")
                new_str = line.replace(pattern, Color.OK_CYAN + pattern + Color.ENDC)
                list.append(str(i) + ": " + new_str.strip("\n"))
            i = i + 1

        for record in list:
            print(record)


def main():
    start_time = time.time()
    print('Number of arguments:', len(sys.argv), 'arguments.')
    pattern = "TODO"
    path = '../../'
    search(path, pattern)
    print('cost time:', '%.2f' % (time.time() - start_time), 'ms')

main()
