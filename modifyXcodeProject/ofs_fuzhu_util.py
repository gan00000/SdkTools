#coding=utf-8
import imp
import json
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




if __name__ == "__main__":

    config_data = file_util.read_file_data(
        '/Users/ganyuanrong/KPlatform/KPlatform_iOS/SDK_MAIN/Resources/V5/kplat20240717.json')
    config_data_json = json.loads(config_data)

    paramsa = {}
    paramsa_con = {}
    for k, v in config_data_json.items():
        if 'param_' in k:
            w1 = word_util.get_random_letter_word()
            # print k + '=' + v
            paramsa_con[k] = w1
            k_old = k.replace('param_', '')
            paramsa[w1] = k_old

    for k, v in paramsa_con.items():
        print '"%s"     :       "%s",' % (k, v)

    # 将字典转换为JSON字符串
    json_string = json.dumps(paramsa)
    print json_string

