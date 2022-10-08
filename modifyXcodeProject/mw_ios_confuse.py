#coding=utf-8
import imp
import sys
imp.reload(sys)
sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的

import os
import re

import chardet

# 导入 random(随机数) 模块
import random

genest_word=[]

xcode_project_path = ''

# /Users/gan/Desktop/黑特篮球new2/SkyBetufi/SourceCode/SkySrc/CommonModule/GUtility/PKCategory
oc_all_path = ''
oc_modify_path = ''

handle_file_count = 0
file_count = 0

oc_exclude_files = []
oc_exclude_dirs = []


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


def random_word_for_method():#产生方法名称替代代码方法，使用defind

    for i in range(300):

        first_index = random.randint(0, len(genest_word)-1)
        sec_index = random.randint(0, len(genest_word) - 1)
        if first_index == sec_index:
            sec_index = random.randint(0, len(genest_word) - 1)

        first_word = genest_word[first_index]
        sec_word = genest_word[sec_index]

        new_word = first_word.lower() + sec_word.capitalize()
        print new_word

word_oc_method_temp = []
def random_word_for_no_use_method():

    first_word, sec_word = random_2word()
    new_word = first_word.lower() + sec_word.capitalize()

    while (new_word in word_oc_method_temp):
        first_word, sec_word = random_2word()
        new_word = first_word.capitalize() + sec_word.capitalize()

    word_oc_method_temp.append(new_word)
    return new_word




def modify_oc_class_name(oc_path):
    global file_count, handle_file_count, fia

    project_content_path = os.path.join(xcode_project_path, 'project.pbxproj')
    project_content = read_file_data(project_content_path)

    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store" or file_name.endswith(".swift"):
                    continue

                file_count = file_count + 1

                aaa = 1
                for not_dir in oc_exclude_dirs:
                    if not_dir in root:
                        aaa = 2

                if aaa == 2:
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

                        if '+' in file_name:  # 分类
                            fia = file_name_no_extension.split('+')
                            file_new_name = fia[0] + "+" + new_word + '.m'
                            header_file_new_name = fia[0] + "+" + new_word + '.h'



                        else:
                            file_new_name = new_word + '.m'
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


                        modify_oc_class_reference(oc_all_path, file_name_no_extension, file_new_name_no_extension)

                        # 更改xproject文件中的.m
                        project_content = replace_xproject_data_reference(project_content, file_name, file_new_name)

                        # 更改xproject文件中的.h
                        project_content = replace_xproject_data_reference(project_content, header_file_name, header_file_new_name)

                        handle_file_count = handle_file_count + 1
                        print '处理完成' + file_name

        wite_data_to_file(project_content_path, project_content)
        print '修改完成 file_count:' + str(file_count) + "  handle_file_count:" + str(handle_file_count)


#oc_path 所有源文件，置于一个单独目录最好
def modify_oc_class_reference(oc_path, old_ref, new_ref):

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

                    # if have_the_word_in_data(file_data, old_ref):

                    file_new_data = replace_data_by_word(file_data, old_ref, new_ref)
                    if (file_name.endswith('.m') or file_name.endswith('.h')) and new_ref in file_name and '+' in old_ref and '+' in new_ref: #分类
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

        old_content = '\\b' + old_content + '\\b'
        png_old_name_re = re.compile(old_content)
        new_data = re.sub(png_old_name_re, new_content, data)
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

def deleteComments():#还有问题

    source_dir = '/Users/gan/iospro/game/rongyaodg/app/Classes/device'

    if os.path.exists(source_dir):
        list_dirs = os.walk(source_dir)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if 'google' in root or 'bind' in root:
                    continue

                if file_name.endswith('.h') or file_name.endswith('.m') or file_name.endswith('.mm') or file_name.endswith('.cpp'):

                    file_path = os.path.join(root, file_name)
                    file_data = read_file_data(file_path)

                    file_data_0 = replace_data_content(file_data,'/\\*\\*/', '')
                    file_data_1 = replace_data_content(file_data_0,'([^:/])//.*', '\\1')
                    file_data_2 = replace_data_content(file_data_1,'^//.*', '')
                    file_data_3 = replace_data_content(file_data_2,'/\\*{1,2}[\\s\\S]*?\\*/', '')
                    file_data_4 = replace_data_content(file_data_3,'\\s*\\n', '\\n')

                    wite_data_to_file(file_path, file_data_4)

