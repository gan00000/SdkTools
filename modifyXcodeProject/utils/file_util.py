#coding=utf-8
import imp
import sys
imp.reload(sys)
sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的

import os
import re

def read_file_data_utf8(file_path):
    print 'read_file_data=' + file_path
    if os.path.exists(file_path):
        f_obj = open(file_path, mode="rb")  # 首先先创建一个文件对象
        f_data = f_obj.read().decode("UTF-8")  # 用read()方法读取文件内容  contents = f.read().decode("UTF-8")
        f_obj.close()
        return f_data
    return None

def read_file_data(file_path):
    # print 'read_file_data=' + file_path
    if os.path.exists(file_path):
        f_obj = open(file_path, mode="rb")  # 首先先创建一个文件对象
        f_data = f_obj.read()#.decode("UTF-8")  # 用read()方法读取文件内容  contents = f.read().decode("UTF-8")
        f_obj.close()
        return f_data
    return None

def read_file_data_for_line(file_path):
    if os.path.exists(file_path):
        f_obj = open(file_path, mode="rb")  # 首先先创建一个文件对象
        # f_data = f_obj.read()  # 用read()方法读取文件内容
        text_lines = f_obj.readlines()
        f_obj.close()
        return text_lines


def wite_data_to_file(file_path, data):
    f_obj = open(file_path, mode='wb')  # 首先先创建一个文件对象   f.write(contents.encode("UTF-8"))
    f_obj.write(data.encode("UTF-8"))
    f_obj.flush()
    f_obj.close()

def wite_data_to_file_noencode(file_path, data):
    f_obj = open(file_path, mode='wb')  # 首先先创建一个文件对象   f.write(contents.encode("UTF-8"))
    f_obj.write(data)
    f_obj.flush()
    f_obj.close()
