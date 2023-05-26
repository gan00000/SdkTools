#coding=utf-8
import imp
import sys
import uuid

from modifyXcodeProject import oc_class_parser, oc_method_util, cpp_code_util
from modifyXcodeProject.utils import file_util, word_util, datetime_util
from modifyXcodeProject.utils.PrpCrypt import PrpCrypt

imp.reload(sys)
sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的

import os
import re

import chardet

# 导入 random(随机数) 模块
import random

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
                    print '正在处理=' + file_name
                    file_path = os.path.join(root, file_name)
                    file_data = file_util.read_file_data(file_path)

                    # file_data_0 = replace_data_content(file_data,'/\\*\\*/', '')
                    # file_data_1 = replace_data_content(file_data_0,'([^:/])//.*', '\\1')
                    # file_data_2 = replace_data_content(file_data_1,'^//.*', '')
                    # file_data_3 = replace_data_content(file_data_2,'/\\*{1,2}[\\s\\S]*?\\*/', '')
                    # file_data_4 = replace_data_content(file_data_3,'\\s*\\n', '\\n')

                    # file_data_0 = re.sub(r'//[\s\S]*?\n', '\n', file_data)
                    # # method_data_temp = re.sub(r'^ *//.*', '', method_data_temp)  #//[\s\S]*?\n
                    # file_data_1 = re.sub(r'/\*{1,2}[\s\S]*?\*/', '', file_data_0)  # 非贪婪模式

                    file_data_1 = cpp_code_util.removeAnnotate(file_data)

                    file_util.wite_data_to_file(file_path, file_data_1)


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

                file_util.wite_data_to_file(file_path, content)

# def addNoUseMethodForCpp(src_dir_path, exclude_dirs, exclude_files):
#     if not os.path.exists(src_dir_path):
#         print("src_dir_path not exist")
#         return
#     cppReturnType = ['int32_t','int64_t']
#     list_dirs = os.walk(src_dir_path)
#     for root, dirs, files in list_dirs:
#
#         exclude_dir_flag = 0
#         for exclude_dir in exclude_dirs:
#             if exclude_dir in root:
#                 exclude_dir_flag = 1
#         if exclude_dir_flag == 1:
#             continue
#
#         for file_name in files:
#             if file_name == ".DS_Store":
#                 continue
#
#             if file_name in exclude_files:
#                 continue
#             # if 'AFNetworking' in root or 'YYModel' in root:
#             #     continue
#
#             if file_name.endswith('.cpp'):
#                 file_path = os.path.join(root, file_name)
#
#                 f_obj = open(file_path, "r")
#                 text_lines = f_obj.readlines()
#
#                 content = ''
#                 has_implementation = 0
#                 print '处理中  ' + file_name
#                 for line in text_lines:
#                     # print chardet.detect(line)
#                     line = line.decode('utf-8')
#                     line_strip = line.strip()
#                     if line_strip.startswith('static inline'): #方法插入位置
#
#                         isneed = random.randint(1, 20) #随机决定是否改行需要添加无用方法
#                         if 4 <= isneed <= 6:#添加
#
#                             method_count = random.randint(1, 2) #随机产生插入的方法数量
#                             new_add_method_content = ''
#                             for i in range(method_count):
#
#                                 return_type = cppReturnType[random.randint(0, len(cppReturnType)-1)] #随机方法返回类型
#                                 noUserMethod_name = random_word_for_no_use_method_for_cpp()
#
#                                 method_content = '\n' + '   static inline ' + return_type + ' mwdk_' + noUserMethod_name + '() {\n'
#
#                                 params_counts = random.randint(0, 5) #随机参数个数,最大5个
#                                 eee = str(random.randint(2,999999))
#                                 qqq = str(random.randint(880, 999990))
#                                 # dd = 'return static_cast<%s> (floor(%s) * %s);\n }\n' % (return_type, eee, qqq)
#                                 if params_counts == 0:
#                                     method_content = method_content + '     return static_cast<%s> (floor(%s) * %s);\n  }\n' % (return_type, eee, qqq)
#
#                                 elif params_counts == 1:
#                                     method_content = method_content + '     return static_cast<%s> (abs(%s) - %s);\n    }\n' % (return_type, eee, qqq)
#
#                                 elif params_counts == 2:
#                                     method_content = method_content + '     return static_cast<%s> (%s - %s);\n     }\n' % (return_type, eee, qqq)
#
#                                 elif params_counts == 3:
#                                     method_content = method_content + '     return static_cast<%s> (%s + %s);\n     }\n' % (return_type, eee, qqq)
#                                 elif params_counts == 4:
#                                     method_content = method_content + '     return static_cast<%s> (ceil(%s) + %s);\n   }\n' % (return_type, eee, qqq)
#
#                                 elif params_counts == 5:
#                                     method_content = method_content + '     return static_cast<%s> (exp(%s) + %s);\n    }\n' % (return_type, eee, qqq)
#
#                                 new_add_method_content = new_add_method_content + method_content
#                             content = content + new_add_method_content + '\n' + line
#
#
#
#                         else:
#                             content = content + line
#                     else:
#                         content = content + line
#
#                 wite_data_to_file(file_path, content)
#

