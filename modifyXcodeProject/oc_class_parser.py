#coding=utf-8
import imp
import sys

# from modifyXcodeProject import mw_ios_confuse
from modifyXcodeProject import oc_method_util
from modifyXcodeProject.model import PropertyInfo
from modifyXcodeProject.model.MethodInfo import MethodInfo
from modifyXcodeProject.utils import file_util, word_util

imp.reload(sys)
sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的

import os
import re

import chardet

# 导入 random(随机数) 模块
import random

code_temples = []
code_if_temples = []

params_not_use_list = ['rect', 'alertController'] #排除使用作为条件判断的参数

#找出方法名字，修改方法名
def parse(file_name):

    mthod_arr = []
    mthod_arr2 = []
    mMethodInfo_list = []
    if os.path.exists(file_name) and (file_name.endswith('.m') or file_name.endswith('.mm') or file_name.endswith('.h')):

        if file_name.endswith('.m'):  #
            file_path = file_name
            # print 'handle file = ' + file_path
            print '正在处理: ' + file_name
            file_data = file_util.read_file_data(file_path)
            # property_list = parse_property(file_data)
            # 读取方法内容

            text_lines = file_util.read_file_data_for_line(file_path)

            method_content = ''
            method_defind_content = ''

            is_in_method = 0
            for line in text_lines:
                # print chardet.detect(line)
                line = line.decode('utf-8')
                # line = line.strip()

                # //system_method为标致系统方法或者实现的系统方法，不可改(自己在代码中标记)
                # if '//system_method' in line:
                #     continue

                # 方法声明开始
                if line.startswith('- (') or line.startswith('+ (') or line.startswith('-  (') or line.startswith(
                        '+  (') or line.startswith('-(') or line.startswith('+('):
                    is_in_method = 1
                    is_in_method_def_line = 1
                    method_content = ''
                    method_defind_content = ''

                if is_in_method == 1:
                    method_content = method_content + line

                    if is_in_method_def_line == 1:
                        method_defind_content = method_defind_content + line

                    line_temp = line.strip()
                    if line_temp.endswith('{') or line_temp.endswith('{\n'):  # 方法内容开始 方法声明结束

                        is_in_method_def_line = 0

                    if line.startswith('}') or line.startswith('}\n'):#函数end
                        is_in_method = 0
                        print '正则处理方法: ' + method_defind_content
                        # print method_content
                        method_content_temp = method_content

                        method_defind_params_list = parse_method_defind_params(method_defind_content)
                        local_params_list = parse_method_local_params(method_content)
                        code_method_temp_file = '/Users/ganyuanrong/Desktop/sdk_confuse/temp/code_method_temp.log'
                        file_util.wite_data_to_file(code_method_temp_file, method_content)
                        code_method_temp_lines = file_util.read_file_data_for_line(code_method_temp_file)
                        code_method_temp_content = ''

                        local_params_appear_list = []  #改行出现过本地变量，因为出现过才能使用其作为条件判断
                        code_line_pre = '' #前一行代码
                        can_insert_code = 1
                        if_exp_apper = 0
                        if_exp_after_count = 0

                        for code_line in code_method_temp_lines:

                            code_line_1_temp = removeAnnotate(code_line)
                            code_line_1_temp = code_line_1_temp.strip()
                            code_line_pre_1_tmp = code_line_pre.strip()

                            if local_params_list and ('\\' not in code_line):
                                for local_p in local_params_list:
                                    if local_p in local_params_appear_list:
                                        continue

                                    if (' ' + local_p + '=') in code_line \
                                            or (' ' + local_p + ' =') in code_line \
                                            or (' *' + local_p + '=') in code_line \
                                            or (' *' + local_p + ' =') in code_line \
                                            or (' * ' + local_p + '=') in code_line \
                                            or (' * ' + local_p + ' =') in code_line:
                                        local_params_appear_list.append(local_p)

                            #if语句后面无{}的时候不可插入code
                            if code_line_1_temp.startswith('if') and (not code_line_1_temp.endswith('{')):
                                can_insert_code = 0
                                if_exp_apper = 1
                                if_exp_after_count = 0

                            if if_exp_apper == 1 and code_line_1_temp.startswith('{'):
                                can_insert_code = 1
                                if_exp_apper = 0
                                if_exp_after_count = 0

                            if if_exp_apper == 1 and code_line_1_temp.endswith(';') and not code_line_1_temp.startswith('//'):
                                if_exp_after_count = if_exp_after_count + 1
                                if if_exp_after_count > 2:
                                    can_insert_code = 1
                                    if_exp_apper = 0
                                    if_exp_after_count = 0

                            if (code_line.endswith(';') or code_line.endswith(';\n')) \
                                    and (can_insert_code == 1) \
                                    and ('return' not in code_line) \
                                    and ('continue' not in code_line) \
                                    and ('break' not in code_line)\
                                    and ('\\' not in code_line):

                                is_insert_nouse_code = random.randint(0, 10)
                                if is_insert_nouse_code > 9:  # 该逗号是否插入代码

                                    code_params_type = random.randint(0, 3)
                                    if code_params_type == 0:  #函数声明参数设置条件
                                        if method_defind_params_list:

                                            method_param_insert = method_defind_params_list[random.randint(0, len(method_defind_params_list)-1)] #随机抽出一个参数
                                            print '使用函数声明变量为条件判断插入code params:' + method_param_insert
                                            code_temple = handle_code_temples(method_param_insert)

                                            code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple, code_line)
                                        else:
                                            code_temple = insert_no_param_code()
                                            code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple, code_line)

                                    elif code_params_type == 1: #本地参数设置条件
                                        if local_params_appear_list: #出现过的本地变量参数
                                            method_param_insert = local_params_appear_list[random.randint(0, len(local_params_appear_list) - 1)]  # 随机抽出一个参数
                                            code_temple = handle_code_temples(method_param_insert)
                                            print '使用本地变量为条件判断插入code params:' + method_param_insert
                                            code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple,code_line)

                                        else:
                                            code_temple = insert_no_param_code()
                                            code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple,code_line)
                                    else:

                                        code_temple = insert_no_param_code()

                                        code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple,code_line)
                                else:
                                    # 不添加
                                    code_method_temp_content = code_method_temp_content + code_line

                            elif ((code_line.strip().startswith('return')) \
                                    or (code_line.strip().startswith('continue')) \
                                    or (code_line.strip().startswith('while')) \
                                    or (code_line.strip().startswith('if')) \
                                    or (code_line.strip().startswith('for'))) \
                                    and (can_insert_code == 1):
                                is_insert_nouse_code = random.randint(0, 10)
                                if is_insert_nouse_code < 3:  # 是否在return等前一行插入代码

                                    code_params_type = random.randint(0, 3)
                                    if code_params_type == 0:
                                        if method_defind_params_list:

                                            method_param_insert = method_defind_params_list[
                                                random.randint(0, len(method_defind_params_list) - 1)]  # 随机抽出一个参数
                                            print '使用函数声明变量为条件判断插入code params:' + method_param_insert
                                            code_temple = handle_code_temples(method_param_insert)

                                            code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple, code_line, True)
                                        else:
                                            code_temple = insert_no_param_code()
                                            code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple, code_line, True)

                                    elif code_params_type == 1:
                                        if local_params_appear_list:
                                            method_param_insert = local_params_appear_list[random.randint(0, len(local_params_appear_list) - 1)]  # 随机抽出一个参数
                                            code_temple = handle_code_temples(method_param_insert)
                                            print '使用本地变量为条件判断插入code params:' + method_param_insert
                                            code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple, code_line, True)

                                        else:
                                            code_temple = insert_no_param_code()
                                            code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple, code_line, True)
                                    else:

                                        code_temple = insert_no_param_code()

                                        code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple, code_line, True)
                                else:
                                    #不添加
                                    code_method_temp_content = code_method_temp_content + code_line

                            else:
                                # 不添加
                                code_method_temp_content = code_method_temp_content + code_line

                        file_data = file_data.replace(method_content, code_method_temp_content)
                        file_util.wite_data_to_file(file_name, file_data)

                        # params_list = parse_method_local_params(method_content)
                        # if params_list:
                        #     print params_list
                        #     print '\n'


