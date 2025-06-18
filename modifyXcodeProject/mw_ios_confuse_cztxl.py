#coding=utf-8
import glob
import imp
import shutil
import string
import sys
import uuid

import md5util
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

def words_reader(word_file_path):

    words = []
    f_obj = open(word_file_path, "r")
    text_lines = f_obj.readlines()
    for line in text_lines:
        line = line.decode('utf-8')
        word = line.strip().replace(' ', '')
        if len(word) > 1:  # 太短的单词去掉
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


def modify_oc_class_name(oc_path, xcode_project_path, oc_all_path, oc_exclude_dirs11, oc_exclude_files11, oc_exclude_dirs_ref_modify, oc_exclude_files_ref_modify):
    global file_count, handle_file_count, fia

    project_content_path = os.path.join(xcode_project_path, 'project.pbxproj')
    project_content = read_file_data(project_content_path)

    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        old_map_new_content = ''
        class_dic = {}
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store" or file_name.endswith(".swift") or 'main' in file_name:
                    continue

                file_count = file_count + 1

                exclude_dir_flag = 0
                for exclude_dir in oc_exclude_dirs11:
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
                    if header_file_name in oc_exclude_files11: #特殊排除
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

                        has_same_class = 0
                        if class_dic.has_key(file_name_no_extension):#已存在一样的类进行过修改
                            new_word = class_dic[file_name_no_extension]
                            has_same_class = 1

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

                        xib_path = os.path.join(root, file_name_no_extension + '.xib')
                        if os.path.exists(xib_path):
                            xib_path_new = os.path.join(root, new_word + '.xib')
                            os.rename(xib_path, xib_path_new)

                        if '+' in file_name:  # 分类
                            file_new_name_no_extension = fia[0] + "+" + new_word
                        else:
                            file_new_name_no_extension = new_word


                        modify_oc_class_reference(oc_all_path, file_name_no_extension, file_new_name_no_extension, oc_exclude_dirs_ref_modify, oc_exclude_files_ref_modify)

                        # 更改xproject文件中的.m
                        project_content = replace_xproject_data_reference(project_content, file_name, file_new_name)

                        # 更改xproject文件中的.h
                        project_content = replace_xproject_data_reference(project_content, header_file_name, header_file_new_name)

                        project_content = replace_xproject_data_reference(project_content, file_name_no_extension + '.xib',
                                                                          new_word + '.xib')

                        handle_file_count = handle_file_count + 1
                        print '处理完成' + file_name
                        # 保存映射关系
                        if has_same_class == 0:
                            class_dic[file_name_no_extension] = file_new_name_no_extension
                        # 记录映射关系
                        old_map_new_content = old_map_new_content + file_name_no_extension + ' -------> ' + file_new_name_no_extension + '\n'

        wite_data_to_file(project_content_path, project_content)
        print '修改完成 file_count:' + str(file_count) + "  handle_file_count:" + str(handle_file_count)
        class_change_log_path = os.path.splitext(xcode_project_path)[0] + 'class_change_%s.log' % datetime_util.get_current_time_2() #写更改类的日志
        old_map_new_content = '===class change start===\n' + old_map_new_content
        file_util.wite_data_to_file(class_change_log_path, old_map_new_content)


#oc_path 所有源文件，置于一个单独目录最好
def modify_oc_class_reference(oc_path, old_ref, new_ref, oc_exclude_dirs_ref_modify, oc_exclude_files_ref_modify):
    file_count = 0
    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                file_count = file_count + 1

                if file_name in oc_exclude_files_ref_modify:
                    continue

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


def replace_xproject_data_reference(xproject_data, old_file_name, new_file_name):
    return replace_data_by_word(xproject_data, old_file_name, new_file_name)


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



def replace_data_content(data, old_content, new_content):

    png_old_name_re = re.compile(old_content)

    new_data = re.sub(png_old_name_re, new_content, data)
    return new_data


def read_file_data(file_path):
    f_obj = open(file_path, mode="r")  # 首先先创建一个文件对象
    f_data = f_obj.read()  # 用read()方法读取文件内容
    f_obj.close()
    return f_data


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

                    file_data = oc_code_util.removeAnnotate(file_data)
                    wite_data_to_file(file_path, file_data)



method_return_type = ['void', 'NSString *', 'BOOL', 'CGFloat', 'NSUInteger']
method_params_type = ['NSString *', 'BOOL', 'CGFloat', 'NSUInteger']
jisuan_type = ['*', '/', '+', '-']

cpp_base_type = ['int', 'bool', 'void', 'int32_t', 'int64_t', 'double']