def addNewComments(src_dir_path, comment_file_path):

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
                    file_data_4 = replace_data_content(file_data_3, '\\s*\\n', '\\n')

                    src_data = file_data_4
                    #删除注释完成

                    data_list = list(src_data)

                    huan_hang_pos = []
                    for m in re.finditer('\n', src_data):
                        # print(m.start(), m.end())
                        # print(m.end())
                        huan_hang_pos.append(m.end())

                    for pos in reversed(huan_hang_pos):
                        # print(m.start(), m.end())

                        isneed = random.randint(1, 20)  # 随机决定是否改行需要添加注释
                        if 5 <= isneed <= 10:  # 添加注释
                            new_comment_len = random.randint(10, 400)  # 随机产生注释长度,最少10，最长不超400字符
                            new_comment_start_index = random.randint(0, comment_data_length - 401)  # 随机注释文章的起始位置
                            new_comment = comment_data[new_comment_start_index: new_comment_start_index + new_comment_len]

                            comment_type = random.randint(1, 3)  # 随机注释类型

                            if comment_type == 2:

                                comment_data_2 = new_comment.replace('\n', '\n//')
                                comment_data_2 = comment_data_2 + '\n'
                                data_list.insert(pos, '//' + comment_data_2)

                            else:

                                comment_data_2 = '\n/**\n  ' + new_comment + ' \n**/\n'
                                # content = content + line + comment_data_2
                                data_list.insert(pos, comment_data_2)

                    content = ''.join(data_list)
                    # content = unicode(content, "utf-8")

                    try:
                        content = content.encode("utf-8")
                    except:
                        print "encode error:" + file_path
                        pass
                    wite_data_to_file(file_path, content)
# =========

                    # f_obj = open(file_path, "r")
                    # text_lines = f_obj.readlines()
                    #
                    # content = ''
                    # print '处理中  ' + file_name
                    # for line in text_lines:
                    #     print chardet.detect(line)
                    #     line = line.decode('utf-8')
                    #
                    #     isneed = random.randint(1, 20) #随机决定是否改行需要添加注释
                    #     if isneed <= 5  and isneed <= 10:#添加注释
                    #         new_comment_len = random.randint(10, 400) #随机产生注释长度,最少10，最长不超400字符
                    #         new_comment_start_index = random.randint(0, comment_data_length - 401) #随机注释文章的起始位置
                    #         new_comment = comment_data[new_comment_start_index : new_comment_start_index + new_comment_len]
                    #
                    #         comment_type = random.randint(1, 3) #随机注释类型
                    #
                    #         if comment_type == 2:
                    #
                    #             comment_data_2 = new_comment.replace('\n', '\n//')
                    #             comment_data_2 = comment_data_2 + '\n'
                    #             content = content + line + '//' + comment_data_2
                    #
                    #         else:
                    #
                    #             comment_data_2 = '\n/**\n  ' + new_comment + ' \n**/\n'
                    #             content = content + line + comment_data_2
                    #
                    #     else:
                    #         content = content + line
                    #
                    #         # start = random.randint(1, data_length - 600)
                    #         # comment_length = random.randint(1, 300)
                    #         # comment_data = aaa_data[start: start + comment_length]
                    #
                    # wite_data_to_file(file_path, content)

method_return_type = ['void', 'NSString *', 'BOOL', 'CGFloat', 'NSUInteger']
method_params_type = ['NSString *', 'BOOL', 'CGFloat', 'NSUInteger']
jisuan_type = ['*', '/', '+', '-']

property_type = ['@property (nonatomic, copy) NSString *', '@property (nonatomic, assign) BOOL ', '@property (nonatomic, strong) NSDictionary *', '@property (nonatomic, assign) NSUInteger ',
                 '@property(nonatomic, weak) id ', '@property (nonatomic, assign) CGFloat ']
