#coding=utf-8
import imp
import string
import sys

# from modifyXcodeProject import mw_ios_confuse
from modifyXcodeProject import oc_method_util
from modifyXcodeProject.model.PropertyInfo import PropertyInfo
from modifyXcodeProject.utils import file_util, word_util, datetime_util

imp.reload(sys)
sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的

import os
import re

import chardet

# 导入 random(随机数) 模块
import random

code_temples = []
code_if_temples = []

params_not_use_list = ['rect', 'alertController', 'i'] #排除使用作为条件判断的参数
insert_code_sum = 0

#找出方法名字，修改方法名
def parse(file_name, sdk_confuse_dir): #.m文件

    mthod_arr = []
    mthod_arr2 = []

    if os.path.exists(file_name) and (file_name.endswith('.m') or file_name.endswith('.mm') or file_name.endswith('.h')):

        if file_name.endswith('.m'):  #
            file_path = file_name
            # print 'handle file = ' + file_path
            print '正在处理: ' + file_name

            property_list_add = insert_class_property(file_path)

            methods_list = insert_methods(file_path, sdk_confuse_dir)

            insert_method_extra_code(file_path, methods_list, property_list_add)

    print '一共插入的代码数量为：' + str(insert_code_sum)

def insert_class_property(file_path_m):
    word_aar = []
    insert_property_list = []
    file_path_h = file_path_m.replace('.m', '.h')
    file_data_h = file_util.read_file_data(file_path_h)
    if file_data_h:
        interface_content_list = re.findall(r'@interface[\s\S]*@end', file_data_h)
        if interface_content_list:
            property_tag_list = re.findall(r'@property.+ \*?\w+;', interface_content_list[0])
            if property_tag_list: #存在属性
                for property_tag_content in property_tag_list:
                    add_property = random.randint(1, 2)  # 随机需要增加属性
                    if add_property == 1: #增加
                        property_tag_content_add = property_tag_content
                        add_property_count = random.randint(1, 3)  # 随机需要增加属性的数量
                        for i in range(add_property_count):
                            pi = PropertyInfo()
                            add_property_type = oc_method_util.method_param_type_list[random.randint(0, len(oc_method_util.method_param_type_list) - 1)]
                            w1, w2 = word_util.random_2words_not_same_inarr(word_aar)
                            propertyName = w1.lower() + w2.capitalize()
                            if '*' in add_property_type:
                                add_property_content = '@property (nonatomic, strong) %s%s;//===insert my property===' %(add_property_type, propertyName)
                            else:
                                add_property_content = '@property (nonatomic, assign) %s %s;//===insert my property===' % (add_property_type, propertyName)
                            pi.propertyName = propertyName
                            pi.propertyType = add_property_type
                            insert_property_list.append(pi)
                            property_tag_content_add = property_tag_content_add + '\n' + add_property_content + '\n'

                        file_data_h = file_data_h.replace(property_tag_content, property_tag_content_add)
                file_util.wite_data_to_file(file_path_h, file_data_h)
    return insert_property_list