def changeStringHeaderValue(header_path):
    global f_obj, text_lines, line
    f_obj = open(header_path, "r")
    text_lines = f_obj.readlines()
    content = ''
    for line in text_lines:
        line = line.decode('utf-8')
        if 'wwwww_tag_wwwww' in line:
            str_result = re.findall('//@"(.+)"', line)  # @"[\\w.]+"
            if str_result:
                str_result_1 = str_result[0]
                # str_result_1 = str_result_1[4: len(str_result_1) - 1]
                aes_encrypt_result = pc.aes_encrypt_base64(str_result_1)
                defineVale = 'Decrypt_AllStringContent(@"%s")' % (aes_encrypt_result)

                if 'Decrypt_AllStringContent' in line:
                    line = re.sub('Decrypt_AllStringContent\\(@".+"\\)', defineVale, line)
                    if line.endswith('\n'):
                        line = line.replace('\n', '')
                    print line
                    content = content + line + '\n'
                else:
                    line = re.sub('  @".+?" ', "  " + defineVale + "     ", line)
                    if line.endswith('\n'):
                        line = line.replace('\n', '')
                    print line
                    content = content + line + '\n'
            else:
                content = content + line
        else:
            content = content + line
    file_util.wite_data_to_file_noencode(header_path, content)


def changeMethodHeaderValue(header_path):

    f_obj = open(header_path, "r")
    text_lines = f_obj.readlines()
    content = ''
    for line in text_lines:
        line = line.decode('utf-8')
        if '_MMMethodMMM' in line:
            str_result = re.findall(r'#define +\w+_MMMethodMMM ', line)  # @"[\\w.]+"
            if str_result:
                str_result_1 = str_result[0]
                method_name = str_result_1.replace('#define ', '').strip()
                w1_dong = word_util.random_word_dong()
                w1_name = word_util.random_word_name() + word_util.random_1word().capitalize()
                if method_name.startswith('initWith'):
                    method_rep = str_result_1 + "         " + 'initWith' + w1_dong.capitalize() + w1_name.capitalize()
                elif method_name.startswith('init'):
                    method_rep = str_result_1 + "         " + 'init' + w1_dong.capitalize() + w1_name.capitalize()
                else:
                    method_rep = str_result_1 + "         " + w1_dong.lower() + w1_name.capitalize()
                letter = string.letters[random.randint(0, len(string.letters) - 1)]
                method_rep = method_rep + letter
                print method_rep
                content = content + method_rep + '\n'
            else:
                content = content + line
        else:
            content = content + line
    if len(content) > 1:
        file_util.wite_data_to_file_noencode(header_path, content)


def changeImageNameForDefindHeader(bundle_path,header_path, is_encode_png):
    if os.path.exists(bundle_path):

        time_s = datetime_util.get_current_time_2()
        destination_bundle = bundle_path.replace('.bundle', time_s + '.bundle')
        shutil.copytree(bundle_path, destination_bundle)

        list_dirs = os.walk(destination_bundle)
        header_data = read_file_data(header_path)
        isChange = 0
        for root, dirs, files in list_dirs:
            for file_name in files:
                if file_name.endswith('.png') or file_name.endswith('.jpg'):

                    w1, w2 = random_2word()
                    image_name_new_no_extension = w1.lower() + '_' + w2.lower()

                    image_name_no_extension = os.path.splitext(file_name)[0]
                    file_extension = os.path.splitext(file_name)[1]

                    if is_encode_png:

                        image_name_new = image_name_new_no_extension + '.asset'
                        file_old_path = os.path.join(root, file_name)
                        file_new_path = os.path.join(root, image_name_new)

                        iamge_content = file_util.read_file_data(file_old_path)
                        aes_encrypt_result = pc.encrypt_for_data(iamge_content)
                        file_util.wite_data_to_file_noencode(file_new_path, aes_encrypt_result)

                        # 删除文件
                        os.remove(file_old_path)

                    else:
                        image_name_new = image_name_new_no_extension + file_extension
                        file_old_path = os.path.join(root, file_name)
                        file_new_path = os.path.join(root, image_name_new)
                        os.rename(file_old_path, file_new_path)

                    # @"mmplaygame_apple_signin"
                    image_str_old = "@\"%s\"" % image_name_no_extension
                    image_str_new = "@\"%s\"" % image_name_new_no_extension
                    masx = re.findall(r'%s' % image_str_old, header_data)
                    if masx is None:
                        print 'xxxxxxxx==== image not defind image_str_old = %s, image_str_new = %s' % (image_str_old, image_str_new)

                    header_data = header_data.replace(image_str_old, image_str_new)
                    isChange = 1


        if isChange == 1:
            wite_data_to_file(header_path, header_data)

        return destination_bundle

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


