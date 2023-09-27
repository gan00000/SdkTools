#coding=utf-8
import imp
import sys
import uuid

from modifyXcodeProject import oc_class_parser, oc_method_util, cpp_code_util, oc_code_util
from modifyXcodeProject.utils import file_util, word_util, datetime_util
from modifyXcodeProject.utils.PrpCrypt import PrpCrypt

imp.reload(sys)
sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的

import os
import re

import chardet

# 导入 random(随机数) 模块
import random

genest_word = []
words_dong = []
words_name = []

# xcode_project_path = ''

# /Users/gan/Desktop/黑特篮球new2/SkyBetufi/SourceCode/SkySrc/CommonModule/GUtility/PKCategory
# oc_all_path = ''
# oc_modify_path = ''

handle_file_count = 0
file_count = 0

oc_exclude_files = []
oc_exclude_dirs = []

words_dong_s = []
def random_word_dong():
    temp_int = random.randint(0, len(words_dong) - 1)
    temp = words_dong[temp_int]
    while temp in words_dong_s:
        temp_int = random.randint(0, len(words_dong) - 1)
        temp = words_dong[temp_int]
    words_dong_s.append(temp)
    return temp


words_name_s = []
def random_word_name():
    temp_int = random.randint(0, len(words_name) - 1)
    temp = words_name[temp_int]
    while temp in words_name_s:
        temp_int = random.randint(0, len(words_name) - 1)
        temp = words_name[temp_int]
    words_name_s.append(temp)
    return temp

def random_2word():#随机生成两个单词

    first_index = random.randint(0, len(genest_word) - 1)
    sec_index = random.randint(0, len(genest_word) - 1)
    while (first_index == sec_index):
        sec_index = random.randint(0, len(genest_word) - 1)

    first_word = genest_word[first_index]
    sec_word = genest_word[sec_index]

    return first_word, sec_word

def random_1word():

    first_index = random.randint(0, len(genest_word) - 1)
    first_word = genest_word[first_index]

    return first_word

def words_reader(word_file_path):

    words = []
    f_obj = open(word_file_path, "r")
    text_lines = f_obj.readlines()
    for line in text_lines:
        line = line.decode('utf-8')
        word = line.strip().replace(' ', '')
        if len(word) > 2:  # 太短的单词去掉
            words.append(word)
    return words

word_oc_class_temp = []
def random_word_for_oc_class():

    first_word, sec_word = random_2word()
    new_word = first_word.capitalize() + sec_word.capitalize()

    while (new_word in word_oc_class_temp):
        first_word, sec_word = random_2word()
        new_word = first_word.capitalize() + sec_word.capitalize()

    word_oc_class_temp.append(new_word)
    return new_word

word_image_name_temp = []
def random_word_for_image():

    first_word, sec_word = random_2word()
    new_word = first_word.lower() + sec_word.lower()

    while (new_word in word_image_name_temp):
        first_word, sec_word = random_2word()
        new_word = first_word.lower() + "_" + sec_word.lower()

    word_image_name_temp.append(new_word)
    return new_word


word_oc_method_temp = []
def random_word_for_no_use_method():

    first_word, sec_word = random_2word()
    new_word = first_word.lower() + sec_word.capitalize()

    while (new_word in word_oc_method_temp):
        first_word, sec_word = random_2word()
        new_word = first_word.capitalize() + sec_word.capitalize()

    word_oc_method_temp.append(new_word)
    return new_word

def random_word_for_no_use_method_for_cpp():

    first_word, sec_word = random_2word()
    new_word = first_word.lower() + '_' + sec_word.lower() + '_' + random_1word().lower()

    while (new_word in word_oc_method_temp):
        first_word, sec_word = random_2word()
        new_word = first_word.lower() + '_' + sec_word.lower() + '_' + random_1word().lower()

    word_oc_method_temp.append(new_word)
    return new_word


def modify_oc_class_name(oc_path, xcode_project_path, oc_all_path, oc_exclude_dirs_ref_modify):
    global file_count, handle_file_count, fia

    project_content_path = os.path.join(xcode_project_path, 'project.pbxproj')
    project_content = read_file_data(project_content_path)

    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        old_map_new_content = ''
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store" or file_name.endswith(".swift") or 'main' in file_name:
                    continue

                file_count = file_count + 1

                exclude_dir_flag = 0
                for exclude_dir in oc_exclude_dirs:
                    if exclude_dir in root:
                        exclude_dir_flag = 1
                if exclude_dir_flag == 1:
                    continue


                if file_name.endswith('.m') or file_name.endswith('.mm'):#cpp文件

                    # if has_new_prefix_in_start(file_name):
                    #     continue
                    # if oc_new_prefix and file_name.startswith(oc_new_prefix): #已经存在前缀，不处理
                    #     continue

                    # if '+' in file_name:  # 分类
                    #     continue

                    file_name_no_extension = os.path.splitext(file_name)[0]

                    file_extension = os.path.splitext(file_name)[1]

                    header_file_name = file_name_no_extension + '.h'  #cpp对应的头文件名称
                    if header_file_name in oc_exclude_files: #特殊排除
                        continue

                    header_file_path = os.path.join(root, header_file_name)   #头文件路径
                    if os.path.exists(header_file_path):

                        print '正在处理文件：' + file_name
                        new_word = random_word_for_oc_class()
                        if file_name_no_extension.endswith('View') or file_name_no_extension.endswith('ViewV2'):
                            new_word = new_word + 'View'
                        elif file_name_no_extension.endswith('Mode'):
                            new_word = new_word + 'Mode'
                        elif file_name_no_extension.endswith('Data'):
                            new_word = new_word + 'Data'
                        elif file_name_no_extension.endswith('Controller'):
                            new_word = new_word + 'Controller'
                        elif file_name_no_extension.endswith('Button'):
                            new_word = new_word + 'Button'
                        elif file_name_no_extension.endswith('TextFiled'):
                            new_word = new_word + 'TextFiled'
                        elif file_name_no_extension.endswith('Cell'):
                            new_word = new_word + 'Cell'

                        if '+' in file_name:  # 分类
                            fia = file_name_no_extension.split('+')
                            file_new_name = fia[0] + "+" + new_word + file_extension
                            header_file_new_name = fia[0] + "+" + new_word + '.h'



                        else:
                            file_new_name = new_word + file_extension
                            header_file_new_name = new_word + '.h'

                        file_old_path = os.path.join(root, file_name)
                        file_new_path = os.path.join(root, file_new_name)

                        try:
                            os.rename(file_old_path, file_new_path)  #更改文件名
                        except:
                            print '文件无法更改名称：' + file_old_path
                            continue


                        try:

                            header_file_new_path = os.path.join(root, header_file_new_name)

                            os.rename(header_file_path, header_file_new_path)  # 更改头文件名

                        except:
                            print '文件无法更改名称：' + header_file_path
                            continue

                        if '+' in file_name:  # 分类
                            file_new_name_no_extension = fia[0] + "+" + new_word
                        else:
                            file_new_name_no_extension = new_word


                        modify_oc_class_reference(oc_all_path, file_name_no_extension, file_new_name_no_extension, oc_exclude_dirs_ref_modify)

                        # 更改xproject文件中的.m
                        project_content = replace_xproject_data_reference(project_content, file_name, file_new_name)

                        # 更改xproject文件中的.h
                        project_content = replace_xproject_data_reference(project_content, header_file_name, header_file_new_name)

                        handle_file_count = handle_file_count + 1
                        print '处理完成' + file_name
                        old_map_new_content = old_map_new_content + file_name_no_extension + ' -------> ' + file_new_name_no_extension + '\n'

        wite_data_to_file(project_content_path, project_content)
        print '修改完成 file_count:' + str(file_count) + "  handle_file_count:" + str(handle_file_count)
        class_change_log_path = os.path.splitext(xcode_project_path)[0] + 'class_change_%s.log' % datetime_util.get_current_time_2() #写更改类的日志
        old_map_new_content = '===class change start===\n' + old_map_new_content
        file_util.wite_data_to_file(class_change_log_path, old_map_new_content)