def addNoUseMethodAndProperty(src_dir_path, exclude_dirs, exclude_files):
    if not os.path.exists(src_dir_path):
        print("src_dir_path not exist")
        return

    list_dirs = os.walk(src_dir_path)
    for root, dirs, files in list_dirs:

        exclude_dir_flag = 0
        for exclude_dir in exclude_dirs:
            if root.endswith(exclude_dir):
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

            if file_name.endswith('.m') or file_name.endswith('.h'):
                file_path = os.path.join(root, file_name)

                f_obj = open(file_path, "r")
                text_lines = f_obj.readlines()

                content = ''
                has_implementation = 0
                print '处理中  ' + file_name
                for line in text_lines:
                    # print chardet.detect(line)
                    line = line.decode('utf-8')

                    if has_implementation == 0 and '@implementation' in line:
                        has_implementation = 1

                    if has_implementation == 1 and file_name.endswith('.m') and (line.startswith('- (') or line.startswith('+ (')): #方法插入位置

                        # method_public = '+'
                        # if line.startswith('+'):
                        #     method_public = '+'
                        # else:
                        #     method_public = '-'
                        method_public_private = random.randint(1, 5)
                        if method_public_private >= 4:
                            method_public = '+'
                        else:
                            method_public = '-'

                        isneed = random.randint(1, 20) #随机决定是否改行需要添加无用方法
                        if 5 <= isneed <= 10:#添加

                            method_count = random.randint(1, 3) #随机产生插入的方法数量
                            new_add_method_content = ''
                            for i in range(method_count):

                                return_type = method_return_type[random.randint(0, len(method_return_type)-1)] #随机方法返回类型
                                noUserMethod_name = random_word_for_no_use_method()

                                method_content = '\n' + method_public + ' ' + '(' + return_type + ')' + noUserMethod_name


                                params_counts = random.randint(0, 5) #随机参数个数,最大5个
                                if params_counts == 0:

                                    if return_type == 'void':
                                        params_word1 = random_1word()
                                        params_word2 = random_1word()
                                        method_some_things = '[NSString stringWithFormat:@"%s", @"%s" , @"%s"];' % ('%@%@', params_word1, params_word2)
                                        method_content =  method_content + '\n{\n    %s \n}' % (method_some_things)

                                    elif return_type == 'NSString *':
                                        params_word1 = random_1word()
                                        params_word2 = random_1word()
                                        method_some_things = 'return [NSString stringWithFormat:@"%s", @"%s" , @"%s"];' % ('%@%@',params_word1, params_word2)
                                        method_content = method_content + '\n{\n    %s \n}' % (method_some_things)
                                    elif return_type == 'BOOL' or return_type == 'CGFloat' or return_type == 'NSUInteger':
                                        params_word1 = random.randint(1, 10000000)
                                        params_word2 = random.randint(0, 10000000)
                                        params_word3 = random.randint(0, 10000000)
                                        method_some_things = 'return %s * %s + %s ;' % (params_word1, params_word2, params_word3)
                                        method_content = method_content + '\n{\n    %s \n}' % (method_some_things)



                                else:


                                    params_type_string = []
                                    params_type_string = []
                                    params_type_string = []

                                    for m in range(params_counts):
                                        params_word = random_1word()
                                        params_type = method_params_type[random.randint(0, len(method_params_type)-1)] #随机参数类型
                                        if m == 0:
                                            method_content = method_content + ':(' + params_type + ')' + params_word
                                        else:
                                            method_content = method_content + " " + params_word + ':(' + params_type + ')' + params_word


                                    if return_type == 'void':
                                        params_word1 = random_1word()
                                        params_word2 = random_1word()
                                        method_some_things = '[NSString stringWithFormat:@"%s", @"%s" , @"%s"];' % ('%@%@', params_word1, params_word2)
                                        method_content = method_content + '\n{\n    %s \n}' % (method_some_things)

                                    elif return_type == 'NSString *':
                                        params_word1 = random_1word()
                                        params_word2 = random_1word()
                                        method_some_things = 'return [NSString stringWithFormat:@"%s", @"%s" , @"%s"];' % ('%@%@',params_word1, params_word2)
                                        method_content = method_content + '\n{\n    %s \n}' % (method_some_things)
                                    elif return_type == 'BOOL' or return_type == 'CGFloat' or return_type == 'NSUInteger':
                                        params_word1 = random.randint(1, 10000000)
                                        params_word2 = random.randint(0, 10000000)
                                        params_word3 = random.randint(0, 10000000)
                                        method_some_things = 'return %s * %s + %s ;' % (params_word1, params_word2, params_word3)
                                        method_content = method_content + '\n{\n    %s \n}' % (method_some_things)

                                    # method_content = method_content + '\n{\n    %s \n}' % (" ")

                                new_add_method_content = new_add_method_content + method_content
                            content = content + new_add_method_content + '\n' + line



                        else:
                            content = content + line
                    elif line.startswith('@interface') or line.startswith('@property'):#属性插入

                        isneed = random.randint(1, 20)
                        if 5 <= isneed <= 12:

                            property_a = property_type[random.randint(0, len(property_type)-1)]
                            aaa = random.randint(1, 2) #决定是双单词还是三个单词，为了防止与原属性重复，设置长一点
                            if aaa == 1:
                                afirst, bsecond = random_2word()
                                property_name = random_1word().lower() + afirst.capitalize() + bsecond.capitalize()
                            else:
                                afirst, bsecond = random_2word()
                                property_name = afirst.lower()+bsecond.capitalize()

                            property_content = property_a + property_name + ';'
                            content = content + line + property_content + '\n'

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