def changeClassForCpp(src_root, src_change_path, exclude_dirs, exclude_files):
    if not os.path.exists(src_change_path):
        print("src_dir_path not exist")
        return

    class_arr = []
    list_dirs = os.walk(src_change_path)
    for root, dirs, files in list_dirs:

        for file_name in files:
            if file_name == ".DS_Store":
                continue

            if file_name in exclude_files:
                continue
            if file_name.endswith('.cpp'):
                file_path = os.path.join(root, file_name)

                f_data = file_util.read_file_data_utf8(file_path)
                class_c_list = re.findall(r'(?=\w+::~\w+\()\w+', f_data)
                for i_class in class_c_list:
                    if i_class not in class_arr :
                        class_arr.append(i_class)
                        print i_class
    list_dirs = os.walk(src_change_path)
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
            print '文件处理中=' + file_name
            if file_name in exclude_files:
                continue
            if file_name.endswith('.cpp') or file_name.endswith('.hpp') or file_name.endswith('.h'):
                file_path = os.path.join(root, file_name)

                f_data = file_util.read_file_data_utf8(file_path)
                for class_a in class_arr:
                    f_data = re.sub(r'\b%s\b' % class_a, class_a + 'MWan', f_data)
                    print class_a + '->' + class_a + 'MWan'

                file_util.wite_data_to_file(file_path, f_data)

    list_dirs = os.walk(src_root)
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

            if file_name.endswith('.cpp') or file_name.endswith('.hpp') or file_name.endswith('.h'):
                print '文件处理中=' + file_name
                file_path = os.path.join(root, file_name)

                f_data = file_util.read_file_data_utf8(file_path)
                # f_data = cpp_code_util.removeAnnotate(f_data)

                for class_a in class_arr:
                    f_data = re.sub(r'::\b%s\b' % class_a, '::' + class_a + 'MWan', f_data)
                    f_data = re.sub(r'\b%s\b\*' % class_a, class_a + 'MWan*', f_data)
                    print '::%s' % class_a + '->' + '::' + class_a + 'MWan'

                file_util.wite_data_to_file(file_path, f_data)

if __name__ == '__main__':

    sdk_confuse_dir = '/Users/ganyuanrong/PycharmProjects/SdkTools/modifyXcodeProject/sdk_confuse/'
    woords_file_path = sdk_confuse_dir + 'confuse_words_2.log'
    genest_word = word_util.words_reader(woords_file_path)

    words_dong = word_util.words_reader(sdk_confuse_dir + 'word_dong.log')
    words_name = word_util.words_reader(sdk_confuse_dir + 'word_ming.log')
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
        oc_class_parser.code_temples.append(code_data)


    # 处理cpp

    # var_exclude_dirs = []
    # var_exclude_files = []
    # # src_path = '/Users/ganyuanrong/iOSProject/flsdk_ios/GamaSDK_iOS_Integration/FLSDK/'
    # # src_path = '/Users/ganyuanrong/Downloads/seashhx/dongnyProject/'
    # src_path = '/Users/ganyuanrong/Downloads/seashhx/main'
    # deleteComments(src_path, var_exclude_dirs, var_exclude_files)

    #cpp添加代码
    # var_exclude_dirs = []
    # var_exclude_files = []
    # # src_path = '/Users/ganyuanrong/Downloads/seashhx/dongnyProject/'
    # src_path = '/Users/ganyuanrong/Downloads/seashhx/tools/libfairygui/Classes'
    # addNoUseMethodForCpp2(src_path,var_exclude_dirs,var_exclude_files)

    #修改类名
    var_exclude_dirs = ['cocos2d','libsimulator','MWSDK','ThirdSDK']
    var_exclude_files = []
    # src_path = '/Users/ganyuanrong/Downloads/seashhx/dongnyProject/'
    src_path = '/Users/ganyuanrong/Downloads/seashhx/tools/libfairygui/Classes'
    src_root = '/Users/ganyuanrong/Downloads/seashhx'
    changeClassForCpp(src_root,src_path,var_exclude_dirs,var_exclude_files)


    print 'end'