def addCodeToSrcCode(code_method_temp_content, code_temple, code_line, is_later=False):
    if is_later:
        print '前面插入：' + code_line
        code_method_temp_content = code_method_temp_content + '\n\t\t//====insert my code start===\n\t\t{\n\t\t' + code_temple + '\n\t\t}\n\t\t//====insert my code end===\n\n' + code_line
    else:
        print '后面插入'  + code_line
        code_method_temp_content = code_method_temp_content + code_line
        code_method_temp_content = code_method_temp_content + '\n\t\t//====insert my code start===\n\t\t{\n\t\t' + code_temple + '\n\t\t}\n\t\t//====insert my code end===\n\n'
    return code_method_temp_content


def insert_no_param_code():
    print '自动生成条件判断插入code'
    #条件表达式替换start
    condition_var = handle_code_temple_condition()  #条件变量

    # 条件表达式替换end

    code_temple = handle_code_temples(condition_var)

    # 替换代码模版中的内容end
    return code_temple


#处理条件表达式模版
def handle_code_temple_condition():
    word_aar = []
    method_param_insert_code = code_if_temples[random.randint(0, len(code_if_temples) - 1)] #随机抽出一个条件模版
    method_param_insert_code_str_list = re.findall(r'ppppp\w+_ppppp', method_param_insert_code)
    for ab in method_param_insert_code_str_list:
        w1, w2 = word_util.random_2words_not_same_inarr(word_aar)
        method_param_insert_code = method_param_insert_code.replace(ab, w1 + w1.capitalize())
    method_param_insert_code_num_list = re.findall(r'iiiii\w+_iiiii', method_param_insert_code)
    for ab in method_param_insert_code_num_list:
        numbera = random.randint(1, 10000)
        method_param_insert_code = method_param_insert_code.replace(ab, str(numbera))

    code_int_temple_params_list = re.findall(r'int\w+_int', method_param_insert_code)  # int\w+_int需要时正整数
    for code_int_temple_param in code_int_temple_params_list:
        int_value = random.randint(1, 10000)
        method_param_insert_code = method_param_insert_code.replace(code_int_temple_param, str(int_value))

    return method_param_insert_code