#oc_path 所有源文件，置于一个单独目录最好
def modify_oc_class_reference(oc_path, old_ref, new_ref, oc_exclude_dirs_ref_modify):
    file_count = 0
    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                file_count = file_count + 1

                exclude_dir_flag = 0
                for exclude_dir in oc_exclude_dirs_ref_modify:
                    if exclude_dir in root:
                        exclude_dir_flag = 1
                if exclude_dir_flag == 1:
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm') \
                        or file_name.endswith('.h') or file_name.endswith('.pch') or \
                    file_name.endswith('.storyboard') or file_name.endswith('.xib'):    #oc文件

                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)

                    # if have_the_word_in_data(file_data, old_ref):

                    file_new_data = replace_data_by_word(file_data, old_ref, new_ref)
                    if (file_name.endswith('.m') or file_name.endswith('.mm') or file_name.endswith('.h')) and new_ref in file_name and '+' in old_ref and '+' in new_ref: #分类
                        old_ref_categery = old_ref.split('+')[1]
                        new_ref_categery = new_ref.split('+')[1]
                        file_new_data = file_new_data.replace('(' + old_ref_categery + ')', '(' + new_ref_categery + ')')
                    wite_data_to_file(file_path, file_new_data)

def modify_storyboard_reference(oc_path, old_ref, new_ref):

    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm'):    #oc文件

                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)

                    # if have_the_word_in_data(file_data, old_ref):
                    file_new_data = file_data.replace(old_ref, new_ref)

                    # file_new_data = replace_data_by_word(file_data, old_ref, new_ref)
                    wite_data_to_file(file_path, file_new_data)

def modify_image_name_reference(oc_path, old_ref, new_ref):

    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm') \
                        or file_name.endswith('.h') or file_name.endswith('.pch') or \
                    file_name.endswith('.storyboard') or file_name.endswith('.xib'):    #oc文件

                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)

                    if file_name.endswith('.m') or file_name.endswith('.mm') \
                            or file_name.endswith('.h') or file_name.endswith('.pch'):
                        # imageNamed:@"icon_add_collection"
                        old_ref_b = '@"%s"' % old_ref
                        new_ref_b = '@"%s"' % new_ref

                        if old_ref_b in file_data:
                            file_new_data = file_data.replace(old_ref_b, new_ref_b)
                        else:
                            continue

                    elif file_name.endswith('.storyboard') or file_name.endswith('.xib'):
                        old_ref_m = '<image name="%s"' % old_ref
                        new_ref_m = '<image name="%s"' % new_ref
                        file_new_data = file_data.replace(old_ref_m, new_ref_m)

                        # image = "icon_add_collection"

                        old_ref_c = 'image="%s"' % old_ref
                        new_ref_c = 'image="%s"' % new_ref
                        file_new_data = file_new_data.replace(old_ref_c, new_ref_c)

                        # highlightedImage =
                        old_ref_h = 'highlightedImage="%s"' % old_ref
                        new_ref_h = 'highlightedImage="%s"' % new_ref
                        file_new_data = file_new_data.replace(old_ref_h, new_ref_h)

                    wite_data_to_file(file_path, file_new_data)

# highlightedImage="
def find_highlightedImage(res_path):

    if os.path.exists(res_path):
        list_dirs = os.walk(res_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm') \
                        or file_name.endswith('.h') or file_name.endswith('.pch') or \
                        file_name.endswith('.storyboard') or file_name.endswith('.xib'):  # oc文件

                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)
                    if 'highlightedImage=' in file_data:
                        print file_name


