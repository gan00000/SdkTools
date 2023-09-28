#coding=utf-8
import imp
import string
import sys
import uuid

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

operation_arr = ['+', '-', '*', '/']
operation_bijiao_arr = ['>', '==', '<', '<=', '>=', '!=']
bool_value_arr = ['false', 'true']

numbers_params_type = ['float', 'int', 'double']

cpp_base_type = ['int', 'bool', 'void', 'int32_t', 'int64_t','double','float']

#找出方法名字，修改方法名
def create_operation_expression(rightVar):
    value1 = random.randint(1, 999)
    content = str(value1)
    operation_count = random.randint(1, 5)
    # if (operation_count == 0):
    #     return content
    for c in range(operation_count):
        operation_type = operation_arr[random.randint(0, len(operation_arr) -1)]
        content = content + ' ' + operation_type + ' ' + str(random.randint(1, 999))
    operation_type = operation_arr[random.randint(0, len(operation_arr) - 2)]
    content = rightVar + ' ' + operation_type + ' ' + content
    return content

def create_operation_expression_compare(rightVar):
    left_s = create_operation_expression(rightVar)
    bijiao_s = operation_bijiao_arr[random.randint(0, len(operation_bijiao_arr) - 1)] #比较符号
    right_value = random.randint(1, 100000)
    content = left_s + ' ' + bijiao_s + ' ' + str(right_value)
    return content

def create_operation_expression_compare2(rightVar):
    # left_s = create_operation_expression(rightVar)
    bijiao_s = operation_bijiao_arr[random.randint(0, len(operation_bijiao_arr) - 1)] #比较符号
    right_value = random.randint(1, 100000)
    content = rightVar + ' ' + bijiao_s + ' ' + str(right_value)
    return content


def cpp_code_auto_create1():
    var_arr = []
    var1 = word_util.random_1words_not_same_inarr(var_arr)
    var1 = var1.lower()
    lett = string.letters[random.randint(0, len(string.letters) - 1)]
    var1 = lett + '_' + var1

    var_arr.append(var1)

    type_var = numbers_params_type[random.randint(0, len(numbers_params_type) - 1)]
    content = '%s %s = %s;\n' % (type_var, var1, str(random.randint(1, 9999)))
    if_count = random.randint(1, 12)
    for i in range(if_count):
        var3 = word_util.random_1words_not_same_inarr(var_arr)
        lett = string.letters[random.randint(0, len(string.letters) - 1)]
        var3 = lett + '_' + var3

        type_var2 = numbers_params_type[random.randint(0, len(numbers_params_type) - 1)]
        content = content + '\n%s %s = %s;' % (type_var2, var3, str(random.randint(1, 999)))
        content = content + '\nif(%s){\n' % (create_operation_expression_compare(var1))
        # var2 = word_util.random_1words_not_same_inarr(var_arr)
        content2 = '\t%s = %s;' % (var3, create_operation_expression(var1))
        content = content + content2 + '\n}'
        need_else = random.randint(1, 2)
        if need_else == 1:
            content3 = '\t%s = %s;' % (var3, create_operation_expression(var1))
            content = content + 'else{\n%s\n}\n' % (content3)
        else:
            content = content + '\n'
        var1 = var3
        var_arr.append(var3)
    # print content
    return var_arr, content

def cpp_code_auto_create2():
    var_arr = []
    var1 = word_util.random_1words_not_same_inarr(var_arr)
    var1 = var1.lower()
    lett = string.letters[random.randint(0, len(string.letters) - 1)]
    var1 = lett + '_' + var1

    var_arr.append(var1)
    type_var1 = numbers_params_type[random.randint(0, len(numbers_params_type) - 1)]
    content = '%s %s = %s;\n' % (type_var1, var1, str(random.randint(1, 9999)))
    # content = content + '\nif(%s){\n' % (create_operation_expression_compare(var1))
    # var2 = word_util.random_1words_not_same_inarr(var_arr)
    # content2 = '\t%s = %s;' % (var2, create_operation_expression(var1))
    # content = content + content2 + ' if_temp_if\n}'
    # content = ''
    if_count = random.randint(1, 5)
    for i in range(if_count):

        ifdata = '\nif(%s){\n' % (create_operation_expression_compare2(var1))
        var3 = word_util.random_1words_not_same_inarr(var_arr)
        lett = string.letters[random.randint(0, len(string.letters) - 1)]
        var3 = lett + '_' + var3

        type_var2 = numbers_params_type[random.randint(0, len(numbers_params_type) - 1)]
        ifdata2 = '\t%s %s = %s;' % (type_var2, var3, create_operation_expression(var1))
        ifdata = ifdata + ifdata2
        if i == if_count - 1:
            ifdata = ifdata + '\n}'
        else:
            ifdata = ifdata + ' if_temp%s_if\n}' % (str(i))

        if i == 0:
            content = content + ifdata
        else:
            content = content.replace('if_temp%s_if' % (str(i - 1)), ifdata)
        var1 = var3
        var_arr.append(var3)
    # print content
    return var_arr, content

