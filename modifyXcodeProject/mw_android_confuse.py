#coding=utf-8
import imp
import sys
import uuid

from modifyXcodeProject import oc_class_parser, oc_method_util, cpp_code_util, oc_code_util
from modifyXcodeProject.model.AndResFileInfo import AndResFileInfo
from modifyXcodeProject.utils import file_util, word_util, datetime_util
from modifyXcodeProject.utils.PrpCrypt import PrpCrypt

imp.reload(sys)
sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的

import os
import re

import chardet

# 导入 random(随机数) 模块
import random

def getStringKey(src_dir_path):
    result_aar = []
    if os.path.exists(src_dir_path):
        list_dirs = os.walk(src_dir_path)

        for root, dirs, files in list_dirs:
            for file_name in files:
                file_path = os.path.join(root, file_name)  # 头文件路径
                file_data = file_util.read_file_data(file_path)
                file_data = re.sub('<!--.*-->', '', file_data)
                # '<string name="api_pay_web_payment">api/web/payment.page</string>'
                string_list = re.findall(r'<string name="(\w+)">.*</string>', file_data)
                for string_tag in string_list:
                    # print string_tag
                    if string_tag not in result_aar and string_tag not in exclude_string:
                        result_aar.append(string_tag)
    print 'string:'
    print result_aar
    return result_aar

def getColorKey(src_dir_path):
    result_aar = []
    if os.path.exists(src_dir_path):
        list_dirs = os.walk(src_dir_path)

        for root, dirs, files in list_dirs:
            for file_name in files:
                file_path = os.path.join(root, file_name)  # 头文件路径
                file_data = file_util.read_file_data(file_path)
                file_data = re.sub('<!--.*-->', '', file_data)
                # '<string name="api_pay_web_payment">api/web/payment.page</string>'
                string_list = re.findall(r'<color name="(\w+)">.*</color>', file_data)
                for string_tag in string_list:
                    # print string_tag
                    if string_tag not in result_aar:
                        result_aar.append(string_tag)
    print 'color:'
    print result_aar
    return result_aar


def getDimenKey(src_dir_path):
    result_aar = []
    if os.path.exists(src_dir_path):
        list_dirs = os.walk(src_dir_path)

        for root, dirs, files in list_dirs:
            for file_name in files:
                file_path = os.path.join(root, file_name)  # 头文件路径
                file_data = file_util.read_file_data(file_path)
                file_data = re.sub('<!--.*-->', '', file_data)
                # '<string name="api_pay_web_payment">api/web/payment.page</string>'
                string_list = re.findall(r'<dimen name="(\w+)">.*</dimen>', file_data)
                for string_tag in string_list:
                    # print string_tag
                    if string_tag not in result_aar:
                        result_aar.append(string_tag)
    print 'dimen:'
    print result_aar
    return result_aar

def getIds(src_dir_path):

    result_aar = []
    if os.path.exists(src_dir_path):
        list_dirs = os.walk(src_dir_path)

        for root, dirs, files in list_dirs:
            for file_name in files:
                file_path = os.path.join(root, file_name)  # 头文件路径
                file_data = file_util.read_file_data(file_path)
                # '<string name="api_pay_web_payment">api/web/payment.page</string>'
                file_data = re.sub('<!--.*-->', '', file_data)
                id_tag_list = re.findall(r'android:id="@\+id/\w+"', file_data)
                for id_tag in id_tag_list:
                    id_name = id_tag.replace('android:id="@+id/', '').replace('"', '')
                    # print id_name
                    if id_name not in result_aar:
                        result_aar.append(id_name)
    print 'id:'
    print result_aar
    return result_aar

