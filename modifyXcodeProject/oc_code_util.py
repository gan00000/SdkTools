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

def removeAnnotate(file_data):
    file_data = re.sub(r'^//.*', '', file_data)
    file_data = re.sub(r'\n//.*', '', file_data)
    file_data = re.sub(r'([^:/])//.*', '\\1', file_data)  # 这里防止链接被去掉，分组捕获
    file_data = re.sub(r'/\*{1,2}[\s\S]*?\*/', '', file_data)  # 非贪婪模式
    return file_data