storyboard_new_prefix = "FaCai"
storyboard_old_prefix = "UKRosRed"
def rename_storyboard_name(storyboard_path):

    project_content_path = os.path.join(xcode_project_path, 'project.pbxproj')
    project_content = read_file_data(project_content_path)

    if os.path.exists(storyboard_path):
        list_dirs = os.walk(storyboard_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name.endswith(".storyboard"):

                    if storyboard_new_prefix and file_name.startswith(storyboard_new_prefix): #已经存在前缀，不处理
                        continue

                    file_name_no_extension = os.path.splitext(file_name)[0]
                    file_extension = os.path.splitext(file_name)[1]

                    if not storyboard_new_prefix and not storyboard_old_prefix:  # 此种情况为删除前缀
                        continue

                    print '正在处理文件：' + file_name
                    file_new_name = get_new_file_name_for_oc(file_name, storyboard_old_prefix, storyboard_new_prefix)  # 新文件名字
                    file_old_path = os.path.join(root, file_name)
                    file_new_path = os.path.join(root, file_new_name)

                    try:
                        os.rename(file_old_path, file_new_path)  # 更改文件名

                        file_new_name_no_extension = os.path.splitext(file_new_name)[0]

                        old_xxx = 'kLoadStoryboardWithName(@"' + file_name_no_extension + '")'

                        new_xxx = 'kLoadStoryboardWithName(@"' + file_new_name_no_extension + '")'

                        modify_storyboard_reference(oc_all_path, old_xxx, new_xxx)

                        project_content = replace_xproject_data_reference(project_content, file_name, file_new_name)

                        print '处理完成' + file_name
                    except:
                        print '文件无法更改名称：' + file_old_path
                        continue


        wite_data_to_file(project_content_path, project_content)
        # print '修改完成 file_count:' + str(file_count) + "  handle_file_count:" + str(handle_file_count)

def replace_xproject_data_reference(xproject_data, old_file_name, new_file_name):
    return replace_data_by_word(xproject_data, old_file_name, new_file_name)


def get_new_file_name(file_name, old_prefix, new_prefix): #new_prefix为空表示去掉前缀

    if new_prefix and file_name.startswith(new_prefix):  # 已经存在前缀，不处理
        return file_name

    if old_prefix.strip() and file_name.startswith(old_prefix):  # 存在旧前缀，替换掉
        new_file_name = file_name.replace(old_prefix, new_prefix)
    else:

        new_file_name = new_prefix + file_name
    return new_file_name



def get_new_file_name_for_oc(file_name, old_prefix, new_prefix): #new_prefix为空表示去掉前缀

    if '+' in file_name: #分类
        file_name_s = file_name.split('+')
        category_class = file_name_s[0]
        category_name = file_name_s[1]
        if new_prefix and category_name.startswith(new_prefix):  # 已经存在前缀，不处理
            return file_name

        if old_prefix.strip() and category_name.startswith(old_prefix):  # 存在旧前缀，替换掉
            category_name_new = category_name.replace(old_prefix, new_prefix)
        else:

            category_name_new = new_prefix + category_name

        return category_class + '+' + category_name_new


    if new_prefix and file_name.startswith(new_prefix):  # 已经存在前缀，不处理
        return file_name

    if old_prefix.strip() and file_name.startswith(old_prefix):  # 存在旧前缀，替换掉
        new_file_name = file_name.replace(old_prefix, new_prefix)
    else:

        new_file_name = new_prefix + file_name
    return new_file_name



def replace_file_content_by_word(file_path, old_content, new_content):

    file_data = read_file_data(file_path)

    # have_the_word_in_data(file_data, old_content)
    old_content = '\\b' + old_content + '\\b'
    png_old_name_re = re.compile(old_content)
    result2 = re.sub(png_old_name_re, new_content, file_data)
    # new_f_all_txt = file_data.replace(png_old_name, png_new_name)

    f_obj = open(file_path, 'w')  # 首先先创建一个文件对象
    f_obj.write(result2)
    f_obj.flush()
    f_obj.close()

def wite_data_to_file(file_path, data):
    f_obj = open(file_path, mode='w')  # 首先先创建一个文件对象
    f_obj.write(data)
    f_obj.flush()
    f_obj.close()


def replace_data_by_word(data, old_content, new_content):

    if '+' in old_content:
        new_data = data.replace(old_content, new_content)
    else:

        # old_content = '\\b' + old_content + '\\b'
        # png_old_name_re = re.compile(old_content)
        new_data = re.sub(r'\b%s\b' % old_content, new_content, data)
    return new_data

def replace_image_data(data, old_content, new_content):
    old_content = '"' + old_content + '"'
    new_content = '"' + new_content + '"'
    # png_old_name_re = re.compile(old_content)
    # new_data = re.sub(png_old_name_re, new_content, data)
    new_data = data.replace(old_content, new_content)
    return new_data


def replace_data_content(data, old_content, new_content):

    png_old_name_re = re.compile(old_content)

    new_data = re.sub(png_old_name_re, new_content, data)
    return new_data


def replace_data_content22(data, old_content, new_content, delete):

    png_old_name_re = re.compile(old_content)

    if delete:
        aaa = png_old_name_re.match(data)
        new_data = data.replace(old_content, aaa.group(0))

    else:
        new_data = re.sub(png_old_name_re, new_content, data)
    return new_data


def have_the_word_in_data(data, the_str):

    word_pattern = '\\b' + the_str + '\\b'
    match_obj = re.search(re.compile(word_pattern), data)
    # if match_obj:
    #     print match_obj.group()
    return match_obj

def read_file_data(file_path):
    f_obj = open(file_path, mode="r")  # 首先先创建一个文件对象
    f_data = f_obj.read()  # 用read()方法读取文件内容
    f_obj.close()
    return f_data


def modify_sdk_bundle_image_name(image_dir_path, src_dir_path, image_exclude_files):

    if os.path.exists(image_dir_path):
        list_dirs = os.walk(image_dir_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                file_path = os.path.join(root, file_name)  # 文件路径

                # match_obj = re.findall(re.compile('\"\w+\(%s|%d\)\w+\.png\\b'), file_data)
                if file_name.endswith(".png"):
                    print 'find png file match =>' + file_name
                    file_name_no_extension = os.path.splitext(file_name)[0]
                    file_extension = os.path.splitext(file_name)[1]

                    if file_name_no_extension in image_exclude_files:
                        pass
                    else:
                        # 开始修改图片
                        new_image_name_no_extension = random_word_for_image()
                        new_image_name = new_image_name_no_extension + file_extension

                        file_old_path = os.path.join(root, file_name)
                        file_new_path = os.path.join(root, new_image_name)
                        os.rename(file_old_path, file_new_path)

                        modify_image_name_reference(src_dir_path,file_name_no_extension,new_image_name_no_extension)


                # print 'no match'
        # print image_exclude_files



def deleteComments(src_dir_path, exclude_dirs, exclude_files):  # 删除注释

    if os.path.exists(src_dir_path):
        list_dirs = os.walk(src_dir_path)
        for root, dirs, files in list_dirs:

            has_exclude_dir = 0
            for exclude_dir in exclude_dirs:
                if exclude_dir in root:
                    has_exclude_dir = 1

            if has_exclude_dir == 1:
                continue

            for file_name in files:
                if file_name in exclude_files:
                    continue

                if file_name.endswith('.h') or file_name.endswith('.m') or file_name.endswith(
                        '.mm') or file_name.endswith('.cpp'):
                    file_path = os.path.join(root, file_name)
                    file_data = read_file_data(file_path)

                    # file_data_0 = replace_data_content(file_data,'/\\*\\*/', '')
                    # file_data_1 = replace_data_content(file_data_0,'([^:/])//.*', '\\1')
                    # file_data_2 = replace_data_content(file_data_1,'^//.*', '')
                    # file_data_3 = replace_data_content(file_data_2,'/\\*{1,2}[\\s\\S]*?\\*/', '')
                    # file_data_4 = replace_data_content(file_data_3,'\\s*\\n', '\\n')

                    # link_list = re.findall('@"\w+://\w*',file_data)
                    # if link_list:
                    #     for link in link_list:
                    #         link_temp = link.replace('://', 'KKKKKK')
                    #         file_data = file_data.replace(link, link_temp)

                    file_data = oc_code_util.removeAnnotate(file_data)

                    # file_data = file_data.replace('KKKKKK', '://')
                    wite_data_to_file(file_path, file_data)


def addNewComments(src_dir_path,comment_exclude_dirs, comment_file_path):

    if not os.path.exists(comment_file_path):
        print("comment_file_path not exist")
        return

    aaa_data = read_file_data(comment_file_path)

    # str2 = aaa_data.decode('windows-1252')
    # comment_data = str2.encode('utf-8')
    print chardet.detect(aaa_data)
    # comment_data = aaa_data
    comment_data = aaa_data.decode('utf-8')
    comment_data_length = len(comment_data)


    # wite_data_to_file('/Users/gan/iospro/game/afaefae22222.txt', aaa_data)
    # fencoding = chardet.detect(aaa_data)
    # print 'fencoding ' + fencoding
    # aa = 'eee'
    # if aa:
    #     return

    # mmm_not = ['#ifndef','#import','#include','#endif','#define']

    if os.path.exists(src_dir_path):
        list_dirs = os.walk(src_dir_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if 'google' in root or 'bind' in root:
                    continue

                exclude_dir_flag = 0
                for exclude_dir in comment_exclude_dirs:
                    if exclude_dir in root:
                        exclude_dir_flag = 1
                if exclude_dir_flag == 1:
                    continue

                if file_name.endswith('.h') or file_name.endswith('.m') or file_name.endswith(
                        '.mm') or file_name.endswith('.cpp'):
                    file_path = os.path.join(root, file_name)

# ============
                    src_data = read_file_data(file_path)
                    print chardet.detect(src_data)
                    src_data = src_data.decode('utf-8')

                    # 删除原来的注释
                    file_data_0 = replace_data_content(src_data, '/\\*\\*/', '')
                    file_data_1 = replace_data_content(file_data_0, '([^:/])//.*', '\\1')
                    file_data_2 = replace_data_content(file_data_1, '^//.*', '')
                    file_data_3 = replace_data_content(file_data_2, '/\\*{1,2}[\\s\\S]*?\\*/', '')
                    # file_data_4 = replace_data_content(file_data_3, '\\s*\\n', '\\n')

                    src_data = file_data_3
                    #删除注释完成

                    # data_list = list(src_data)
                    #
                    # huan_hang_pos = []
                    # for m in re.finditer('\n', src_data):
                    #     # print(m.start(), m.end())
                    #     # print(m.end())
                    #
                    #     huan_hang_pos.append(m.end())
                    #
                    # for pos in reversed(huan_hang_pos):
                    #     # print(m.start(), m.end())
                    #
                    #     isneed = random.randint(1, 20)  # 随机决定是否改行需要添加注释
                    #     if 8 <= isneed <= 10:  # 添加注释
                    #         new_comment_len = random.randint(10, 400)  # 随机产生注释长度,最少10，最长不超400字符
                    #         new_comment_start_index = random.randint(0, comment_data_length - 401)  # 随机注释文章的起始位置
                    #         new_comment = comment_data[new_comment_start_index: new_comment_start_index + new_comment_len]
                    #
                    #         comment_type = random.randint(1, 3)  # 随机注释类型
                    #
                    #         if comment_type == 2:
                    #
                    #             comment_data_2 = new_comment.replace('\n', '\n//')
                    #             comment_data_2 = comment_data_2 + '\n'
                    #             data_list.insert(pos, '//' + comment_data_2)
                    #
                    #         else:
                    #
                    #             comment_data_2 = '\n/**\n  ' + new_comment + ' \n**/\n'
                    #             # content = content + line + comment_data_2
                    #             data_list.insert(pos, comment_data_2)
                    #
                    # content = ''.join(data_list)
                    # # content = unicode(content, "utf-8")
                    #
                    # try:
                    #     content = content.encode("utf-8")
                    # except:
                    #     print "encode error:" + file_path
                    #     pass
                    # wite_data_to_file(file_path, content)
# =========

                    wite_data_to_file(file_path, src_data)
                    f_obj = open(file_path, "r")
                    text_lines = f_obj.readlines()

                    content = ''
                    print '处理中  ' + file_name
                    for line in text_lines:
                        print chardet.detect(line)
                        line = line.decode('utf-8')

                        if '\\' not in line.strip():
                            isneed = random.randint(1, 20) #随机决定是否改行需要添加注释
                            if 8 <= isneed <= 10:#添加注释
                                new_comment_len = random.randint(10, 300) #随机产生注释长度,最少10，最长不超400字符
                                new_comment_start_index = random.randint(0, comment_data_length - 301) #随机注释文章的起始位置
                                new_comment = comment_data[new_comment_start_index : new_comment_start_index + new_comment_len]

                                comment_type = random.randint(1, 3) #随机注释类型

                                if comment_type == 2:

                                    comment_data_2 = new_comment.replace('\n', '\n//')
                                    comment_data_2 = comment_data_2 + '\n'
                                    content = content + line + '//' + comment_data_2

                                else:

                                    comment_data_2 = '\n/**\n  ' + new_comment + ' \n**/\n'
                                    content = content + line + comment_data_2

                            else:
                                content = content + line

                                # start = random.randint(1, data_length - 600)
                                # comment_length = random.randint(1, 300)
                                # comment_data = aaa_data[start: start + comment_length]
                        else:
                            content = content + line

                    wite_data_to_file(file_path, content)

method_return_type = ['void', 'NSString *', 'BOOL', 'CGFloat', 'NSUInteger']
method_params_type = ['NSString *', 'BOOL', 'CGFloat', 'NSUInteger']
jisuan_type = ['*', '/', '+', '-']

cpp_base_type = ['int', 'bool', 'void', 'int32_t', 'int64_t', 'double']
def addNoUseMethodForCpp2(src_dir_path, exclude_dirs, exclude_files):
    if not os.path.exists(src_dir_path):
        print("src_dir_path not exist")
        return

    list_dirs = os.walk(src_dir_path)
    for root, dirs, files in list_dirs:

        exclude_dir_flag = 0
        for exclude_dir in exclude_dirs:
            if exclude_dir in root:
                exclude_dir_flag = 1
        if exclude_dir_flag == 1:
            continue

        for file_name in files:
            if file_name == ".DS_Store":
                continue

            if file_name in exclude_files:
                continue
            # if 'AFNetworking' in root or 'YYModel' in root:
            #     continue

            if file_name.endswith('.cpp'):
                file_path = os.path.join(root, file_name)

                f_obj = open(file_path, "r")
                text_lines = f_obj.readlines()

                content = ''
                has_implementation = 0
                print '处理中  ' + file_name
                start_insert_method = 0
                pre_line = ''
                for line in text_lines:
                    # print chardet.detect(line)
                    # try:
                    #     line = line.decode('utf-8')
                    # except:
                    #     pass
                    line = line.decode('utf-8')
                    line_strip = line.strip()
                    if(line_strip.endswith('{')):
                        start_insert_method = 1

                    if start_insert_method == 1 \
                            and line_strip.endswith(';') \
                            and not line_strip.startswith('};') \
                            and not line_strip.startswith('USING') \
                            and not line_strip.startswith('static') \
                            and not line_strip.startswith('for') \
                            and not line_strip.startswith('break') \
                            and not line_strip.startswith('//') and not line_strip.startswith('#define'): #无效代码插入位置

                        isneed = random.randint(1, 20) #随机决定是否改行需要添加代码
                        if 4 <= isneed <= 8:#添加
                            code_temp = ''
                            aType = random.randint(1,6)
                            if aType == 1:
                                vars, code_temp = cpp_code_util.cpp_code_auto_create1()
                            elif aType == 2:
                                vars, code_temp = cpp_code_util.cpp_code_auto_create2()
                            elif aType == 3:
                                vars, code_temp = cpp_code_util.cpp_switch_code()
                            else:
                                code_temp = cpp_code_temp_aar[random.randint(0, len(cpp_code_temp_aar) -1)]
                            code_temp = cpp_code_util.replace_code_placeholder(code_temp,'')
                            code_temp = '\n\t//add my cpp code start\n\t{\n\t' + code_temp + '\n\t}\n\t//add my cpp code end\n\n'

                            if line_strip.startswith('return'):
                                if (pre_line.endswith('else if') or pre_line.startswith('if')) and not pre_line.endswith('{') and not line_strip.startswith('{'):
                                    content = content + '\n\t{//add brackets\n\t' + code_temp + '\n\t' + line + '\n\t}//add brackets end \n'
                                elif pre_line.endswith('else') and not pre_line.endswith('#else') and not pre_line.endswith('{') and not line_strip.startswith('{'):
                                    content = content + '\n\t{//add brackets\n\t' + code_temp + '\n\t' + line + '\n\t}//add brackets end \n'
                                else:
                                    content = content + code_temp + '\n' + line
                            else:
                                if (pre_line.endswith('else if') or pre_line.startswith('if')) and not pre_line.endswith('{') and not line_strip.startswith('{'):
                                    content = content + '\n\t{//add brackets\n\t' + line + '\n' + code_temp + '\n\t}//add brackets end \n'
                                elif pre_line.endswith('else') and not pre_line.endswith('#else') and not pre_line.endswith('{') and not line_strip.startswith('{'):
                                    content = content + '\n\t{//add brackets\n\t' + line + '\n' + code_temp + '\n\t}//add brackets end \n'
                                else:
                                    content = content + line + '\n' + code_temp

                        else:
                            content = content + line
                    else:
                        content = content + line
                    if line_strip and not line_strip == '':
                        pre_line = line_strip

                wite_data_to_file(file_path, content)

def addNoUseMethodForCpp(src_dir_path, exclude_dirs, exclude_files):
    if not os.path.exists(src_dir_path):
        print("src_dir_path not exist")
        return
    cppReturnType = ['int32_t','int64_t']
    list_dirs = os.walk(src_dir_path)
    for root, dirs, files in list_dirs:

        exclude_dir_flag = 0
        for exclude_dir in exclude_dirs:
            if exclude_dir in root:
                exclude_dir_flag = 1
        if exclude_dir_flag == 1:
            continue

        for file_name in files:
            if file_name == ".DS_Store":
                continue

            if file_name in exclude_files:
                continue
            # if 'AFNetworking' in root or 'YYModel' in root:
            #     continue

            if file_name.endswith('.cpp'):
                file_path = os.path.join(root, file_name)

                f_obj = open(file_path, "r")
                text_lines = f_obj.readlines()

                content = ''
                has_implementation = 0
                print '处理中  ' + file_name
                for line in text_lines:
                    # print chardet.detect(line)
                    line = line.decode('utf-8')
                    line_strip = line.strip()
                    if line_strip.startswith('static inline'): #方法插入位置

                        isneed = random.randint(1, 20) #随机决定是否改行需要添加无用方法
                        if 4 <= isneed <= 6:#添加

                            method_count = random.randint(1, 2) #随机产生插入的方法数量
                            new_add_method_content = ''
                            for i in range(method_count):

                                return_type = cppReturnType[random.randint(0, len(cppReturnType)-1)] #随机方法返回类型
                                noUserMethod_name = random_word_for_no_use_method_for_cpp()

                                method_content = '\n' + '   static inline ' + return_type + ' mwdk_' + noUserMethod_name + '() {\n'

                                params_counts = random.randint(0, 5) #随机参数个数,最大5个
                                eee = str(random.randint(2,999999))
                                qqq = str(random.randint(880, 999990))
                                # dd = 'return static_cast<%s> (floor(%s) * %s);\n }\n' % (return_type, eee, qqq)
                                if params_counts == 0:
                                    method_content = method_content + '     return static_cast<%s> (floor(%s) * %s);\n  }\n' % (return_type, eee, qqq)

                                elif params_counts == 1:
                                    method_content = method_content + '     return static_cast<%s> (abs(%s) - %s);\n    }\n' % (return_type, eee, qqq)

                                elif params_counts == 2:
                                    method_content = method_content + '     return static_cast<%s> (%s - %s);\n     }\n' % (return_type, eee, qqq)

                                elif params_counts == 3:
                                    method_content = method_content + '     return static_cast<%s> (%s + %s);\n     }\n' % (return_type, eee, qqq)
                                elif params_counts == 4:
                                    method_content = method_content + '     return static_cast<%s> (ceil(%s) + %s);\n   }\n' % (return_type, eee, qqq)

                                elif params_counts == 5:
                                    method_content = method_content + '     return static_cast<%s> (exp(%s) + %s);\n    }\n' % (return_type, eee, qqq)

                                new_add_method_content = new_add_method_content + method_content
                            content = content + new_add_method_content + '\n' + line



                        else:
                            content = content + line
                    else:
                        content = content + line

                wite_data_to_file(file_path, content)

def haveOfforceInSources(oc_path, xofforce):
    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm'):  # oc文件

                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)
                    if xofforce in file_data:
                        return True

        return False

    return False


#找出方法名字，修改方法名
def modify_class_method(src_dir, exclude_dirs,var_exclude_change_dirs, exclude_files, exclude_method_name):

    mthod_params_list = []
    mthod_arr2 = []
    property_list = []
    if os.path.exists(src_dir):
        list_dirs = os.walk(src_dir)
        for root, dirs, files in list_dirs:

            has_exclude_dir = 0
            for exclude_dir in exclude_dirs:
                if exclude_dir in root:
                    has_exclude_dir = 1

            if has_exclude_dir == 1:
                continue

            for file_name in files:

                if file_name == ".DS_Store" or file_name in exclude_files:
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm'):#
                    file_path = os.path.join(root, file_name)  # 头文件路径

                    # 找出这个类的属性，包含.h
                    class_property_list = []
                    file_path_h = file_path.replace('.mm', '.h')
                    file_path_h = file_path_h.replace('.m', '.h')
                    if os.path.exists(file_path_h):

                        file_data_h = file_util.read_file_data(file_path_h)
                        if file_data_h:
                            property_list_h = re.findall(r'@property.+ \*?(\w+);', file_data_h)
                            if property_list_h:  # 存在属性
                                for property_h in property_list_h:
                                    print property_h
                                    if property_h not in class_property_list:
                                        class_property_list.append(property_h)

                    file_data_m = read_file_data(file_path)
                    property_list_m = re.findall(r'@property.+ \*?(\w+);', file_data_m)
                    if property_list_m:  # 存在属性
                        for property_m in property_list_m:
                            print property_m
                            if property_m not in class_property_list:
                                class_property_list.append(property_m)

                    method_def_list = re.findall(r'[-+] {0,3}\(\w+\) {0,2}\w+[\s\S]*?\{', file_data_m) #找出所有该文件方法
                    if method_def_list:
                        for method_content in method_def_list:
                            print method_content
                            if 'IBAction' in method_content: #犹豫别人工程的原因，这里先忽略这种
                                continue

                            mthod_params_list2 = []
                            if ':' in method_content:
                                method_params = re.findall(r'\b\w+:', method_content)
                                for param in method_params:
                                    param_1 = param.replace(':','').replace(' ','')
                                    mthod_params_list2.append(param_1)
                                    if param_1 not in mthod_params_list and param_1 not in exclude_method_name and param_1 not in class_property_list:
                                        mthod_params_list.append(param_1)
                            else:
                                method_params = re.findall(r'\) {0,3}\b\w+\b', method_content) #其实只会有一个
                                for param in method_params:
                                    param_1 = param.replace(')', '').replace(' ', '')
                                    mthod_params_list2.append(param_1)
                                    if param_1 not in mthod_params_list and param_1 not in exclude_method_name and param_1 not in class_property_list:
                                        mthod_params_list.append(param_1)
                            print mthod_params_list2



    print '=============================='
    print '=============================='
    print mthod_params_list
    print '=============================='
    print '=============================='
    iii = 1
    if iii==1:
        return
    method_property_same_temp = []
    method_property_have_tag = []
    for xa in mthod_arr2:
        # print "%s" % xa
        if '_MMMethodMMM' in xa:
            method_property_have_tag.append(xa)

        for property in property_list:
            if property == xa or ('is' + property).lower() in xa.lower() or ('get' + property).lower() in xa.lower() or ('set' + property).lower() in xa.lower() :
                if xa not in method_property_same_temp:
                    method_property_same_temp.append(xa)

    for same_temp in method_property_same_temp:
        mthod_arr2.remove(same_temp)

    for method_tag in method_property_have_tag:
        mthod_arr2.remove(method_tag)

    for xa in mthod_arr2:
        print "%s" % xa

    # xx = 1
    # if xx:
    #     return
    if mthod_arr2 and len(mthod_arr2) > 0:
        if os.path.exists(src_dir):
            list_dirs = os.walk(src_dir)
            for root, dirs, files in list_dirs:

                has_exclude_dir = 0
                for exclude_dir in var_exclude_change_dirs:
                    if exclude_dir in root:
                        has_exclude_dir = 1

                if has_exclude_dir == 1:
                    continue

                for file_name in files:
                    if file_name == ".DS_Store":
                        continue

                    if file_name.endswith('.m') or file_name.endswith('.mm') or file_name.endswith('.h'):#
                        file_path = os.path.join(root, file_name)  # 头文件路径
                        file_data = read_file_data(file_path)
                        for method_name_x in mthod_arr2:
                            method_name_x = method_name_x.strip()
                            if method_name_x is None or method_name_x == '':
                                continue
                            if ':' in method_name_x:
                                method_name_aaaa = method_name_x.replace(':', '')

                                # 修改方法定义的第一个
                                file_data = file_data.replace(')' + method_name_x,
                                                              ')' + method_name_aaaa + '_MMMethodMMM:')
                                file_data = file_data.replace(') ' + method_name_x,
                                                              ') ' + method_name_aaaa + '_MMMethodMMM:')
                                file_data = file_data.replace(')  ' + method_name_x,
                                                              ')  ' + method_name_aaaa + '_MMMethodMMM:')

                                # 修改方法定义或者引用
                                file_data = file_data.replace(' ' + method_name_x, ' ' + method_name_aaaa + '_MMMethodMMM:')

                                if '@selector(' + method_name_x + ')' in file_data:
                                    print '@selector(' + method_name_x + ')'
                                    file_data = file_data.replace('@selector(' + method_name_x + ')',
                                                              '@selector(' + method_name_aaaa + '_MMMethodMMM:)')

                                # file_data = re.sub('\\) *' + method_name_x + '\\b',
                                #                    ')' + method_name_x + '_MMMethodMMM', file_data)

                            else:

                                file_data = re.sub('\\) *' + method_name_x + '\\b', ')' + method_name_x + '_MMMethodMMM', file_data)

                                # 修改方法定义或者引用
                                file_data = file_data.replace(' ' + method_name_x + ']', ' ' + method_name_x + '_MMMethodMMM]')
                                file_data = file_data.replace(' ' + method_name_x + ' ]', ' ' + method_name_x + '_MMMethodMMM]')
                                file_data = file_data.replace(' ' + method_name_x + '  ]', ' ' + method_name_x + '_MMMethodMMM]')
                                if '@selector(' + method_name_x + ')' in file_data:
                                    print '@selector(' + method_name_x + ')'
                                    file_data = file_data.replace('@selector(' + method_name_x + ')',
                                                              '@selector(' + method_name_x + '_MMMethodMMM)')
                                # 修改方法定义的第一个
                                # file_data = file_data.replace(')' + method_name_x, ')' + method_name_x + '_MMMethodMMM')
                                # file_data = file_data.replace(') ' + method_name_x, ')' + method_name_x + '_MMMethodMMM')
                                # file_data = file_data.replace(')  ' + method_name_x,
                                #                               ')' + method_name_x + '_MMMethodMMM')
                                # print 'sss'

                        wite_data_to_file(file_path, file_data)


def find_method_name_by_tag(src_dir_path):

    xxxresult = []
    if os.path.exists(src_dir_path):
        list_dirs = os.walk(src_dir_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name.endswith('.m') or file_name.endswith('.h'):
                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)
                    method_tag_results = re.findall('\\b\\w+_MMMethodMMM', file_data)
                    for xxxd in method_tag_results:
                        if xxxd not in xxxresult:
                            xxxresult.append(xxxd)

    if xxxresult:
        for xssss in xxxresult:

            w1, w2 = random_2word()
            if xssss.startswith('initWith'):
                ww = 'initWith' + w1.capitalize() + w2.capitalize()
            elif xssss.startswith('init'):
                ww = 'init' + w1.capitalize() + w2.capitalize()
            else:
                ww = w1.lower() + w2.capitalize() + '_' + random_1word().capitalize()

            print '#define ' + xssss + '   ' + ww

def find_string_tag(src_dir_path,exclude_dirs,exclude_strings, encrpty_key,encrpty_iv):

    xxxresult = []
    if os.path.exists(src_dir_path):
        list_dirs = os.walk(src_dir_path)
        for root, dirs, files in list_dirs:

            has_exclude_dir = 0
            for exclude_dir in exclude_dirs:
                if exclude_dir in root:
                    has_exclude_dir = 1

            if has_exclude_dir == 1:
                continue

            for file_name in files:

                if file_name.endswith('.m') or file_name.endswith('.mm') or file_name.endswith('.h'):
                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)
                    file_data = unicode(file_data)
                    compile_pp = re.compile(u'@"[\\w.#\u4e00-\u9fa5]+"')  #中文 ：\u4e00-\u9fa5
                    method_tag_results = compile_pp.findall(file_data)
                    # method_tag_results = re.findall(r'@"[\w.#]+"', file_data)
                    for xxxd in method_tag_results:
                        if xxxd not in xxxresult:
                            xxxresult.append(xxxd)

    if xxxresult:
        # wanxianmzxqKEY, eIV = wanxianmzxqIV
        pc = PrpCrypt(encrpty_key, encrpty_iv)  # 初始化密钥
        for xssss in xxxresult:

            xssss_vale = xssss[2 : len(xssss)-1]

            # defineVale_test = '#define %s Decrypt_AllStringContent(@"%s")  //%s' % (xssss, xssss_vale, xssss)
            # print defineVale_test

            if xssss_vale in exclude_strings:
                continue

            w1, w2 = random_2word()
            # 匹配所有汉字
            # print(re.findall(u'[\u4e00-\u9fa5]', xssss_vale))
            # if re.match(u'[\u4e00-\u9fa5]', xssss_vale):
            if re.findall(u'[\u4e00-\u9fa5]', xssss_vale):

                ssa = "wwwww_tag_wwwww_" + w1 + '_' + w2
            else:
                ssa = "wwwww_tag_wwwww_" + xssss_vale
            ssa = ssa.replace(".","_").replace("#","_CC_")
            encryptValue = pc.aes_encrypt(xssss_vale)
            if encryptValue.endswith('\n'):
                encryptValue = encryptValue[0:len(encryptValue)-1]

            # defineVale = '#define %s        Decrypt_AllStringContent_2(@"%s")  //%s' % (ssa, encryptValue, xssss)
            defineVale = '#define %s        %s  //%s' % (ssa, xssss, xssss)
            print defineVale

            if os.path.exists(src_dir_path):
                list_dirs = os.walk(src_dir_path)
                for root, dirs, files in list_dirs:

                    has_exclude_dir = 0
                    for exclude_dir in exclude_dirs:
                        if exclude_dir in root:
                            has_exclude_dir = 1

                    if has_exclude_dir == 1:
                        continue

                    for file_name in files:

                        if file_name.endswith('.m') or file_name.endswith('.mm') or file_name.endswith('.h'):
                            file_path = os.path.join(root, file_name)  # 头文件路径
                            file_data = read_file_data(file_path)
                            if xssss in file_data:
                                file_data = file_data.replace(xssss, ssa)
                                wite_data_to_file(file_path, file_data)

def replace_string_tag(src_dir_path,exclude_dirs,exclude_strings, re_pr, encrpty_key,encrpty_iv):

    xxxresult = []
    if os.path.exists(src_dir_path):
        list_dirs = os.walk(src_dir_path)
        for root, dirs, files in list_dirs:

            has_exclude_dir = 0
            for exclude_dir in exclude_dirs:
                if exclude_dir in root:
                    has_exclude_dir = 1

            if has_exclude_dir == 1:
                continue

            for file_name in files:

                if file_name.endswith('.m') or file_name.endswith('.h'):
                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)
                    file_data = unicode(file_data)
                    compile_pp = re.compile(re_pr)  #中文 ：\u4e00-\u9fa5
                    method_tag_results = compile_pp.findall(file_data)
                    # method_tag_results = re.findall(r'@"[\w.#]+"', file_data)
                    for xxxd in method_tag_results:
                        if xxxd not in xxxresult:
                            xxxresult.append(xxxd)

    if xxxresult:
        if encrpty_key and encrpty_iv:
            # wanxianmzxqKEY, eIV = wanxianmzxqIV
            pc = PrpCrypt(encrpty_key, encrpty_iv)  # 初始化密钥
        for xssss in xxxresult:

            xssss_vale = xssss[2 : len(xssss)-1]

            # defineVale_test = '#define %s Decrypt_AllStringContent(@"%s")  //%s' % (xssss, xssss_vale, xssss)
            # print defineVale_test

            if xssss_vale in exclude_strings:
                continue

            w1, w2 = random_2word()
            ssa = w1 + '_' + w2
            encryptValue = pc.aes_encrypt(xssss_vale)
            if encryptValue.endswith('\n'):
                encryptValue = encryptValue[0:len(encryptValue)-1]

            defineVale = '#define %s        Decrypt_AllStringContent_2(@"%s")  //%s' % (ssa, encryptValue, xssss)
            print defineVale

            # if os.path.exists(src_dir_path):
            #     list_dirs = os.walk(src_dir_path)
            #     for root, dirs, files in list_dirs:
            #
            #         has_exclude_dir = 0
            #         for exclude_dir in exclude_dirs:
            #             if exclude_dir in root:
            #                 has_exclude_dir = 1
            #
            #         if has_exclude_dir == 1:
            #             continue
            #
            #         for file_name in files:
            #
            #             if file_name.endswith('.m') or file_name.endswith('.h'):
            #                 file_path = os.path.join(root, file_name)  # 头文件路径
            #                 file_data = read_file_data(file_path)
            #                 if xssss in file_data:
            #                     file_data = file_data.replace(xssss,ssa)
            #                     wite_data_to_file(file_path,file_data)