def insert_method_extra_code(file_path, methods_list, property_list): #方法内插入垃圾代码
    file_data = file_util.read_file_data(file_path)
    # property_list = parse_property(file_data)
    # 读取方法内容
    text_lines = file_util.read_file_data_for_line(file_path)
    method_content = ''
    method_defind_content = ''
    is_in_method = 0
    method_assess = ''
    for line in text_lines:
        # print chardet.detect(line)
        line = line.decode('utf-8')
        # line = line.strip()

        # //system_method为标致系统方法或者实现的系统方法，不可改(自己在代码中标记)
        # if '//system_method' in line:
        #     continue

        # 方法声明开始
        if (line.startswith('- (') or line.startswith('+ (') or line.startswith('-  (') or line.startswith(
                '+  (') or line.startswith('-(') or line.startswith('+(')) and '//insert method' not in line:
            is_in_method = 1
            is_in_method_def_line = 1
            method_content = ''
            method_defind_content = ''
            method_assess = ''
            line_temp = line.strip()
            if line_temp.startswith('-'):  # 方法内容开始 方法声明结束
                method_assess = '-'
            else:
                method_assess = '+'

        if is_in_method == 1:
            method_content = method_content + line

            if is_in_method_def_line == 1:
                method_defind_content = method_defind_content + line

            line_temp = line.strip()
            if line_temp.endswith('{') or line_temp.endswith('{\n'):  # 方法内容开始 方法声明结束
                is_in_method_def_line = 0

            if line.startswith('}') or line.startswith('}\n'):  # 函数end
                is_in_method = 0
                print '正则处理方法: ' + method_defind_content
                # print method_content
                method_content_temp = method_content

                method_defind_params_list = parse_method_defind_params(method_defind_content)
                local_params_list = parse_method_local_params(method_content)
                code_method_temp_file = '/Users/ganyuanrong/PycharmProjects/SdkTools/modifyXcodeProject/sdk_confuse/temp/code_method_temp.log'  # 把方法内容写到临时文件
                file_util.wite_data_to_file(code_method_temp_file, method_content)
                code_method_temp_lines = file_util.read_file_data_for_line(code_method_temp_file)
                code_method_temp_content = ''

                local_params_appear_list = []  # 改行出现过本地变量，因为出现过才能使用其作为条件判断
                code_line_pre = ''  # 前一行代码
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

                    # if语句后面无{}的时候不可插入code
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
                            and ('break' not in code_line) \
                            and ('\\' not in code_line):

                        is_insert_nouse_code = random.randint(0, 10)
                        if is_insert_nouse_code > 9:  # 该逗号是否插入代码

                            code_params_type = random.randint(0, 3)
                            if code_params_type == 0:  # 函数声明参数设置条件
                                if method_defind_params_list:

                                    method_param_insert = method_defind_params_list[
                                        random.randint(0, len(method_defind_params_list) - 1)]  # 随机抽出一个参数
                                    print '使用函数声明变量为条件判断插入code params:' + method_param_insert
                                    code_temple = handle_code_temples(method_param_insert)

                                    code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple,
                                                                                code_line, method_assess, property_list,
                                                                                insert_methods_list=methods_list)
                                else:
                                    code_temple = insert_no_param_code()
                                    code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple,
                                                                                code_line, method_assess, property_list,
                                                                                insert_methods_list=methods_list)

                            elif code_params_type == 1:  # 本地参数设置条件
                                if local_params_appear_list:  # 出现过的本地变量参数
                                    method_param_insert = local_params_appear_list[
                                        random.randint(0, len(local_params_appear_list) - 1)]  # 随机抽出一个参数
                                    code_temple = handle_code_temples(method_param_insert)
                                    print '使用本地变量为条件判断插入code params:' + method_param_insert
                                    code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple,
                                                                                code_line, method_assess,property_list,
                                                                                insert_methods_list=methods_list)

                                else:
                                    code_temple = insert_no_param_code()
                                    code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple,
                                                                                code_line, method_assess, property_list,
                                                                                insert_methods_list=methods_list)
                            else:

                                code_temple = insert_no_param_code()

                                code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple,
                                                                            code_line, method_assess, property_list,
                                                                            insert_methods_list=methods_list)
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
                                    code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple,
                                                                                code_line, method_assess, property_list, True,
                                                                                insert_methods_list=methods_list)
                                else:
                                    code_temple = insert_no_param_code()
                                    code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple,
                                                                                code_line, method_assess, property_list, True,
                                                                                insert_methods_list=methods_list)

                            elif code_params_type == 1:
                                if local_params_appear_list:
                                    method_param_insert = local_params_appear_list[
                                        random.randint(0, len(local_params_appear_list) - 1)]  # 随机抽出一个参数
                                    code_temple = handle_code_temples(method_param_insert)
                                    print '使用本地变量为条件判断插入code params:' + method_param_insert
                                    code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple,
                                                                                code_line, method_assess, property_list, True,
                                                                                insert_methods_list=methods_list)

                                else:
                                    code_temple = insert_no_param_code()
                                    code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple,
                                                                                code_line, method_assess, property_list, True,
                                                                                insert_methods_list=methods_list)
                            else:

                                code_temple = insert_no_param_code()

                                code_method_temp_content = addCodeToSrcCode(code_method_temp_content, code_temple,
                                                                            code_line, method_assess, property_list, True,
                                                                            insert_methods_list=methods_list)
                        else:
                            # 不添加
                            code_method_temp_content = code_method_temp_content + code_line

                    else:
                        # 不添加
                        code_method_temp_content = code_method_temp_content + code_line

                file_data = file_data.replace(method_content, code_method_temp_content)
                file_util.wite_data_to_file(file_path, file_data)

                # params_list = parse_method_local_params(method_content)
                # if params_list:
                #     print params_list
                #     print '\n'

