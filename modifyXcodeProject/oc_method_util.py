#coding=utf-8
import imp
import string
import sys

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
words_gl = []

method_access = ['-', '+']
method_param_type_list = ['NSString *', 'float', 'int', 'BOOL', 'NSArray *', 'NSDictionary *', 'long', 'NSData *', 'NSString *', 'NSInteger', 'CGFloat', 'NSMutableDictionary *', 'NSObject *', 'NSMutableArray *']
method_return_type_list = method_param_type_list[:]
method_return_type_list.append('void')

numbers_params_type = ['float', 'int', 'long', 'NSInteger','CGFloat']

#找出方法名字，修改方法名
def create_operation_expression(rightVar):
    value1 = random.randint(1, 9999)
    content = str(value1)
    operation_count = random.randint(1, 8)
    # if (operation_count == 0):
    #     return content
    for c in range(operation_count):
        operation_type = operation_arr[random.randint(0, len(operation_arr) -1)]
        content = content + ' ' + operation_type + ' ' + str(random.randint(1, 9999))
    operation_type = operation_arr[random.randint(0, len(operation_arr) - 2)]
    content = rightVar + ' ' + operation_type + ' ' + content
    return content

def create_case_expression(leftVar, rightVar):
    case_count = random.randint(1, 16)
    content = ''
    case_value_aar = []
    for c in range(case_count):
        case_value = random.randint(-100, 10000)
        while case_value in case_value_aar:
            case_value = random.randint(-100, 10000)
        # print case_value
        ex = create_operation_expression(rightVar)
        if ex:
            content = content + 'case ' + str(case_value) +':\n\t\t\t{\n\t\t\t\t' \
                      + leftVar + ' = ' + ex + '; \n\t\t\t break;\n\t\t\t}\n\t\t\t'
            case_value_aar.append(case_value)

    return content


def create_operation_expression_compare(rightVar):
    left_s = create_operation_expression(rightVar)
    bijiao_s = operation_bijiao_arr[random.randint(0, len(operation_bijiao_arr) - 1)] #比较符号
    right_value = random.randint(1, 100000)
    content = left_s + ' ' + bijiao_s + ' ' + str(right_value)
    return content

# def create_switch_expression(switchvar, leftVar):

# -(void)startPayWithProductId_MMMethodMMM:(NSString *)productId cpOrderId_MMMethodMMM:(NSString *)cpOrderId extra_MMMethodMMM:(NSString *)extra gameInfo_MMMethodMMM:(GameUserModel*)gameUserModel accountModel_MMMethodMMM:
def createMehtodTemp(method_access):
    params_count = random.randint(0, 8) #随机参数个数
    params_type = []
    for c in range(params_count):
        params_type.append(method_param_type_list[random.randint(0, len(method_param_type_list) - 1)]) #随机一个参数类型
    method_access_a = method_access #method_access[random.randint(0, len(method_access) - 1)] #随机类或者成员方法
    method_return_type = method_return_type_list[random.randint(0, len(method_return_type_list) - 1)]
    method_def = method_access_a + ' (' + method_return_type + ')'

    method_call = ''

    word_aar = []

    string_params = []
    boolean_params = []
    params_name = []
    imp_mmmmmm_imp_inedx = []
    if params_count == 0:
        w1, w2 = word_util.random_2words_not_same_inarr(word_aar)
        method_def = method_def + w1 + w2.capitalize()

        method_call = w1 + w2.capitalize()  # 调用的语句

        # if pType in numbers_params_type or pType == 'BOOL':
        #
        #     method_call = method_call + ('int%s_int ' % (str(m)))
        #
        # elif pType == 'NSString *':
        #     method_call = method_call + ('@"ppppp%s_ppppp" ' % (str(m)))
        # else:
        #     method_call = method_call + ('nil ')

    else:
        m = 1
        for pType in params_type:
            w1, w2 = word_util.random_2words_not_same_inarr(word_aar)
            method_def = method_def + w1 + w2.capitalize() + ':(' + pType + ')' + w1 + '_' + str(m) + " "
            params_name.append(w1 + '_' + str(m)) #保存参数名称

            method_call = method_call + w1 + w2.capitalize() + ':' #调用的语句

            if pType in numbers_params_type or pType == 'BOOL':

                method_call = method_call + ('int%s_int ' % (str(m)))

            elif pType == 'NSString *':
                method_call = method_call + ('@"ppppp%s_ppppp" ' % (str(m)))
            else:
                method_call = method_call + ('nil ')


            m = m + 1
    method_def = method_def.strip() + ';'
    # print method_def

    method_implement = method_def.replace(';', '{ //insert method')
    # method_implement = '\n//===insert my method start=== \n' + method_implement
    if params_count == 0:
        method_implement = method_implement + '\n\timp_mmmmmm_%s_imp' % (str(0))
        imp_mmmmmm_imp_inedx.append(0)
    else:
        have_if = 0
        for i in range(len(params_type)):
            isvar = random.randint(0, 1)  # 是否作为判断添加code
            if isvar == 1:
                if_code = params_name[i]
                if params_type[i] in numbers_params_type:
                    if_code = create_operation_expression_compare(params_name[i])

                method_implement = method_implement + '\n\tif(%s){\n\t\timp_mmmmmm_%s_imp\n\t}' % (if_code, str(i))
                have_if = have_if + 1
                imp_mmmmmm_imp_inedx.append(i)

        if have_if == 0: #都没有的情况
            method_implement = method_implement + '\n\timp_mmmmmm_%s_imp' % (str(0))
            imp_mmmmmm_imp_inedx.append(0)

    return_content = ''
    if method_return_type == 'void':
        pass
    else:
        if method_return_type in params_type:
            m_index = params_type.index(method_return_type)
            return_content = '\n\treturn ' + params_name[m_index] + ';\n'
        else:
            w1, w2 = word_util.random_2words_not_same_inarr(word_aar)
            w_inedx = random.randint(0, len(string.letters) - 1)
            waa = string.letters[w_inedx] + '_' + str(w_inedx)
            if method_return_type in numbers_params_type or method_return_type == 'BOOL':
                return_content = '\n\t%s %s = %s;\n' % (method_return_type, waa, str(random.randint(0, 99999)))
                return_content = return_content + '\treturn ' + waa + ';\n'

            elif method_return_type == 'NSString *':
                return_content = '\n\tNSString *%s = @"%s";\n' % (waa, w2 + w1)
                return_content = return_content + '\treturn ' + waa + ';\n'
            else:
                return_content = '\n\t%s%s = nil;\n' % (method_return_type, waa)
                return_content = return_content + '\treturn ' + waa + ';\n'

    # method_implement = method_implement + ('\n %s} \n//===insert my method end===\n' % return_content)
    method_implement = method_implement + ('\n %s}' % return_content)

    mi = MethodInfo()
    mi.methodParamsNameList = params_name
    mi.methodParamsTypeList = params_type
    mi.methodContent = method_implement
    mi.methodReturnType = method_return_type
    mi.methodIsPrivate = method_access_a
    mi.methodNameCanChange = 0
    mi.method_def = method_def
    mi.method_call = method_call
    return mi, imp_mmmmmm_imp_inedx


if __name__ == '__main__':
    # print create_case_expression('aaa', 'bbb')
    #print create_operation_expression('aadd')
    for c in range(20):
        xx = random.randint(0, 2)
        print xx