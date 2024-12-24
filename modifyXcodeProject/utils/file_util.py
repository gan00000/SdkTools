#coding=utf-8
import imp
import shutil
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



def copy_all_to_destination(source_dir, destination_dir):
    # 创建目标目录（如果不存在）
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # 遍历源目录中的所有文件和目录
    for item in os.listdir(source_dir):

        if item == '.git' or item == '.gitignore' or item == '.DS_Store':
            continue

        source_path = os.path.join(source_dir, item)  # 源路径
        destination_path = os.path.join(destination_dir, item)  # 目标路径

        try:
            if os.path.isdir(source_path):
                # 复制目录
                shutil.copytree(source_path, destination_path, symlinks=True)
                # print(f'Copied directory: {source_path} to {destination_path}')
            else:
                # 复制文件
                shutil.copy2(source_path, destination_path)
                # print(f'Copied file: {source_path} to {destination_path}')
        except Exception as e:
            print e

def delete_contents(directory):
    # 检查目录是否存在
    if os.path.exists(directory) and os.path.isdir(directory):
        # 遍历目录中的所有内容并删除
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # 删除子目录及其内容
                    # print('Deleted directory')
                else:
                    os.remove(item_path)  # 删除文件
                    # print('Deleted file')
            except Exception as e:
                print( 'Error deleting ')
    else:
        print 'Directory does not exist'
