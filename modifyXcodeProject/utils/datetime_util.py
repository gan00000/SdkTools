#coding=utf-8
import imp
import sys
from datetime import datetime

imp.reload(sys)
sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的

import os
import re

def get_current_time():
    currentDateAndTime = datetime.now()
    # print currentDateAndTime
    currentTime = currentDateAndTime.strftime("%Y-%m-%d %H:%M:%S")
    return currentTime

def get_current_time_2():
    currentDateAndTime = datetime.now()
    # print currentDateAndTime
    currentTime = currentDateAndTime.strftime("%Y_%m_%d_%H_%M_%S")
    return currentTime