def modify_method_params(src_dir, exclude_dirs, exclude_files, var_exclude_bian):

    all_var_new = []
    if os.path.exists(src_dir):
        list_dirs = os.walk(src_dir)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store" or file_name in exclude_files:
                    continue

                if file_name.endswith('.m'):#
                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)

                    # 读取方法内容
                    f_obj = open(file_path, "r")
                    text_lines = f_obj.readlines()

                    method_content = ''
                    is_in_method = 0
                    for line in text_lines:
                        # print chardet.detect(line)
                        line = line.decode('utf-8')
                        # line = line.strip()
                        # 方法开始
                        if line.startswith('- (') or line.startswith('+ (') or line.startswith('-  (') or line.startswith('+  (') or line.startswith('-(') or line.startswith('+('):
                            is_in_method = 1
                            method_content = ''

                        if is_in_method == 1:
                            method_content = method_content + line

                        if is_in_method == 1 and line.startswith('}'): #方法结束
                            is_in_method = 0
                            print method_content

                            method_content_temp = method_content

                            params_arr = []
                            aresults = re.findall('\\*[ ]*\\w+\\b', method_content) #函数内定义的指针类型的变量
                            bresult = re.findall('\\* *\\w*\\)\\w+\\b ', method_content)  #函数参数指针类型的变量
                            if aresults:

                                for ax in aresults:
                                    axxx = ax.replace('*', '').strip()
                                    if '_Nullable' in axxx or axxx in var_exclude_bian:
                                        continue
                                    params_arr.append(axxx)

                            if bresult:

                                for ax in bresult:
                                    axxx = ax.replace(' ', '').strip()
                                    axxx = axxx.replace('*)', '')
                                    if '_Nullable' in axxx or axxx in var_exclude_bian:
                                        continue
                                    params_arr.append(axxx)

                            print params_arr
                            if params_arr:
                                new_param_temp = []
                                for a_param in params_arr: #更换参数

                                    if a_param in ['0','1','2','3']:
                                        continue

                                    a_param_a = a_param
                                    first_wm, sec_w = random_2word()
                                    new_param = 'mwGg' + first_wm.capitalize() + sec_w.capitalize()
                                    while new_param in new_param_temp:
                                        first_wm, sec_w = random_2word()
                                        new_param = 'mwGg' + first_wm.capitalize() + sec_w.capitalize()

                                    #把.xxx这种不能替换，可能是其他类的属性
                                    # method_content_temp = method_content_temp.replace('.' + a_param_a, 'AAAAAAA')
                                    # method_content_temp = method_content_temp.replace(a_param_a, new_param)
                                    # method_content_temp = method_content_temp.replace('AAAAAAA' , '.' + a_param_a)
                                    method_content_temp = re.sub('\.' + a_param_a + '\\b', ' _AAAAAAA_ ', method_content_temp)
                                    #同名方法名称剔除
                                    method_content_temp = re.sub('\\b' + a_param_a + ':', ' _BBBBBBB_ ',method_content_temp)


                                    method_content_temp = re.sub('\\b' + a_param_a + '\\b', new_param, method_content_temp)
                                    method_content_temp = re.sub(' _AAAAAAA_ ', '.' + a_param_a,  method_content_temp)

                                    method_content_temp = re.sub(' _BBBBBBB_ ',  a_param_a + ':', method_content_temp)

                                    new_param_temp.append(new_param)
                                    if not new_param in all_var_new:
                                        all_var_new.append(new_param)

                            file_data = file_data.replace(method_content, method_content_temp)
                            method_content = ''
                            method_content_temp = ''

                    wite_data_to_file(file_path, file_data)



        # wite_data_to_file(project_content_path, project_content)

    print "all_var_new: %s" % all_var_new


