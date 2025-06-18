#coding=utf-8
import imp
import string
import sys
import uuid

import md5util
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


# 匹配OC字符串字面量 @"..."
string_regex_2 = re.compile(r'@\"(.*?)\"')
#
    # @\"：匹配字面量字符串的开头，OC中字符串字面量以 @" 开始。
    # (?:\\.|[^"\\])*?：匹配字符串内部的内容
    #     \\.：匹配转义字符（例如 \"、\\ 等）
    #     [^"\\]：匹配非双引号且非反斜杠的任意字符
    #     *?：非贪婪匹配，尽可能少匹配字符，直到遇到下一个闭合的 "
    # \"：匹配字符串的结束双引号

string_regex = re.compile(r'@\"(?:\\.|[^"\\])*?\"')

# 正则表达式中常用的特殊字符（用于简单判断是否可能是正则表达式）
regex_special_chars = r'^$.*+?[](){}|\\'
exclude_str = ["%@", "%f", "%2ld", "\\n", "%02x", "0X", "%d", "%ld", "text/plain", "text/html", "application/json",
               "text/json", "text/javascript", "UTF-8", "charset", "POST", "image/jpeg", "USD", "sdk-config", "id",
               "Content-Type", "txt", "true", "false", "bundle", "png", "asset", "CFBundleURLTypes", "CFBundleURLName", "CFBundleURLSchemes", "CFBundleDisplayName"
               , "CFBundleVersion", "CFBundleShortVersionString", "CFBundleIdentifier", "CFBundleName"]

def looks_like_regex(s):
    return any(ch in s for ch in regex_special_chars)

def find_oc_regex_strings(filepath):
    results = []
    content = file_util.read_file_data(filepath)
    content = removeAnnotate(content)
    matches = string_regex.findall(content)
    for m in matches:
        results.append(m)
    return results

def scan_directory_for_oc_regexes(base_dir):
    all_results = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.m') or file.endswith('.h'):
                path = os.path.join(root, file)
                regex_strings = find_oc_regex_strings(path)
                if regex_strings:
                    for v in regex_strings:
                        matches_inner = string_regex_2.findall(v)
                        if matches_inner:
                            stings_v = matches_inner[0]
                            if len(stings_v.strip()) > 1 and stings_v not in exclude_str and v not in all_results:
                                all_results.append(v)
    return all_results

def replace_string_tag(base_dir, regexes):

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.m'):
                path = os.path.join(root, file)
                content = file_util.read_file_data(path)
                for xv in regexes:
                    md5_str = md5util.md5hex(xv)
                    md5_rep = "wwwww_tag_wwwww_" + md5_str  # w1 + '_' + w2
                    content = content.replace(xv, md5_rep)
                file_util.wite_data_to_file_noencode(path, content)

if __name__ == "__main__":

    oc_path = '/Users/ganyuanrong/iOSProject/flsdk_ios/GamaSDK_iOS_Integration/FLSDK'
    results = scan_directory_for_oc_regexes(oc_path)
    replace_string_tag(oc_path, results)
    for regexes in results:
        md5_str = md5util.md5hex(regexes)
        md5_rep = "wwwww_tag_wwwww_" + md5_str

        print '#define %s        %s  //%s' % (md5_rep, regexes, regexes)