def insert_methods(file_path_m, sdk_confuse_dir): #类内插入方法

    methods_list = []

    # 处理对应.h文件
    file_path_h = file_path_m.replace('.m', '.h')
    file_data_h = file_util.read_file_data(file_path_h)
    file_data_m = file_util.read_file_data(file_path_m)

    interface_content = ''
    if file_data_h:
        interface_content_list = re.findall(r'@interface[\s\S]+@end', file_data_h)
        if interface_content_list:
            if len(interface_content_list) > 1:
                return methods_list
            interface_content = interface_content_list[0]   #只处理一个文件只有一个类的情况，多个类的暂不处理

    implementation_content_list = re.findall(r'@implementation[\s\S]+@end', file_data_m) #只处理一个文件只有一个类的情况，多个类的暂不处理
    if not implementation_content_list or len(implementation_content_list) > 1:
        return methods_list
    implementation_content = implementation_content_list[0]

    # 找出类名
    class_def_content = re.findall(r'@implementation \w+', file_data_m)
    if class_def_content and len(class_def_content) > 0:
        class_name = class_def_content[0].replace('@implementation', '').replace(' ', '').strip()


    method_access = ''
    method_tag_list_a = re.findall(r'\n- ?\(', implementation_content) #成员方法属性个数 -
    method_tag_list_b = re.findall(r'\n\+ ?\(', implementation_content) #类方法个数+

    if method_tag_list_a and len(method_tag_list_a) > 0 and len(method_tag_list_a) > len(method_tag_list_b):
        method_access = '-'
    else:
        method_access = '+'

    if implementation_content:
        # implementation_content = implementation_content_list[0]
        tempLog_path = sdk_confuse_dir + 'temp/tempLog.log'
        file_util.wite_data_to_file(tempLog_path, implementation_content)
        temp_log_content_lines = file_util.read_file_data_for_line(tempLog_path)

        method_imp_content = ''
        for line in temp_log_content_lines:

            line_a = line.strip()
            if line_a.startswith('- (') or line_a.startswith('-(') or line_a.startswith('-  (') \
                    or line_a.startswith('+ (') or line_a.startswith('+(') or line_a.startswith('+  (') \
                    or line_a.startswith('@end'):  # 前面插入
                is_insert_method = random.randint(0, 2)
                if is_insert_method == 1:  # 随机是否需要增加方法

                    method_count = random.randint(1, 2)  # 随机需要增加方法的个数
                    insert_time = datetime_util.get_current_time()

                    for mc in range(method_count):
                        method = create_method_boj(method_access)
                        method.class_name = class_name
                        methods_list.append(method)
                        line = ('\n//===insert my method start=== %s\n' % insert_time) + method.methodContent + ('\n//===insert my method end=== %s\n' % insert_time) + line
                        # method_def_content = method_def_content + '\n//insert my method def start\n' + method.method_def + '\n//insert my method def end\n'

            method_imp_content = method_imp_content + line

        file_data_m = file_data_m.replace(implementation_content, method_imp_content)
        file_util.wite_data_to_file(file_path_m, file_data_m)

        if methods_list:
            insert_m_content = ''
            for m in methods_list:
                insert_m_content = insert_m_content + m.method_def + '//insert method def\n'

            if len(insert_m_content) > 0:
                interface_content_new = interface_content.replace("@end", insert_m_content + "@end")
                file_data_h = file_data_h.replace(interface_content, interface_content_new)
                file_util.wite_data_to_file(file_path_h, file_data_h)
    return methods_list