def modify_class_property(src_dir, exclude_dirs, exclude_files, var_exclude_bian):

    all_var_new = []
    if os.path.exists(src_dir):
        list_dirs = os.walk(src_dir)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store" or file_name in exclude_files:
                    continue

                if file_name.endswith('.m') or file_name.endswith('.h'):#
                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)

                    # 读取方法内容
                    f_obj = open(file_path, "r")
                    text_lines = f_obj.readlines()

                    method_content = ''
                    is_in_method = 0
                    for line in text_lines:
                        # print chardet.detect(line)
                        line = line.decode('utf-8')
                        # line = line.strip()
                        # 方法开始
                        if line.startswith('- (') or line.startswith('+ (') or line.startswith('-  (') or line.startswith('+  (') or line.startswith('-(') or line.startswith('+('):
                            is_in_method = 1
                            method_content = ''

                        if is_in_method == 1:
                            method_content = method_content + line

                        if is_in_method == 1 and line.startswith('}'): #方法结束
                            is_in_method = 0
                            print method_content

                            method_content_temp = method_content

                            params_arr = []
                            aresults = re.findall('\\*[ ]*\\w+\\b', method_content) #函数内定义的指针类型的变量
                            bresult = re.findall('\\* *\\w*\\)\\w+\\b ', method_content)  #函数参数指针类型的变量
                            if aresults:

                                for ax in aresults:
                                    axxx = ax.replace('*', '').strip()
                                    if '_Nullable' in axxx or axxx in var_exclude_bian:
                                        continue
                                    params_arr.append(axxx)

                            if bresult:

                                for ax in bresult:
                                    axxx = ax.replace(' ', '').strip()
                                    axxx = axxx.replace('*)', '')
                                    if '_Nullable' in axxx or axxx in var_exclude_bian:
                                        continue
                                    params_arr.append(axxx)

                            print params_arr
                            if params_arr:
                                new_param_temp = []
                                for a_param in params_arr: #更换参数

                                    if a_param in ['0','1','2','3']:
                                        continue

                                    a_param_a = a_param
                                    first_wm, sec_w = random_2word()
                                    new_param = 'mwGg' + first_wm.capitalize() + sec_w.capitalize()
                                    while new_param in new_param_temp:
                                        first_wm, sec_w = random_2word()
                                        new_param = 'mwGg' + first_wm.capitalize() + sec_w.capitalize()

                                    #把.xxx这种不能替换，可能是其他类的属性
                                    # method_content_temp = method_content_temp.replace('.' + a_param_a, 'AAAAAAA')
                                    # method_content_temp = method_content_temp.replace(a_param_a, new_param)
                                    # method_content_temp = method_content_temp.replace('AAAAAAA' , '.' + a_param_a)
                                    method_content_temp = re.sub('\.' + a_param_a + '\\b', ' _AAAAAAA_ ', method_content_temp)
                                    #同名方法名称剔除
                                    method_content_temp = re.sub('\\b' + a_param_a + ':', ' _BBBBBBB_ ',method_content_temp)


                                    method_content_temp = re.sub('\\b' + a_param_a + '\\b', new_param, method_content_temp)
                                    method_content_temp = re.sub(' _AAAAAAA_ ', '.' + a_param_a,  method_content_temp)

                                    method_content_temp = re.sub(' _BBBBBBB_ ',  a_param_a + ':', method_content_temp)

                                    new_param_temp.append(new_param)
                                    if not new_param in all_var_new:
                                        all_var_new.append(new_param)

                            file_data = file_data.replace(method_content, method_content_temp)
                            method_content = ''
                            method_content_temp = ''

                    wite_data_to_file(file_path, file_data)



        # wite_data_to_file(project_content_path, project_content)

    print "all_var_new: %s" % all_var_new