def rename_res_file(src_dir_path):
    drawable_file_aar = []
    layout_file_aar = []
    mipmap_file_aar = []
    values_file_aar = []
    anim_file_aar = []

    old_new_map_drawable = {}
    old_new_map_layout = {}
    old_new_map_mipmap = {}
    old_new_map_values = {}
    old_new_map_anim = {}

    word_arr = []
    if os.path.exists(src_dir_path):
        list_dirs = os.walk(src_dir_path)

        for root, dirs, files in list_dirs:

            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                file_name_key = file_name.replace('.', '_')

                file_info = AndResFileInfo()
                file_info.name = file_name
                file_info.file_root = root
                file_info.file_path = os.path.join(root, file_name)

                file_name_no_extension = os.path.splitext(file_name)[0]
                file_extension = os.path.splitext(file_name)[1]

                file_info.file_name_no_extension = file_name_no_extension
                file_info.file_extension = file_extension

                pref = 'okokok_'
                if 'res/drawable' in root:

                    if old_new_map_drawable.has_key(file_name_key):
                        file_new_name = old_new_map_drawable[file_name_key]
                    else:

                        w1, w2 = word_util.random_2words_not_same_inarr(word_arr)
                        w1 = w1.lower()
                        file_new_name = pref + w1 + file_extension
                        file_name_no_extension_new = pref + w1
                        file_info.type = 'drawable'
                        file_info.file_name_no_extension_new = file_name_no_extension_new
                        file_info.name_new = file_new_name
                        file_new_path = os.path.join(root, file_new_name)
                        file_info.file_path_new = file_new_path
                        drawable_file_aar.append(file_info)
                        old_new_map_drawable[file_name_key] = file_new_name

                    file_new_path = os.path.join(root, file_new_name)
                    os.rename(file_info.file_path, file_new_path)



                if 'res/layout' in root:
                    if old_new_map_layout.has_key(file_name_key):
                        file_new_name = old_new_map_layout[file_name_key]
                    else:
                        w1, w2 = word_util.random_2words_not_same_inarr(word_arr)
                        w1 = w1.lower()
                        file_new_name = pref + w1 + file_extension
                        file_name_no_extension_new = pref + w1

                        file_info.type = 'layout'
                        file_info.file_name_no_extension_new = file_name_no_extension_new
                        file_info.name_new = file_new_name
                        file_new_path = os.path.join(root, file_new_name)
                        file_info.file_path_new = file_new_path
                        layout_file_aar.append(file_info)
                        old_new_map_layout[file_name_key] = file_new_name

                    file_new_path = os.path.join(root, file_new_name)
                    os.rename(file_info.file_path, file_new_path)


                if 'res/mipmap' in root:

                    if old_new_map_mipmap.has_key(file_name_key):
                        file_new_name = old_new_map_mipmap[file_name_key]
                    else:
                        w1, w2 = word_util.random_2words_not_same_inarr(word_arr)
                        w1 = w1.lower()
                        file_new_name = pref + w1 + file_extension
                        file_name_no_extension_new = pref + w1

                        file_info.type = 'mipmap'
                        file_info.file_name_no_extension_new = file_name_no_extension_new
                        file_info.name_new = file_new_name
                        file_new_path = os.path.join(root, file_new_name)
                        file_info.file_path_new = file_new_path
                        mipmap_file_aar.append(file_info)

                        old_new_map_mipmap[file_name_key] = file_new_name

                    file_new_path = os.path.join(root, file_new_name)
                    os.rename(file_info.file_path, file_new_path)


                if 'res/values' in root:

                    if old_new_map_values.has_key(file_name_key):
                        file_new_name = old_new_map_values[file_name_key]
                    else:

                        w1, w2 = word_util.random_2words_not_same_inarr(word_arr)
                        w1 = w1.lower()
                        file_new_name = pref + w1 + file_extension
                        file_name_no_extension_new = pref + w1

                        file_info.type = 'values'
                        file_info.file_name_no_extension_new = file_name_no_extension_new
                        file_info.name_new = file_new_name
                        file_new_path = os.path.join(root, file_new_name)
                        file_info.file_path_new = file_new_path
                        values_file_aar.append(file_info)
                        old_new_map_values[file_name_key] = file_new_name

                    file_new_path = os.path.join(root, file_new_name)
                    os.rename(file_info.file_path, file_new_path)


                if 'res/anim' in root:
                    if old_new_map_anim.has_key(file_name_key):
                        file_new_name = old_new_map_anim[file_name_key]
                    else:

                        w1, w2 = word_util.random_2words_not_same_inarr(word_arr)
                        w1 = w1.lower()
                        file_new_name = pref + w1 + file_extension
                        file_name_no_extension_new = pref + w1

                        file_info.type = 'anim'
                        file_info.file_name_no_extension_new = file_name_no_extension_new
                        file_info.name_new = file_new_name
                        file_new_path = os.path.join(root, file_new_name)
                        file_info.file_path_new = file_new_path
                        anim_file_aar.append(file_info)
                        old_new_map_anim[file_name_key] = file_new_name

                    file_new_path = os.path.join(root, file_new_name)
                    os.rename(file_info.file_path, file_new_path)


    print drawable_file_aar
    print layout_file_aar
    print mipmap_file_aar
    print values_file_aar
    print anim_file_aar
    res_dic = {'drawable': drawable_file_aar, 'layout': layout_file_aar, 'mipmap': mipmap_file_aar,
               'values': values_file_aar, 'anim': anim_file_aar}
    # return drawable_file_aar, layout_file_aar, mipmap_file_aar, values_file_aar, anim_file_aar
    return res_dic