def changeStringHeaderValue(header_path):
    global f_obj, text_lines, line
    f_obj = open(header_path, "r")
    text_lines = f_obj.readlines()
    for line in text_lines:
        line = line.decode('utf-8')
        if 'wwwww_tag_wwwww' in line:
            str_result = re.findall('//@"(.+)"', line)  # @"[\\w.]+"
            if str_result:
                str_result_1 = str_result[0]
                # str_result_1 = str_result_1[4: len(str_result_1) - 1]
                aes_encrypt_result = pc.aes_encrypt(str_result_1)
                defineVale = 'Decrypt_AllStringContent(@"%s")' % (aes_encrypt_result)

                if 'Decrypt_AllStringContent' in line:
                    line = re.sub('Decrypt_AllStringContent\\(@".+"\\)', defineVale, line)
                    if line.endswith('\n'):
                        line = line.replace('\n', '')
                    print line
                else:
                    line = re.sub('  @".+" ', "  " + defineVale + " ", line)
                    if line.endswith('\n'):
                        line = line.replace('\n', '')
                    print line


def changeMethodHeaderValue(header_path):

    f_obj = open(header_path, "r")
    text_lines = f_obj.readlines()
    for line in text_lines:
        line = line.decode('utf-8')
        if '_MMMethodMMM' in line:
            str_result = re.findall(r'#define +\w+_MMMethodMMM ', line)  # @"[\\w.]+"
            if str_result:
                str_result_1 = str_result[0]
                method_name = str_result_1.replace('#define ', '').strip()
                w1_dong = random_word_dong()
                w1_name = random_word_name()
                if method_name.startswith('initWith'):
                    method_rep = str_result_1 + "         " + 'initWith' + w1_dong.capitalize() + w1_name.capitalize()
                elif method_name.startswith('init'):
                    method_rep = str_result_1 + "         " + 'init' + w1_dong.capitalize() + w1_name.capitalize()
                else:
                    method_rep = str_result_1 + "         " + w1_dong.lower() + w1_name.capitalize()
                print method_rep

