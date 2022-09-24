#coding=utf-8

import os
import time
import json

if __name__ == '__main__':

    log_path = '/Users/gan/Documents/login.log_2018-01-25.log'
    flog_obj = open(log_path, "r")

    count = 0
    line = 0
    # print f_txt  # 打印所读取到的内容
    # log_list = flog_obj.readlines()
    gameCode = '\"gameCode\":\"twzjios\"'
    gameCode_m = '\"gameCode\":\"twzj\"'

    line = 0
    users = {}
    for mline in flog_obj.readlines():
        # print 'lineUnique---->' + lineUnique
        if 'login-loginLog' in mline and 'userId' in mline:
            if gameCode in mline or gameCode_m in mline:

                split_lines = mline.split('{')
                if len(split_lines) == 2:
                    line = line+1
                    line_2 = split_lines[1]
                    line_2 = '{' + line_2
                    data = json.loads(line_2)
                    userId = data['userId']
                    if userId:
                        users['userId_' + userId] = userId

    flog_obj.close()

    for k, v in users.items():
        print v

    # print 'line：' + str(line)
    # print 'count：' + str(count)