def change_res_file_name(src_path, res_path):

    res_dic = rename_res_file(src_path)
    ids_aar = getIds(res_path)
    str_aar = getStringKey(res_path)
    color_aar = getColorKey(res_path)
    dimen_aar = getDimenKey(res_path)
    if res_dic:

        if os.path.exists(src_path):
            list_dirs = os.walk(src_path)
            for root, dirs, files in list_dirs:
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    file_data = file_util.read_file_data(file_path)

                    for item_key, item_value in res_dic.items():
                        for file_info in item_value:

                            file_name_no_extension_new = file_info.file_name_no_extension_new

                            file_data = re.sub(r'@%s/%s\b' % (file_info.type, file_info.file_name_no_extension),'@%s/%s' % (file_info.type, file_name_no_extension_new), file_data)
                            file_data = re.sub(r'R\.%s\.%s\b' % (file_info.type, file_info.file_name_no_extension),'R.%s.%s' % (file_info.type, file_name_no_extension_new), file_data)

                    # file_data = rename_id(file_data, ids_aar)
                    # file_data = rename_string(file_data, str_aar)
                    # file_data = rename_color(file_data, color_aar)
                    # file_data = rename_dimen(file_data, dimen_aar)

                    file_util.wite_data_to_file_noencode(file_path, file_data)

def change_id_tag_file_name(src_path, res_path):
    #修改id
    ids_aar = getIds(res_path)
    # 修改string key
    str_aar = getStringKey(res_path)
    color_aar = getColorKey(res_path)
    dimen_aar = getDimenKey(res_path)

    if os.path.exists(src_path):
        list_dirs = os.walk(src_path)
        for root, dirs, files in list_dirs:
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_data = file_util.read_file_data(file_path)

                # for item_key, item_value in res_dic.items():
                #     for file_info in item_value:
                #
                #         file_name_no_extension_new = file_info.file_name_no_extension_new
                #
                #         file_data = re.sub(r'@%s/%s\b' % (file_info.type, file_info.file_name_no_extension),'@%s/%s' % (file_info.type, file_name_no_extension_new), file_data)
                #         file_data = re.sub(r'R\.%s\.%s\b' % (file_info.type, file_info.file_name_no_extension),'R.%s.%s' % (file_info.type, file_name_no_extension_new), file_data)

                file_data = rename_id(file_data, ids_aar)
                file_data = rename_string(file_data, str_aar)
                file_data = rename_color(file_data, color_aar)
                file_data = rename_dimen(file_data, dimen_aar)

                file_util.wite_data_to_file_noencode(file_path, file_data)



string_old_new_dic = {}
id_old_new_dic = {}
color_old_new_dic = {}
dimen_old_new_dic = {}

