#coding=utf-8
import imp
import sys

from modifyXcodeProject.model import PropertyInfo
from modifyXcodeProject.model.MethodInfo import MethodInfo
from modifyXcodeProject.utils import file_util

imp.reload(sys)
sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的

import os
import re

import chardet

# 导入 random(随机数) 模块
import random

operation_arr = ['+','-','*','%','/']
words_gl = []
#找出方法名字，修改方法名
def create_operation_expression(rightVar):
    value1 = random.randint(-100, 100000)
    content = str(value1)
    operation_count = random.randint(0, 5)
    if (operation_count == 0):
        return content
    for c in range(operation_count):
        operation_type = operation_arr[random.randint(0, len(operation_arr) -1)]
        content = content + ' ' + operation_type + ' ' + str(random.randint(1, 100000))
    operation_type = operation_arr[random.randint(0, len(operation_arr) - 1)]
    content = rightVar + ' ' + operation_type + ' (' + content + ')'
    return content

def create_case_expression(leftVar, rightVar):
    case_count = random.randint(1, 10)
    content = ''
    for c in range(case_count):
        case_value = random.randint(-100, 1000)
        # print case_value
        ex = create_operation_expression(rightVar)
        if ex:
            content = content + 'case ' + str(case_value) +':\n\t\t\t{\n\t\t\t\t' \
                      + leftVar + ' = ' + ex + '; \n\t\t\t break;\n\t\t\t}\n\t\t\t'

    return content

# def create_switch_expression(switchvar, leftVar):

if __name__ == '__main__':
    # print create_case_expression('aaa', 'bbb')
    print create_operation_expression('aadd')