#找出方法名字，修改方法名
def modify_class_method(src_dir, exclude_dirs, exclude_files, exclude_method_name):

    mthod_arr = []
    if os.path.exists(src_dir):
        list_dirs = os.walk(src_dir)
        for root, dirs, files in list_dirs:

            has_exclude_dir = 0
            for exclude_dir in exclude_dirs:
                if root.endswith(exclude_dir):
                    has_exclude_dir = 1

            if has_exclude_dir == 1:
                continue

            for file_name in files:

                if file_name == ".DS_Store" or file_name in exclude_files:
                    continue

                if file_name.endswith('.m'):#
                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)

                    # 读取方法内容
                    f_obj = open(file_path, "r")
                    text_lines = f_obj.readlines()

                    method_content = ''

                    is_in_method = 0
                    for line in text_lines:
                        # print chardet.detect(line)
                        line = line.decode('utf-8')
                        # line = line.strip()

                        #//system_method为标致系统方法或者实现的系统方法，不可改(自己在代码中标记)
                        if '//system_method' in line:
                            continue

                        # 方法声明开始
                        if line.startswith('- (') or line.startswith('+ (') or line.startswith('-  (') or line.startswith('+  (') or line.startswith('-(') or line.startswith('+('):
                            is_in_method = 1
                            method_content = ''

                        if is_in_method == 1:
                            method_content = method_content + line

                        line_temp = line.strip()

                        if is_in_method == 1 and (line_temp.endswith('{') or line_temp.endswith('{\n')): #方法内容开始
                            is_in_method = 0
                            # print method_content
                            local_m_temp = []
                            method_content_temp = method_content
                            # print method_content_temp

                            aresults = re.findall('\\b\\w+\\b:', method_content) #函数名称
                            if aresults:

                                for method_name in aresults:
                                    method_name = method_name.strip()

                                    isShuzi = re.findall('^[0-9]', method_name) #是否数字开头
                                    if isShuzi:
                                        continue

                                    if '_Nullable' in method_name or method_name in exclude_method_name:
                                        continue

                                    local_m_temp.append(method_name)
                                    # if method_name not in mthod_name_arr:
                                    #     mthod_name_arr.append(method_name)


                            else: #无参数函数
                                method_content_1 = method_content.replace(' ','').replace('\n', '').replace('{','')
                                method_name = re.sub('^[-+]\\(.+\\)','', method_content_1) #去除前面的类型
                                method_name = re.sub('//.+', '', method_name) #去除注释
                                local_m_temp.append(method_name)
                                # if method_name not in mthod_name_arr:
                                #     mthod_name_arr.append(method_name)

                            mthod_arr.append(local_m_temp)
                            method_content = ''
                            print 'local_m_temp: %s filename: %s' % (local_m_temp, file_path)



        # wite_data_to_file(project_content_path, project_content)

    print "mthod_arr: %s" % mthod_arr


def modify_oc_class_method_in_header(header_path):
    file_path = header_path
    f_obj = open(file_path, "r")
    text_lines = f_obj.readlines()
    for line in text_lines:
        # print chardet.detect(line)
        line = line.decode('utf-8')