def changeImageNameForDefindHeader(imageDir,header_path):
    if os.path.exists(imageDir):
        list_dirs = os.walk(imageDir)
        header_data = read_file_data(header_path)
        isChange = 0
        for root, dirs, files in list_dirs:
            for file_name in files:
                if file_name.endswith('.png') or file_name.endswith('.jpg'):

                    w1, w2 = random_2word()
                    image_name_new_no_extension = w1.lower() + '_' + w2.lower() + '_img'

                    image_name_no_extension = os.path.splitext(file_name)[0]
                    file_extension = os.path.splitext(file_name)[1]

                    image_name_new = image_name_new_no_extension + file_extension

                    file_old_path = os.path.join(root, file_name)
                    file_new_path = os.path.join(root, image_name_new)
                    os.rename(file_old_path, file_new_path)

                    # @"mmplaygame_apple_signin"
                    image_str_old = "@\"%s\"" % image_name_no_extension
                    image_str_new = "@\"%s\"" % image_name_new_no_extension
                    header_data = header_data.replace(image_str_old, image_str_new)
                    isChange = 1

        if isChange == 1:
            wite_data_to_file(header_path, header_data)

def add_code(src_dir_path,exclude_dirs,exclude_files):#添加垃圾代码

    if os.path.exists(src_dir_path):
        list_dirs = os.walk(src_dir_path)
        for root, dirs, files in list_dirs:

            has_exclude_dir = 0
            for exclude_dir in exclude_dirs:
                if exclude_dir in root:
                    has_exclude_dir = 1

            if has_exclude_dir == 1:
                continue

            for file_name in files:
                if file_name in exclude_files:
                    continue
                if file_name.endswith('.m') or file_name.endswith('.mm') or file_name.endswith('.h'):
                    file_path = os.path.join(root, file_name)
                    oc_class_parser.parse(file_path, sdk_confuse_dir)
                    # oc_class_parser.change_method_params_name(file_path)