def rename_id(file_data, ids_aar):
    id_tepm_aar = []
    for id_name in ids_aar:
        if id_old_new_dic.has_key(id_name):
            new_id = id_old_new_dic[id_name]
        else:
            w1,w2 = word_util.random_2words_not_same_inarr(id_tepm_aar)
            new_id = 'mId_' + w1.lower() + '_' + w2.lower()
            id_old_new_dic[id_name] = new_id

        file_data = re.sub(r'@id/%s\b' % id_name, '@id/%s' % new_id, file_data)
        file_data = re.sub(r'R\.id\.%s\b' % id_name, 'R.id.%s' % new_id, file_data)
        file_data = re.sub(r'android:id="@\+id/%s"' % id_name, 'android:id="@+id/%s"' % new_id, file_data)

    return file_data

def rename_string(file_data, str_aar):
    aaa2 = []
    for str_name in str_aar:
        if string_old_new_dic.has_key(str_name):
            new_tag = string_old_new_dic[str_name]
        else:
            w1,w2 = word_util.random_2words_not_same_inarr(aaa2)
            new_tag = 'mstr_' + w1.lower() + '_' + w2.lower()
            string_old_new_dic[str_name] = new_tag

        file_data = re.sub(r'@string/%s\b' % str_name, '@string/%s' % new_tag, file_data)
        file_data = re.sub(r'R\.string\.%s\b' % str_name, 'R.string.%s' % new_tag, file_data)
        file_data = re.sub(r'<string name="%s">' % str_name, '<string name="%s">' % new_tag, file_data)

    return file_data

def rename_color(file_data, color_aar):
    aaa3 = []
    for str_name in color_aar:
        if color_old_new_dic.has_key(str_name):
            new_tag = color_old_new_dic[str_name]
        else:
            w1, w2 = word_util.random_2words_not_same_inarr(aaa3)
            new_tag = 'mcolor_' + w1.lower() + '_' + w2.lower()
            color_old_new_dic[str_name] = new_tag

        file_data = re.sub(r'@color/%s\b' % str_name, '@color/%s' % new_tag, file_data)
        file_data = re.sub(r'R\.color\.%s\b' % str_name, 'R.color.%s' % new_tag, file_data)
        file_data = re.sub(r'<color name="%s">' % str_name, '<color name="%s">' % new_tag, file_data)

    return file_data

def rename_dimen(file_data, dimen_aar):
    aaa4 = []
    for str_name in dimen_aar:
        if dimen_old_new_dic.has_key(str_name):
            new_tag = dimen_old_new_dic[str_name]
        else:
            w1, w2 = word_util.random_2words_not_same_inarr(aaa4)
            new_tag = 'mdimen_' + w1.lower() + '_' + w2.lower()
            dimen_old_new_dic[str_name] = new_tag

        file_data = re.sub(r'@dimen/%s\b' % str_name, '@dimen/%s' % new_tag, file_data)
        file_data = re.sub(r'R\.dimen\.%s\b' % str_name, 'R.dimen.%s' % new_tag, file_data)
        file_data = re.sub(r'<dimen name="%s">' % str_name, '<dimen name="%s">' % new_tag, file_data)

    return file_data


if __name__ == '__main__':

    sdk_confuse_dir = '/Users/ganyuanrong/PycharmProjects/SdkTools/modifyXcodeProject/sdk_confuse/'
    woords_file_path = sdk_confuse_dir + 'confuse_words_2.log'
    genest_word = word_util.words_reader(woords_file_path)

    words_dong = word_util.words_reader(sdk_confuse_dir + 'word_dong.log')
    words_name = word_util.words_reader(sdk_confuse_dir + 'word_ming.log')
    word_util.words_name = words_name
    word_util.words_dong = words_dong
    word_util.genest_word = genest_word

    src_path = '/Users/ganyuanrong/AndroidProject/MWSDK/GamaSDK/src/'
    res_path = '/Users/ganyuanrong/AndroidProject/MWSDK/GamaSDK/src/'
    # getColorKey(src_path)
    # getDimenKey(src_path)
    # change_res_file_name(src_path, src_path)

    exclude_string = ['sdk_inner_version','scheme','facebook_app_id','facebook_client_token',
                      'facebook_authorities','fb_login_protocol_scheme','facebook_app_name','line_channelId','channel_platform','sdk_name']
    change_id_tag_file_name(src_path, src_path)

    print 'end'