def code_temp_call_method(mehtod, method_assess): #调用插入的函数
    method_def = mehtod.method_def
    w_inedx = random.randint(0, len(string.letters) - 1)
    param_name = string.letters[w_inedx] + '_' + str(w_inedx)
    call_content = ''
    if mehtod.methodReturnType == 'void':
        if method_assess == '-':
            if mehtod.methodIsPrivate == '-':
                call_content = '\n\t[self %s];\n' % mehtod.method_call
            else:
                call_content = '\n\t[%s %s];\n' % (mehtod.class_name, mehtod.method_call)
        else:
            if mehtod.methodIsPrivate == '+':
                call_content = '\n\t[%s %s];\n' % (mehtod.class_name, mehtod.method_call)
    else:
        if method_assess == '-':
            if mehtod.methodIsPrivate == '-':
                call_content = '\n\t' + mehtod.methodReturnType + ' ' + param_name + ' = [self %s];\n' % mehtod.method_call
            else:
                call_content = '\n\t' + mehtod.methodReturnType + ' ' + param_name + ' = [%s %s];\n' % (mehtod.class_name, mehtod.method_call)
        else:
            if mehtod.methodIsPrivate == '+':
                call_content = '\n\t' + mehtod.methodReturnType + ' ' + param_name + ' = [%s %s];\n' % (mehtod.class_name, mehtod.method_call)
        if len(call_content) > 0:
            call_content = call_content + '\tif(%s){}\n' % param_name
    if len(call_content) > 0:
        call_content = replace_code_temp(call_content, '')
    return call_content

def addCodeToSrcCode(code_method_temp_content, code_temple, insert_line_content, method_assess, property_list, is_later=False, insert_methods_list=None):
    call_content = ''
    call_property_content = ''
    if len(insert_methods_list) > 0: #调用方法
        method_obj = insert_methods_list[random.randint(0, len(insert_methods_list) - 1)]
        call_content = code_temp_call_method(method_obj, method_assess)


    if method_assess == '-' and len(property_list) > 0: #调用属性
        for property in property_list:
            if property.propertyType in oc_method_util.numbers_params_type:
                #赋值判断
                if_code = oc_method_util.create_operation_expression_compare('self.%s' % (property.propertyName))
                call_property = 'self.%s = %s;\n\tif(%s){}' % (property.propertyName, str(random.randint(1, 9999)), if_code)
            else:
                call_property = '\tif(self.%s){}' % property.propertyName

            call_property_content = call_property_content + '\n\t' + call_property

        if call_property_content != '':
            call_property_content = call_property_content + '\n'

    code_temple = call_content + call_property_content + code_temple

    global insert_code_sum
    insert_code_sum = insert_code_sum + 1
    insert_time = datetime_util.get_current_time()
    if is_later:
        print '前面插入：' + insert_line_content
        code_method_temp_content = code_method_temp_content + ('\n\t\t//====insert my code start===  %s\n\t\t{\n\t\t' % (insert_time)) + code_temple + ('\n\t\t}\n\t\t//====insert my code end===  %s\n\n' % (insert_time)) + insert_line_content
    else:
        print '后面插入' + insert_line_content
        code_method_temp_content = code_method_temp_content + insert_line_content
        code_method_temp_content = code_method_temp_content + ('\n\t\t//====insert my code start===  %s\n\t\t{\n\t\t' % (insert_time)) + code_temple + ('\n\t\t}\n\t\t//====insert my code end===  %s\n\n' % (insert_time))
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

    code_temple = code_temples[random.randint(0, len(code_temples) - 1)]  # 随机抽出一个代码模版

    code_temple = replace_code_temp(code_temple, condition_var)

    return code_temple