def change_method_params_name(src_dir_path,exclude_dirs,exclude_files):#修改方法本地变量

    if os.path.exists(src_dir_path):
        list_dirs = os.walk(src_dir_path)
        for root, dirs, files in list_dirs:

            has_exclude_dir = 0
            for exclude_dir in exclude_dirs:
                if exclude_dir in root:
                    has_exclude_dir = 1

            if has_exclude_dir == 1:
                continue

            for file_name in files:
                if file_name in exclude_files:
                    continue
                if file_name.endswith('.m'):
                    file_path = os.path.join(root, file_name)
                    # oc_class_parser.parse(file_path, sdk_confuse_dir)
                    oc_class_parser.change_method_params_name(file_path)

def changeXcodeProjectUUid(xcode_project_path): #修改所有uuid

    project_content_path = os.path.join(xcode_project_path, 'project.pbxproj')
    project_data = file_util.read_file_data_utf8(project_content_path)

    # 正则找出所有uuid
    uuid_list = re.findall(r'\b[A-Z0-9]{24}\b', project_data)  # 'fileRef = 03315B9D291DFB7B00A92FBE'
    # uuid_list = re.findall(r'fileRef = [A-Z0-9]{24} ', project_data)

    uuid_temp_list = []
    for mid in uuid_list:
        print mid
        if mid not in uuid_temp_list:
            uuid_temp_list.append(mid)

    for id in uuid_temp_list:
        id_temp = id.strip()
        new_id = oc_method_util.get_uid()
        project_data = project_data.replace(id_temp, new_id)
        print id_temp + '------>' + new_id

    file_util.wite_data_to_file(project_content_path, project_data)