def create_case_expression(leftVar, rightVar):
    case_count = random.randint(1, 16)
    content = ''
    case_value_aar = []
    for c in range(case_count):
        case_value = random.randint(-100, 999)
        while case_value in case_value_aar:
            case_value = random.randint(-100, 999)
        # print case_value
        ex = create_operation_expression(rightVar)
        if ex:
            content = content + 'case ' + str(case_value) +':\n\t\t\t{\n\t\t\t\t' \
                      + leftVar + ' = ' + ex + '; \n\t\t\t break;\n\t\t\t}\n\t\t\t'
            case_value_aar.append(case_value)

    # print content
    return content

def cpp_switch_code():
    var_arr = []
    var1, var2 = word_util.random_2words_not_same_inarr(var_arr)
    w_inedx = random.randint(0, len(string.letters) - 1)
    var1 = string.letters[w_inedx] + '_' + var1

    w_inedx = random.randint(0, len(string.letters) - 1)
    var2 = string.letters[w_inedx] + '_' + var2

    type_var1 = 'int'#numbers_params_type[random.randint(0, len(numbers_params_type) - 1)]
    type_var2 = numbers_params_type[random.randint(0, len(numbers_params_type) - 1)]
    content = '%s %s = %s;\n' % (type_var1, var1, str(random.randint(1, 999)))
    content = content + '%s %s = %s;\n' % (type_var2, var2, str(random.randint(1, 999)))
    switch_content = 'switch (ppppp1_ppppp) {\n' \
    '   case_content_case' \
    '   default:\n' \
    '       break;\n\t\t\t}'
    content = content + switch_content
    content = content.replace('ppppp1_ppppp', var1)
    data = create_case_expression(var1, var2)
    content = content.replace('case_content_case', data)
    var_return = []
    var_return.append(var1)
    var_return.append(var2)
    return var_return,content

def replace_code_placeholder(code_temple_index, code_temple, condition_var, code_temples, again_count=1):

    word_aar = []

    # 替换代码模版中的内容start
    if condition_var and len(condition_var) > 0:
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
        bijiao_s = operation_bijiao_arr[random.randint(0, len(operation_bijiao_arr) - 1)] #比较符号
        code_temple = code_temple.replace(numcop, bijiao_s)

    code_bool_list = re.findall(r'bool\d+_bool', code_temple)  # yes no
    for boola in code_bool_list:
        bool_value = bool_value_arr[random.randint(0, len(bool_value_arr) - 1)]  # 比较符号
        code_temple = code_temple.replace(boola, bool_value)

    code_type_mumber_list = re.findall(r'type_mumber\d+_type', code_temple)  # 数字类型
    for num_type in code_type_mumber_list:
        type_value = numbers_params_type[random.randint(0, len(numbers_params_type) - 1)]
        code_temple = code_temple.replace(num_type, type_value)

    operator_list = re.findall(r'operator\d+_operator', code_temple)  # 数字运算符
    for operator in operator_list:
        operator_value = operation_arr[random.randint(0, len(operation_arr) - 1)]
        code_temple = code_temple.replace(operator, operator_value)

    if 'case_content_case' in code_temple:
        w1, w2 = word_util.random_2words_not_same_inarr(word_aar)
        case_left_var = w1 + w2.capitalize()
        w1, w2 = word_util.random_2words_not_same_inarr(word_aar)
        case_right_var = w1
        code_temple = code_temple.replace('case_left_var', case_left_var)
        code_temple = code_temple.replace('case_right_var', case_right_var)
        case_temp_content = create_case_expression(case_left_var, case_right_var)
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

    codeTemplate_list = re.findall(r'CodeTemplate\d+_CodeTemplate', code_temple)  # 数字运算符
    for codeTemplate in codeTemplate_list:
        if again_count == 1:
            isInsert = random.randint(1, 6)
            if isInsert > 2:
                aa_index = random.randint(0, len(code_temples) - 1)
                if code_temple_index != aa_index:
                    aa_code_temp = code_temples[aa_index]
                    a2_code_temple = replace_code_placeholder(aa_index, aa_code_temp, '', code_temples, 2)
                    code_temple = code_temple.replace(codeTemplate, a2_code_temple)
                else:
                    code_temple = code_temple.replace(codeTemplate, '')
            else:
                code_temple = code_temple.replace(codeTemplate, '')
        else:
            code_temple = code_temple.replace(codeTemplate, '')

    return code_temple

#删除注释
def removeAnnotate(code_data):
    # file_data_0 = replace_data_content(src_data, '/\\*\\*/', '')
    # file_data_1 = replace_data_content(file_data_0, '([^:/])//.*', '\\1')
    # file_data_2 = replace_data_content(file_data_1, '^//.*', '')
    # file_data_3 = replace_data_content(file_data_2, '/\\*{1,2}[\\s\\S]*?\\*/', '')
    # 先删掉注释，不然会拿到注释的变量
    # method_data_temp = re.sub(r'^//.*', '', method_data_temp)
    code_data = re.sub(r'//[\s\S]*?\n', '\n', code_data)
    # method_data_temp = re.sub(r'^ *//.*', '', method_data_temp)  #//[\s\S]*?\n
    code_data = re.sub(r'/\*{1,2}[\s\S]*?\*/', '', code_data)  # 非贪婪模式
    return code_data

if __name__ == '__main__':
    # print create_case_expression('aaa', 'bbb')
    #print create_operation_expression('aadd')

    for c in range(20):
        xx = random.randint(0, 2)
        print xx