def replace_code_temp(code_temple, condition_var):

    word_aar = []

    # 替换代码模版中的内容start
    code_temple = code_temple.replace('var_temp', condition_var)  # 添加表达式替换代码模版占位符
    code_temple_params_list = re.findall(r'ppppp\w+_ppppp', code_temple)  # ppppp\w+_ppppp代表字符
    for code_temple_param in code_temple_params_list:
        w1, w2 = word_util.random_2words_not_same_inarr(word_aar)
        code_temple = code_temple.replace(code_temple_param, w1 + w2.capitalize())
    code_mumber_temple_params_list = re.findall(r'iiiii\w+_iiiii', code_temple)  # iiiii\w+_iiiii的范围可以是负数
    for code_mumber_temple_params in code_mumber_temple_params_list:
        numbera = random.randint(-1000, 10000)
        code_temple = code_temple.replace(code_mumber_temple_params, str(numbera))
    code_int_temple_params_list = re.findall(r'int\w+_int', code_temple)  # int\w+_int需要时正整数
    for code_int_temple_param in code_int_temple_params_list:
        int_value = random.randint(1, 10000)
        code_temple = code_temple.replace(code_int_temple_param, str(int_value))

    code_float_temple_params_list = re.findall(r'float\d+_float', code_temple)  # float值
    for float_value in code_float_temple_params_list:
        int_value = random.randint(1, 10000)
        float_v = float(int_value)
        code_temple = code_temple.replace(float_value, str(float_v))

    code_numcop_list = re.findall(r'numcop\d+_numcop', code_temple)  # 数值比较运算符
    for numcop in code_numcop_list:
        bijiao_s = oc_method_util.operation_bijiao_arr[random.randint(0, len(oc_method_util.operation_bijiao_arr) - 1)] #比较符号
        code_temple = code_temple.replace(numcop, bijiao_s)

    code_bool_list = re.findall(r'bool\d+_bool', code_temple)  # yes no
    for boola in code_bool_list:
        bool_value = oc_method_util.bool_value_arr[random.randint(0, len(oc_method_util.bool_value_arr) - 1)]  # 比较符号
        code_temple = code_temple.replace(boola, bool_value)

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
        value_int_arr = word_util.generateIntArr(dic_count)
        dic_content = ''
        for i in range(dic_count):
            w1, w2 = word_util.random_2words_not_same_inarr(word_aar)

            value_type = random.randint(1, 3)
            if i == dic_count - 1:
                if value_type == 3:
                    val1 = '@"' + w1 + '" : @(' + value_int_arr[i] + ') '
                else:
                    val1 = '@"' + w1 + '" : @"' + w2 + '" '
            else:
                if value_type == 3:
                    val1 = '@"' + w1 + '" : @(' + value_int_arr[i] + '), '
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
                    mPropertyInfo = PropertyInfo()
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

        result_list = re.findall(r'\w+ (?:\*|\* )?\w+ ?=', method_data_temp) #提取类似 NSString * timeStamp=   NSArray *responseArray =
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

def create_method_boj(method_access):

     #生成的方法内容、方法定义、参数类型数组、参数名称数组、插入占位符数组
    mi, imp_mmmmmm_imp_index = oc_method_util.createMehtodTemp(method_access)
    if len(mi.methodParamsNameList) > 0:

        for i in imp_mmmmmm_imp_index:
            method_param_insert = mi.methodParamsNameList[random.randint(0, len(mi.methodParamsNameList) - 1)]
            code_temple = handle_code_temples(method_param_insert)
            imp_mmmmmm_imp = 'imp_mmmmmm_%s_imp' % i
            # print 'imp_mmmmmm_imp=' + imp_mmmmmm_imp
            mi.methodContent = mi.methodContent.replace(imp_mmmmmm_imp, code_temple)
    else:

        code_temple = insert_no_param_code()
        mi.methodContent = mi.methodContent.replace('imp_mmmmmm_0_imp', code_temple)

    # mi.methodContent = method_implement
    return mi