#代码模版处理
def handle_code_temples(condition_var):
    word_aar = []

    code_temple = code_temples[random.randint(0, len(code_temples) - 1)]  # 随机抽出一个代码模版

    # 替换代码模版中的内容start
    code_temple = code_temple.replace('var_temp', condition_var)  # 添加表达式替换代码模版占位符


    code_temple_params_list = re.findall(r'ppppp\w+_ppppp', code_temple)  # ppppp\w+_ppppp代表字符
    for code_temple_param in code_temple_params_list:
        w1, w2 = word_util.random_2words_not_same_inarr(word_aar)
        code_temple = code_temple.replace(code_temple_param, w1 + w2.capitalize())


    code_mumber_temple_params_list = re.findall(r'iiiii\w+_iiiii', code_temple)  # iiiii\w+_iiiii的范围可以是负数
    for code_mumber_temple_params in code_mumber_temple_params_list:
        numbera = (random.random() + 1) * random.randint(-1000, 10000)
        code_temple = code_temple.replace(code_mumber_temple_params, str(numbera))

    code_int_temple_params_list = re.findall(r'int\w+_int', code_temple)  # int\w+_int需要时正整数
    for code_int_temple_param in code_int_temple_params_list:
        int_value = random.randint(1, 10000)
        code_temple = code_temple.replace(code_int_temple_param, str(int_value))
    if 'case_content_case' in code_temple:
        w1, w2 = word_util.random_2words_not_same_inarr(word_aar)
        case_left_var = w1 + w2.capitalize()
        w1, w2 = word_util.random_2words_not_same_inarr(word_aar)
        case_right_var = w1
        code_temple = code_temple.replace('case_left_var', case_left_var)
        code_temple = code_temple.replace('case_right_var', case_right_var)
        case_temp_content = oc_method_util.create_case_expression(case_left_var, case_right_var)
        code_temple = code_temple.replace('case_content_case', case_temp_content)

    if 'dic_value_dic' in code_temple:
        dic_count = random.randint(1, 15)
        dic_content = ''
        for i in range(dic_count):
            w1, w2 = word_util.random_2words_not_same_inarr(word_aar)
            if i == dic_count - 1:
                val1 = '@"' + w1 + '" : @"' + w2 + '" '
            else:
                val1 = '@"' + w1 + '" : @"' + w2 + '", '
            dic_content = dic_content + val1
        code_temple = code_temple.replace('dic_value_dic', dic_content)

    if 'array_value_array' in code_temple:
        arr_count = random.randint(1, 15)
        arr_content = ''
        for i in range(arr_count):
            w1, w2 = word_util.random_2words_not_same_inarr(word_aar)
            if i == arr_count - 1:
                val1 = '@"' + w1 + '_' + w2 + '" '
            else:
                val1 = '@"' + w1 + '_' + w2 + '", '
            arr_content = arr_content + val1
        code_temple = code_temple.replace('array_value_array', arr_content)

    return code_temple