def changeXcodeProjectDir(xcode_project_path, src_dir_path, change_dir_path, dir_prefix):#修改指定目录下的目录名，加前缀
    if os.path.exists(src_dir_path):
        list_dirs = os.walk(src_dir_path)
        project_content_path = os.path.join(xcode_project_path, 'project.pbxproj')
        project_data = file_util.read_file_data_utf8(project_content_path)
        group_list = re.findall(r'Begin PBXGroup section[\s\S]+?End PBXGroup section', project_data)
        if not group_list:
            return
        group_setion_data = group_list[0]
        group_setion_data_1 = group_setion_data
        for root, dirs, files in list_dirs:
            if change_dir_path in root:
                for dir in dirs:
                    if dir.startswith(dir_prefix):
                        continue
                    dir_path_src = os.path.join(root, dir)
                    new_dir = dir_prefix + dir.capitalize()
                    dir_path_dest = os.path.join(root, new_dir)
                    os.rename(dir_path_src, dir_path_dest)

                    # a_uuid_list = re.findall(r'\b\w+\b(?= /\* %s \*/ = \{)' % dir)
                    # a_uuid = a_uuid_list[0]
                    # new_uuid = oc_method_util.get_uid()

                    group_setion_data_1 = re.sub(r'/\* %s \*/' % dir, '/* %s */' % new_dir, group_setion_data_1)
                    group_setion_data_1 = re.sub(r'path = %s;' % dir, 'path = %s;' % new_dir, group_setion_data_1)

                    # group_setion_data_1 = re.sub(r'\b%s\b' % a_uuid, new_uuid, group_setion_data_1)

        project_data = project_data.replace(group_setion_data, group_setion_data_1)

        file_util.wite_data_to_file(project_content_path, project_data)