if __name__ == '__main__':

    # xcode_project_path = '/Users/ganyuanrong/iOSProject/game_mw_sdk_ios_v3/MW_OBS_V3/MW_SDK.xcodeproj'

    # oc_all_path = '/Users/ganyuanrong/iOSProject/game_mw_sdk_ios_v3/MW_OBS_V3/FLSDK'
    # oc_modify_path = '/Users/ganyuanrong/iOSProject/game_mw_sdk_ios_v3/MW_OBS_V3/FLSDK'


    xcode_project_path = '/Users/ganyuanrong/iOSProject/flsdk_ios/GamaSDK_iOS_Integration/MW_SDK.xcodeproj'
    oc_all_path = '/Users/ganyuanrong/iOSProject/flsdk_ios/GamaSDK_iOS_Integration/FLSDK'
    oc_modify_path = '/Users/ganyuanrong/iOSProject/flsdk_ios/GamaSDK_iOS_Integration/FLSDK'


    handle_file_count = 0
    file_count = 0

    oc_exclude_files.extend(['AppDelegate.h', 'MWSDK.h', 'PayData.h', 'LoginData.h', 'AccountModel.h', 'CreateOrderResp.h'])
    oc_exclude_dirs.extend(['AFNetworking', 'Masonry', 'YYModel', 'Model'])

    woords_file_path = '/Users/ganyuanrong/Desktop/sdk_confuse/confuse_words.log'

    f_obj = open(woords_file_path, "r")
    text_lines = f_obj.readlines()
    for line in text_lines:
        line = line.decode('utf-8')
        word = line.strip().replace(' ', '')
        if len(word) > 2:#太短的单词去掉
            genest_word.append(word)
    #1.修改图片  图片md5需要额外处理
    # image_exclude_files = []
    # image_ref_path = '/Users/ganyuanrong/iOSProject/game_mw_sdk_ios_v3/MW_OBS_V3'
    # modify_sdk_bundle_image_name("/Users/ganyuanrong/iOSProject/game_mw_sdk_ios_v3/MW_OBS_V3/Resources/GOT/SDKResourcesV2.bundle/", image_ref_path, image_exclude_files)

    #2.添加垃圾方法和属性 (打乱方法顺序)
    # exclude_dirs = ['AFNetworking', 'YYModel', 'Plat']
    # exclude_files = []
    # addNoUseMethodAndProperty(oc_all_path, exclude_dirs, exclude_files)

    #3.添加随机注释
    # addNewComments(oc_modify_path, '/Users/ganyuanrong/Desktop/sdk_confuse/ofc.log')

    # 4.修改类名
    # modify_oc_class_name(oc_modify_path)

    # 5.修改提取到header的方法宏定义
    # random_word_for_method()
    # modify_oc_class_method_in_header(oc_modify_path)


    #找出方法体,改变方法内定义的变量和方法参数  方法 需要 [-+]开头 结束行位'}'标志，因此结束行需要只有'}'并且无空格
    # var_exclude_dirs = ['AFNetworking', 'YYModel', 'Plat']
    # var_exclude_files = []
    # var_exclude_bian = [''] #参数忽略
    # modify_method_params('/Users/ganyuanrong/iOSProject/flsdk_ios/GamaSDK_iOS_Integration/FLSDK/login/view_v2/',var_exclude_dirs,var_exclude_files,var_exclude_bian)

    #修改属性

    # modify_method_params('/Users/ganyuanrong/iOSProject/flsdk_ios/GamaSDK_iOS_Integration/FLSDK/login/view_v2/',var_exclude_dirs,var_exclude_files,var_exclude_bian)


    #找出所有方法
    var_exclude_dirs = ['AFNetworking', 'YYModel', 'Plat']
    var_exclude_files = []
    var_exclude_name = ['dealloc','show','load','init','drawRect','initialize','encode','decode','length','share','setData','viewWillAppear','viewDidLoad']
    modify_class_method('/Users/ganyuanrong/iOSProject/flsdk_ios/GamaSDK_iOS_Integration/FLSDK/',var_exclude_dirs,var_exclude_files,var_exclude_name)
    pass