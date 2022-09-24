#coding=utf-8
import imp
import sys
imp.reload(sys)
sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的
import re
import os
import excelutil

sdk_path_temp_1 = "/Users/gan/Downloads/fanyi/src/"


def find_ZW(f_path, line_str):
    pchinese = re.compile(u"[\u4e00-\u9fa5]+")  # 判断是否为中文的正则表达式
    # for line in ffile.readlines():  # 循环读取要读取文件的每一行
    txt = unicode(line_str)
    fcontent = pchinese.findall(txt)  # 使用正则表达获取中文
    # print str
    if fcontent:
        for v in fcontent:
            # print f_path + ":" + v
            print v
    return line_str

def find_ZW_1(str):
    pchinese = re.compile(u"[\u4e00-\u9fa5]+")  # 判断是否为中文的正则表达式
    # for line in ffile.readlines():  # 循环读取要读取文件的每一行
    txt = unicode(str)
    fcontent = pchinese.findall(txt)  # 使用正则表达获取中文
    # print str
    if fcontent:
        return fcontent
    return None


def find_chinese():
    if os.path.exists(sdk_path_temp_1):
        list_dirs = os.walk(sdk_path_temp_1)
        for root, dirs, files in list_dirs:
            for f in files:
                if f == ".DS_Store":
                    break

                f_path = os.path.join(root, f)
                # print f_path
                fobj = open(f_path,"r")  # 首先先创建一个文件对象
                # print f_txt  # 打印所读取到的内容
                for line in fobj.readlines():
                    # print line
                    find_ZW(f_path, str(line))

                fobj.close()


def fanyi_replace(fanyi_zh_ch):

    if os.path.exists(sdk_path_temp_1):
        list_dirs = os.walk(sdk_path_temp_1)
        for root, dirs, files in list_dirs:
            for f in files:
                if f == ".DS_Store":
                    break

                f_path = os.path.join(root, f)
                # print f_path

                f_obj = open(f_path, "r")  # 首先先创建一个文件对象
                f_all_txt = f_obj.read()  # 用read()方法读取文件内容
                f_obj.close()

                chinese_list = find_ZW_1(f_all_txt)
                if chinese_list is None:
                    pass
                else:
                    for v in chinese_list:
                        print v

                        f_all_txt = start_replace(f_all_txt, fanyi_zh_ch, v)


                    if f_all_txt == "":
                        pass
                    else:
                        f_obj = open(f_path, 'w')  # 首先先创建一个文件对象
                        f_obj.write(f_all_txt)
                        f_obj.flush()
                f_obj.close()


def start_replace(f_all_txt, fanyi_zh_ch, v):
    m = False;
    for key, value in fanyi_zh_ch.items():
        if key == v:
            m = True
            f_all_txt = f_all_txt.replace(v, value)
            return f_all_txt
    if m:
        pass
    else:
        print "出现问题=======================:" + v
    return f_all_txt


excel = os.path.join("/Users/gan/Downloads","翻译简体_11.xlsx");
# excelutil.writeexcel(excel,aa)
fanyi_zh_ch = excelutil.readExcel(excel)

# fanyi_replace(fanyi_zh_ch)
find_chinese()


