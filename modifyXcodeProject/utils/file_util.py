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
                # shutil.copytree(source_path, destination_path, symlinks=True)
                # 处理目录递归复制
                if os.path.exists(destination_path):
                    # 目标子目录已存在，递归调用自身处理
                    copy_all_to_destination(source_path, destination_path)
                else:
                    # 目标子目录不存在，直接复制
                    shutil.copytree(source_path, destination_path, symlinks=True)
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


def copy_file(source_path, target_path, overwrite=True):
    """
    复制单个文件，支持覆盖已存在的目标文件
    :param source_path: 源文件路径
    :param target_path: 目标文件路径
    :param overwrite: 是否覆盖已存在的文件
    :param verbose: 是否显示详细信息
    :return: 复制成功返回True，失败返回False
    """
    try:
        # 检查源文件是否存在
        if not os.path.isfile(source_path):
            print("不存在或不是文件:" + source_path)
            return False

        # 确保目标目录存在
        target_dir = os.path.dirname(target_path)
        os.makedirs(target_dir, exist_ok=True)

        # 检查目标文件是否存在
        if os.path.exists(target_path):
            if overwrite:
                print("覆盖已存在的文件: " + target_path)
            else:
                print("跳过已存在的文件: " + overwrite)
                return True

        # 复制文件
        shutil.copy2(source_path, target_path)  # copy2保留更多元数据
        # print("已复制: {source_path} -> {target_path}")
        print("已复制: %s -> %s" % source_path, target_path)
        return True

    except Exception as e:
        print("复制文件时出错" + e)
        return False