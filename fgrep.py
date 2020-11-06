#!/bin/python
# -*- coding: utf-8 -*-
import codecs
import os
import sys
import time


class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    ENDC = '\033[0m'


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
        for bom in _TEXT_BOMS:
            if initial_bytes.startswith(bom):
                continue
            else:
                if b'\0' in initial_bytes:
                    return True


file_total_count = 0
found_count = 0
total_line = 0
match_line = 0
deep_level_index = 1

ignore_list = ['.jpg', '.jpeg', '.png', '.bmp', '.svg', '.git']


def search(search_path, pattern, level):
    global file_total_count, deep_level_index
    list = []
    files = os.listdir(search_path)
    for file_name in files:
        name, suffix = os.path.splitext(file_name)
        if suffix in ignore_list or name in ignore_list: continue
        file_path = os.path.join(search_path, file_name)
        if os.path.isdir(file_path):
            if deep_level_index >= int(level):
                break
            deep_level_index = cal_deep_level(file_path)
            search(file_path, pattern, level)
        else:
            file_total_count += 1
            if is_binary_file(file_path):
                continue
            file_process(file_path, list, pattern)


def cal_deep_level(file_path):
    return (file_path.count('/')) + 1 - init_path_deep_level


is_first = True


def file_process(file_path, list, pattern):

    global is_first, found_count, total_line, match_line, output_file_path
    with codecs.open(file_path, 'rb', encoding='UTF-8', errors='ignore') as file:
        i = 1
        is_first = True
        for line in file:
            total_line += 1
            list.clear()
            if pattern in line:
                match_line += 1
                if is_first:
                    found_count += 1
                    add_file_path_to_list(file_path, list)
                add_line_content_to_list(i, line, list, pattern)
            i = i + 1
            if (not output_file_path == ''):
                print_found()

            for record in list:
                if ('' == output_file_path):
                    print(record)
                else:
                    f = open(output_file_path, "a")
                    f.write(record + '\n')


def add_line_content_to_list(i, line, list, pattern):
    line_length = len(line.split())
    if line_length > 180:
        list.append(str(i) + ': ...more...\n')
    else:
        new_str = line.replace(pattern, Color.PURPLE + pattern + Color.ENDC)
        list.append(str(i) + ": " + new_str.strip("\n"))


def add_file_path_to_list(file_path, list):
    global is_first
    list.append(f"{Color.BLUE}File: {file_path}{Color.ENDC}")
    is_first = False


def print_help():
    print("args:")
    print("  help      print help information.")
    print("  pattern   the grep word.")
    print("  path      the search path.")
    print("  deep      the fold deep level.")
    print("  output    the output file name.")
    print("")
    print("example:")
    print("  python fgrep pattern=TODO ")
    print("  python fgrep path=./ pattern=TODO ")
    print("  python fgrep path=./ deep=10 pattern=TODO ")


def print_found():
    print('Line:', str(match_line) + '/' + str(total_line),
          'File:', str(found_count) + '/' + str(file_total_count),
          '\r', end=' ')


def print_cost(start_time):
    print('Cost:', '%.2f' % (time.time() - start_time), 'ms')


init_path = './'
init_path_deep_level = 0
output_file_path = ''

start_time = time.time()
deep = 99

args_length = len(sys.argv)
if args_length < 2:
    print_help()
else:
    pattern = ''
    do_search = False
    for arg in sys.argv:
        str_array = arg.split('=')
        if len(str_array) < 2:
            if 'help' == arg:
                print_help()
                break

            key = str_array[0]
            value = str_array[1]
            if 'path' == key:
                if value == '.':
                    init_path = './'
                else:
                    init_path = value
            if 'deep' == key:
                deep = value
            if 'output' == key:
                output_file_path = value
            if 'pattern' == key:
                pattern = value
                do_search = True


    if do_search:
        print(f'{Color.YELLOW}Do Search in :{Color.ENDC}',
              f'{Color.UNDERLINE}{init_path}{Color.ENDC}',
              f'{Color.YELLOW}pattern:{Color.ENDC}',
              f'{Color.UNDERLINE}{pattern}{Color.ENDC}',
              '\n')
        init_path_deep_level = init_path.count('/') - 1
        search(init_path, pattern, deep)
        print_found()
        print_cost(start_time)
    else:
        print(f'{Color.YELLOW}pattern is required!!{Color.ENDC}')
        print()
        print('    python fgrep pattern=TODO')
        print()