def change_pro_name_proheader(arc_path):
    # global list_dirs, root, dirs, files, file_name
    if os.path.exists(arc_path):
        # list_dirs = os.walk(arc_path)
        # src_data = read_file_data(arc_path)

        str_lines = file_util.read_file_data_for_line(arc_path)
        content = ''
        pre_pro = ''
        for str_line in str_lines:
            str_line = str_line.replace('\n','')
            result = re.findall(r'#define +(\w+_MMMPRO|\w+_PRIROPERTY|\w+_IMPLVAR) +(\w+)', str_line)
            if result:

                defind_name = result[0][0]
                defind_value = result[0][1]
                if pre_pro != '' and pre_pro.lower() in defind_name.lower():
                    pass
                else:
                    new_property = word_util.random_property()
                    #define  payStatusBlock_PRIROPERTY      officerature153Capitalate154
                    new_defind = '#define %s      %s' %(defind_name, new_property)  #str_line.replace(defind_value, new_property)
                    content = content + new_defind + '\n'
                    mdefind = '#define _%s      _%s' %(defind_name, new_property)
                    content = content + mdefind + '\n'
                    set_defind = '#define %s      %s' % ('set' + word_util.capitalize_first_char(defind_name), 'set' + word_util.capitalize_first_char(new_property))
                    content = content + set_defind + '\n'
                    get_defind = '#define %s      %s' %  ('get' + word_util.capitalize_first_char(defind_name), 'get' + word_util.capitalize_first_char(new_property))
                    content = content + get_defind + '\n'

                    pre_pro = defind_name

            else:
                content = content + str_line + '\n'
        file_util.wite_data_to_file_noencode(arc_path, content)



if __name__ == '__main__':


    # handle_file_count = 0
    # file_count = 0
    sdk_confuse_dir = '/Users/ganyuanrong/PycharmProjects/SdkTools/modifyXcodeProject/sdk_confuse/'
    # woords_file_path = sdk_confuse_dir + 'confuse_words_dy.log'
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

    cpp_code_temp_aar = []  # 读取cpp代码模版
    list_dirs = os.walk(sdk_confuse_dir + 'code_temples_cpp')
    for root, dirs, files in list_dirs:
        for file_name in files:
            if file_name == ".DS_Store":
                continue
            file_path = os.path.join(root, file_name)
            code_data = file_util.read_file_data_utf8(file_path)
            if code_data:
                cpp_code_temp_aar.append(code_data)

    for code_data in cpp_code_temp_aar:
        code_data = re.sub(r'\bbool\b', 'BOOL', code_data)
        oc_class_parser.code_temples.append(code_data)


    # des_key = "qK9kVwUX7PAWQ1kB"
    # des_iv = "kcWcrnYYHiayZANc"
    # sdk_verson = 'VN' #设置版本
    # need_sync_source = 1    #是否同步源码，复制
    # is_obs_jiekou = 0 #是否混淆对外接口, 0不混淆，1混淆

    xcode_project_path = "/Users/ganyuanrong/cpGames/slg_xm_cocosNative/slgGame.xcodeproj"
    project_obs_src_path = "/Users/ganyuanrong/cpGames/slg_xm_cocosNative/ios"
    project_all_src_path = "/Users/ganyuanrong/cpGames/slg_xm_cocosNative/ios"
    project_dir_path = "/Users/ganyuanrong/cpGames/slg_xm_cocosNative/ios"
    # res_bundle_path = "/Users/ganyuanrong/iOSProject/flsdk_ios_p_majia/GamaSDK_iOS_Integration/Resources/TH/SDKResourcesTH.bundle"
    # res_bundle_path = "/Users/ganyuanrong/iOSProject/flsdk_ios_p_majia/GamaSDK_iOS_Integration/Resources/%s/SDKResources%s.bundle"
    # res_bundle_path = res_bundle_path % (sdk_verson, sdk_verson)



    # 4. ======删除注释
    var_exclude_dirs = ['AFNetworking', 'YYModel', 'ThirdSrc','ThirdResources']
    var_exclude_files = []
    deleteComments(project_obs_src_path, var_exclude_dirs, var_exclude_files)


    # oc_class_parser.parse('/Users/ganyuanrong/Desktop/AdDelegate.m')
    #6.添加垃圾代码
    var_exclude_dirs = ['AFNetworking', 'YYModel', 'ThirdSrc', 'ThirdResources']
    var_exclude_files = []
    # src_path = '/Users/ganyuanrong/Downloads/mwsdk_ios_vn_v4/GamaSDK_iOS_Integration/FLSDK'

    add_code(project_obs_src_path, var_exclude_dirs, var_exclude_files)


    # 7.修改类名
    oc_exclude_dirs = []
    oc_exclude_dirs.extend(['/AFNetworking', '/Masonry', '/YYModel', '/sdkFrameworks', "/Resources", '/ThirkLib', '/ThirdSrc'])

    oc_exclude_files.extend(
        ['AppDelegate.h', 'UnityAppController.h', 'UnityAppController+Rendering.h'
            , 'UnityViewControllerBase+iOS.h', 'UnityViewControllerBase+tvOS.h', 'UnityViewControllerBase.h',
         'UnityView.h', 'UnityView+iOS.h', 'UnityView+tvOS.h'])
    oc_exclude_dirs.extend(['/ThirdResources', '/PulicHeader'])
    oc_exclude_dirs_ref_modify = ['/ThirkLib', "/YYModel", "/AFNetworking", "/Resources", '/ThirdSrc', '/archives', '/build']


    oc_exclude_files_ref_modify = ['MWStringHeaders.h', 'codeObfuscationForMethodName.h']
    modify_oc_class_name(project_obs_src_path, xcode_project_path, project_all_src_path, oc_exclude_dirs, oc_exclude_files,
                         oc_exclude_dirs_ref_modify, oc_exclude_files_ref_modify)

    print 'end'