def parse_property(file_data):
    if file_data:
        property_result_list = re.findall(r'@property .+;', file_data) #正则匹配出所有属性
        if property_result_list:
            property_list = []
            for property_def in property_result_list:
                property_name = re.findall(r' \\*?\\w+;', property_def)
                if property_name:
                    mPropertyInfo = PropertyInfo
                    property_name = property_name.replace(' ','').replace('*','').replace(';','')
                    mPropertyInfo.propertyName = property_name
                    property_list.append(mPropertyInfo)

            return property_list
    return None

# '\w+ \*\w+ ?='
def parse_method_local_params(method_data): #解析方法局部变量
    if method_data:
        method_data_temp = method_data
        method_data_temp = removeAnnotate(method_data_temp)

        result_list = re.findall(r' \w+ (\*|\* )?\w+ ?=', method_data_temp) #提取类似 NSString * timeStamp=   NSArray *responseArray =
        if result_list:
            params_list = []
            for param_content_temp in result_list:
                param_content_temp_list = re.findall(r' \*?\w+ ?=', param_content_temp)
                if param_content_temp_list:
                    param_name = param_content_temp_list[0]
                    param_name = param_name.replace('*', '').replace('=', '').replace(' ', '')
                    if param_name not in params_list and param_name not in params_not_use_list:
                        params_list.append(param_name)
            return params_list

    return None

#删除注释
def removeAnnotate(method_data_temp):
    # file_data_0 = replace_data_content(src_data, '/\\*\\*/', '')
    # file_data_1 = replace_data_content(file_data_0, '([^:/])//.*', '\\1')
    # file_data_2 = replace_data_content(file_data_1, '^//.*', '')
    # file_data_3 = replace_data_content(file_data_2, '/\\*{1,2}[\\s\\S]*?\\*/', '')
    # 先删掉注释，不然会拿到注释的变量
    # method_data_temp = re.sub(r'^//.*', '', method_data_temp)
    method_data_temp = re.sub(r'//[\s\S]*?\n', '\n', method_data_temp)
    # method_data_temp = re.sub(r'^ *//.*', '', method_data_temp)  #//[\s\S]*?\n
    method_data_temp = re.sub(r'/\*{1,2}[\s\S]*?\*/', '', method_data_temp)  # 非贪婪模式
    return method_data_temp


def parse_method_defind_params(method_data): #解析方法前面变量

    if method_data:
        result_list = re.findall(r': *\(\w+ ?\*? ?\) ?\w+', method_data) #提取类似 -(NSString *)cancelFailedEventsSky:(NSString *)touchesApple managerDecrypt:(NSInteger)managerDecrypt
        if result_list:
            params_list = []
            for param_content_temp in result_list:
                param_content_temp_list = re.findall(r'\) ?\w+', param_content_temp)
                if param_content_temp_list:
                    param_name = param_content_temp_list[0]
                    param_name = param_name.replace('*', '').replace(')', '').replace(' ', '')
                    if param_name not in params_list and param_name not in params_not_use_list:
                        params_list.append(param_name)
            return params_list

    return None