if __name__ == '__main__':

    # xcode_project_path = '/Users/ganyuanrong/iOSProject/game_mw_sdk_ios_v3/MW_OBS_V3/MW_SDK.xcodeproj'

    # oc_all_path = '/Users/ganyuanrong/iOSProject/game_mw_sdk_ios_v3/MW_OBS_V3/FLSDK'
    # oc_modify_path = '/Users/ganyuanrong/iOSProject/game_mw_sdk_ios_v3/MW_OBS_V3/FLSDK'


    xcode_project_path = '/Users/ganyuanrong/iOSProject/mwsdk_cfuse_v6/GamaSDK_iOS_Integration/MW_SDK.xcodeproj'
    oc_all_path = '/Users/ganyuanrong/iOSProject/mwsdk_cfuse_v6/GamaSDK_iOS_Integration/FLSDK'
    oc_modify_path = '/Users/ganyuanrong/iOSProject/mwsdk_cfuse_v6/GamaSDK_iOS_Integration/FLSDK'


    handle_file_count = 0
    file_count = 0
    sdk_confuse_dir = '/Users/ganyuanrong/PycharmProjects/SdkTools/modifyXcodeProject/sdk_confuse/'
    woords_file_path = sdk_confuse_dir + 'confuse_words_2.log'
    genest_word = words_reader(woords_file_path)

    words_dong = words_reader(sdk_confuse_dir + 'word_dong.log')
    words_name = words_reader(sdk_confuse_dir + 'word_ming.log')
    word_util.words_name = words_name
    word_util.words_dong = words_dong
    word_util.genest_word = genest_word

    for code_i in range(50):
        code_data = file_util.read_file_data_utf8(sdk_confuse_dir + 'code_temples/code_%s.log' % code_i)
        if code_data:
            oc_class_parser.code_temples.append(code_data)

    for code_i in range(20):
        code_data = file_util.read_file_data_utf8(sdk_confuse_dir + 'code_temples/code_if_%s.log' % code_i)
        if code_data:
            oc_class_parser.code_if_temples.append(code_data)

    cpp_code_temp_aar = []
    for code_i in range(50):
        code_data = file_util.read_file_data_utf8(sdk_confuse_dir + 'code_temples_cpp/code_%s.log' % code_i)
        if code_data:
            cpp_code_temp_aar.append(code_data)

    for code_data in cpp_code_temp_aar:
        code_data = re.sub(r'\bbool\b', 'BOOL', code_data)
        oc_class_parser.code_temples.append(code_data)

    #1.修改图片  图片md5需要额外处理
    # image_exclude_files = []
    # image_ref_path = '/Users/ganyuanrong/iOSProject/flsdk_ios_v55/GamaSDK_iOS_Integration/obfuscation'
    # modify_sdk_bundle_image_name("/Users/ganyuanrong/iOSProject/flsdk_ios_v55/GamaSDK_iOS_Integration/Resources/GOT/SDKResourcesV5.bundle/",
    #                              image_ref_path, image_exclude_files)

    # 1.1. 修改已经定义好的defind图片名称
    # changeImageNameForDefindHeader('/Users/ganyuanrong/iOSProject/flsdk_ios_kr/GamaSDK_iOS_Integration/Resources/KR/SDKResourcesKR.bundle',
    #                                '/Users/ganyuanrong/iOSProject/flsdk_ios_kr/GamaSDK_iOS_Integration/obfuscation/imageNameHeader.h')
    # 1.2  改变md5:find . -iname "*.png" -exec echo {} \; -exec convert {} {} \;

    #2. 修改已经定义好的defind中的方法名称
    method_header_path = '/Users/ganyuanrong/iOSProject/flsdk_ios_kr/GamaSDK_iOS_Integration/obfuscation/codeObfuscationForMethodName.h'
    # changeMethodHeaderValue(method_header_path)

    #3.添加随机注释，一般不用
    # oc_all_path = '/Users/ganyuanrong/Desktop/Default-moqumiaowan_9.27-Release-1.0_scussce/Classes/'
    # comment_exclude_dirs = ['sdkFrameworks','Native']
    # addNewComments(oc_all_path, comment_exclude_dirs, '/Users/ganyuanrong/Desktop/sdk_confuse/ofc.log')

    # 4.删除注释
    var_exclude_dirs = ['AFNetworking', 'YYModel', 'ThirdSrc','ThirdResources']
    var_exclude_files = []
    # src_path = '/Users/ganyuanrong/iOSProject/flsdk_ios/GamaSDK_iOS_Integration/FLSDK/'
    src_path = '/Users/ganyuanrong/iOSProject/flsdk_ios_kr/GamaSDK_iOS_Integration/FLSDK/'
    # deleteComments(src_path, var_exclude_dirs, var_exclude_files)

    # 5.修改类名
    oc_exclude_files.extend(
        ['AppDelegate.h', 'MWSDK.h', 'PayData.h', 'LoginData.h', 'AccountModel.h', 'CreateOrderResp.h','UnityAppController.h','UnityAppController+Rendering.h'
         ,'UnityViewControllerBase+iOS.h','UnityViewControllerBase+tvOS.h','UnityViewControllerBase.h','UnityView.h','UnityView+iOS.h','UnityView+tvOS.h'])
    oc_exclude_dirs.extend(['AFNetworking', 'Masonry', 'YYModel', 'Model', 'sdkFrameworks', "Resources",'ThirkLib','ThirdSrc'])
    # "ThirkLib", "Model", "YYModel", "AFNetworking", "Plat", "WorkProjResources", "Resources", "obfuscation", "Demo"
    oc_exclude_dirs_ref_modify = ['ThirkLib', "YYModel", "AFNetworking", "Resources",'ThirdSrc']

    xcode_project_path = '/Users/ganyuanrong/iOSProject/flsdk_ios_kr/GamaSDK_iOS_Integration/MW_SDK.xcodeproj'
    oc_modify_path = '/Users/ganyuanrong/iOSProject/flsdk_ios_kr/GamaSDK_iOS_Integration/FLSDK'
    oc_all_path = '/Users/ganyuanrong/iOSProject/flsdk_ios_kr/GamaSDK_iOS_Integration'
    # modify_oc_class_name(oc_modify_path, xcode_project_path, oc_all_path, oc_exclude_dirs_ref_modify)


    #找出所有方法名字并修改
    # var_exclude_dirs = ['AFNetworking', 'YYModel', 'Plat','sdkFrameworks']
    # var_exclude_change_dirs = ['AFNetworking', 'YYModel','sdkFrameworks','ThirdSDK']
    # var_exclude_files = ['AppDelegate.m', 'MWSDK.m', 'PayData.m', 'LoginData.m', 'AccountModel.m', 'CreateOrderResp.m','USDefault.m','UIAlertController+Sdk.m','DisplayManager.mm']
    # var_exclude_name = ['didBecomeActive','willResignActive','didEnterBackground','willEnterForeground','willTerminate',
    #                     'loadView','target','handleAuthrization','error','delegate','name','selector','didFinishLaunchingWithOptions','application',
    #                     'options','annotation','sourceApplication','openURL','dealloc','show','load','init','drawRect','initialize','encode',
    #                     'decode','length','share','setData','viewWillAppear','viewDidLoad','shouldAutorotate','viewDidDisappear','sharedInstance',
    #                     'forKey','objectForKey','setObject','length','presentingViewController','action','completion','onFrameResolved','keyboardDidShow','keyboardWillHide'
    #                     ,'touchesBegan','touchesEnded','touchesCancelled','touchesMoved','withEvent','layoutSubviews','initWithFrame','didRotate']
    #
    # woords_file_path = '/Users/ganyuanrong/PycharmProjects/SdkTools/modifyXcodeProject/sdk_confuse/not_obs_method.log'
    #
    # f_obj = open(woords_file_path, "r")
    # text_lines = f_obj.readlines()
    # for line in text_lines:
    #     line = line.decode('utf-8')
    #     method_name = line.strip().replace(' ', '').replace(':', '')
    #     var_exclude_name.append(method_name)
    # modify_class_method('/Users/ganyuanrong/Downloads/益乐互动_iOS源码/YLFunSDK/FunctionModule',var_exclude_dirs,var_exclude_change_dirs,var_exclude_files,var_exclude_name)


    # xxxresult = []
    # dataxxx = read_file_data('/Users/ganyuanrong/Desktop/关联文件2.txt')
    # method_tag_results = re.findall('ui/baseui/[/\\w]*\\.png', dataxxx)
    # for xxxd in method_tag_results:
    #     if xxxd not in xxxresult:
    #         xxxresult.append(xxxd)
    #
    # for xxxd in xxxresult:
    #     print xxxd


    # find_string_path = '/Users/ganyuanrong/xzgame/jianghu_ftcs/jianghu_ft/ocSrc'
    # exclude_dirs = ['AFNetworking', 'YYModel','Common','Res','utils']
    # exclude_strings = ['AccountListViewCellID','%@%@','%d','%ld','%@','.']
    # wanxianmzxqKEY = 'xiezongxiezong0717key'
    # wanxianmzxqIV = 'xiezongxiezong0717iv'
    # 找出所有字符使用宏替代
    # find_string_tag(find_string_path, exclude_dirs, exclude_strings, wanxianmzxqKEY, wanxianmzxqIV)

    # eKey=mplaywlzhsKEY,eIV=mplaywlzhsIV
    # dataxxx = read_file_data('/Users/ganyuanrong/Desktop/73d30001bc0f27f512ed3afa30f2feb3.txt')
    # pc = PrpCrypt('SdkV6202304KEY', 'SdkV6202304IV')  # 初始化密钥
    # mmxx = pc.aes_decrypt(dataxxx)
    # print mmxx
    # dataxxx = read_file_data('/Users/ganyuanrong/iOSProject/game_mw_sdk_ios_v3/MW_OBS_V3/Resources/GOT/com_mplay_wlzhs.json')
    # mmxx = pc.aes_encrypt(dataxxx)
    # print mmxx
    # print pc.aes_decrypt(mmxx)

    # mmxx = pc.encrypt(dataxxx)
    # print mmxx
    #
    # mmxx = pc.decrypt(mmxx)
    # print mmxx
    pc = PrpCrypt('mwsdk-kr-0828KEY', 'mwsdk-kr-0828IV')
    changeStringHeaderValue('/Users/ganyuanrong/iOSProject/flsdk_ios_kr/GamaSDK_iOS_Integration/obfuscation/MWStringHeaders.h')

    # oc_class_parser.parse('/Users/ganyuanrong/Desktop/AdDelegate.m')
    #6.添加垃圾代码
    var_exclude_dirs = ['AFNetworking', 'YYModel', 'ThirdSrc']
    var_exclude_files = []
    # # src_path = '/Users/ganyuanrong/iOSProject/flsdk_ios/GamaSDK_iOS_Integration/FLSDK/'
    # src_path = '/Users/ganyuanrong/iOSProject/mwsdk_cfuse_v41/GamaSDK_iOS_Integration/FLSDK/'
    # src_path = '/Users/ganyuanrong/iOSProject/flsdk_ios_vn/GamaSDK_iOS_Integration/FLSDK'
    # src_path = '/Users/ganyuanrong/iOSProject/flsdk_ios_v55/GamaSDK_iOS_Integration/FLSDK'
    src_path = '/Users/ganyuanrong/iOSProject/flsdk_ios_kr/GamaSDK_iOS_Integration/FLSDK'
    # add_code(src_path, var_exclude_dirs, var_exclude_files)

    # xcode_project_path = '/Users/ganyuanrong/iOSProject/flsdk_ios_vn/GamaSDK_iOS_Integration/MW_SDK.xcodeproj'
    # src_path = '/Users/ganyuanrong/iOSProject/flsdk_ios_vn'
    # modify_path = '/Users/ganyuanrong/iOSProject/flsdk_ios_vn/GamaSDK_iOS_Integration/FLSDK'
    #7.指定目录下面的目录加前缀
    # changeXcodeProjectDir(xcode_project_path, src_path, modify_path, 'OPEN')
    # 8.修改所有uuid
    # xcode_project_path = '/Users/ganyuanrong/cpGames/vn_sdk_zkb/Unity-iPhone.xcodeproj'
    xcode_project_path = '/Users/ganyuanrong/iOSProject/flsdk_ios_kr/GamaSDK_iOS_Integration/MW_SDK.xcodeproj'
    # changeXcodeProjectUUid(xcode_project_path)
    #修改函数顺序
    #修改变量名称


    print 'end'
