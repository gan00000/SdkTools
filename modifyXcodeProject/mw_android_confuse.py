#coding=utf-8
import base64
import imp
import string
import sys
import uuid

from Crypto.Cipher import AES

import md5util
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

def rename_res_file(src_dir_path, pref):
    drawable_file_aar = []
    layout_file_aar = []
    mipmap_file_aar = []
    # values_file_aar = []
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


                file_info.file_extension = file_extension

                if '.9' in file_name_no_extension:
                    file_info.file_name_no_extension = file_name_no_extension.replace('.9', '')
                    print 'is .9'
                else:
                    file_info.file_name_no_extension = file_name_no_extension

                # pref = 'cal_'

                if 'res/drawable' in root:

                    if old_new_map_drawable.has_key(file_name_key):
                        file_new_name = old_new_map_drawable[file_name_key]
                    else:

                        w1, w2 = word_util.random_2words_not_same_inarr(word_arr)
                        w1 = w1.lower()

                        file_name_no_extension_new = pref + w1

                        if file_name_no_extension.endswith('.9'):
                            file_new_name = file_name_no_extension_new + '.9' + file_extension
                        else:
                            file_new_name = file_name_no_extension_new + file_extension

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


                # if 'res/values' in root:
                #
                #     if old_new_map_values.has_key(file_name_key):
                #         file_new_name = old_new_map_values[file_name_key]
                #     else:
                #
                #         w1, w2 = word_util.random_2words_not_same_inarr(word_arr)
                #         w1 = w1.lower()
                #         file_new_name = pref + w1 + file_extension
                #         file_name_no_extension_new = pref + w1
                #
                #         file_info.type = 'values'
                #         file_info.file_name_no_extension_new = file_name_no_extension_new
                #         file_info.name_new = file_new_name
                #         file_new_path = os.path.join(root, file_new_name)
                #         file_info.file_path_new = file_new_path
                #         values_file_aar.append(file_info)
                #         old_new_map_values[file_name_key] = file_new_name
                #
                #     file_new_path = os.path.join(root, file_new_name)
                #     os.rename(file_info.file_path, file_new_path)


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


    # print drawable_file_aar
    # print layout_file_aar
    # print mipmap_file_aar
    # print values_file_aar
    # print anim_file_aar
    log_info('drawable', drawable_file_aar)
    log_info('layout', layout_file_aar)
    log_info('mipmap', mipmap_file_aar)
    log_info('anim', anim_file_aar)
    res_dic = {'drawable': drawable_file_aar, 'layout': layout_file_aar, 'mipmap': mipmap_file_aar,
                'anim': anim_file_aar}
    # return drawable_file_aar, layout_file_aar, mipmap_file_aar, values_file_aar, anim_file_aar
    return res_dic

def log_info(type, infos):
    for info in infos:
        print 'type:%s, name=%s, new_name=%s' % (type, info.name, info.name_new)

def change_res_file_name(src_path, res_path, pref=""):

    res_dic = rename_res_file(src_path, pref)
    # ids_aar = getIds(res_path)
    # str_aar = getStringKey(res_path)
    # color_aar = getColorKey(res_path)
    # dimen_aar = getDimenKey(res_path)
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

    #todo change stype

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

def remove_unuse_resource(src_path, res_path):
    #修改id
    # ids_aar = getIds(res_path)
    # 修改string key
    str_aar = getStringKey(res_path)
    color_aar = getColorKey(res_path)
    dimen_aar = getDimenKey(res_path)#@color

    #todo change stype

    no_use_str = []
    no_use_color = []
    no_use_dimen = []

    for xml_tag_name in str_aar:
        is_use = check_res_tag_use(src_path, 'string', xml_tag_name)
        if is_use is False:
            print 'no user res tag:' + xml_tag_name
            # no_use_str.append(xml_tag_name)
            del_res_tag(src_path, 'string', xml_tag_name)

    for xml_tag_name in color_aar:

        is_use = check_res_tag_use(src_path, 'color', xml_tag_name)
        if is_use is False:
            print 'no user res tag:' + xml_tag_name
            # no_use_color.append(xml_tag_name)
            del_res_tag(src_path, 'color', xml_tag_name)
    for xml_tag_name in dimen_aar:
        is_use = check_res_tag_use(src_path, 'dimen', xml_tag_name)
        if is_use is False:
            print 'no user res tag:' + xml_tag_name
            # no_use_dimen.append(xml_tag_name)
            del_res_tag(src_path, 'dimen', xml_tag_name)



def check_res_tag_use(src_path, res_type, res_name):#检查资源是否有引用

    if os.path.exists(src_path):
        list_dirs = os.walk(src_path)
        for root, dirs, files in list_dirs:
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_data = file_util.read_file_data(file_path)

                if file_name.endswith('.java'):
                    file_data = oc_code_util.removeAnnotate(file_data)

                # if 'manageriseiedd_acceptencyyzjf' == xml_tag_name:
                #     pass
                # if 'PullToRefreshRecyclerView' in file_name and 'manageriseiedd_acceptencyyzjf' == res_name:
                #     pass

                res_ref_arr = re.findall(r'@%s/%s\b' % (res_type, res_name), file_data)  #color="@color/localaclenutf_smileeebd" >
                if res_ref_arr and len(res_ref_arr) > 0:
                    return True
                res_ref_arr = re.findall(r'R\.%s\.%s\b' % (res_type, res_name), file_data)  #R.color.manageriseiedd_acceptencyyzjf
                if res_ref_arr and len(res_ref_arr) > 0:
                    return True

    return False

def del_res_tag(src_path, res_type, res_name):#检查资源是否有引用

    if os.path.exists(src_path):
        list_dirs = os.walk(src_path)
        for root, dirs, files in list_dirs:
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_data = file_util.read_file_data(file_path)

                # file_data = re.sub('<!--.*-->', '', file_data)
                # '<string name="api_pay_web_payment">api/web/payment.page</string>'
                tag_obj = re.findall(r'<%s name="%s">.*</%s>' % (res_type, res_name, res_type), file_data)
                if tag_obj and len(tag_obj) > 0:
                    file_data = re.sub(r'<%s name="%s">.*</%s>' % (res_type, res_name, res_type), '',  file_data)
                    file_util.wite_data_to_file_noencode(file_path, file_data)


def rename_id(file_data, ids_aar):
    id_tepm_aar = []
    for id_name in ids_aar:
        if id_old_new_dic.has_key(id_name):
            new_id = id_old_new_dic[id_name]
        else:
            w1,w2 = word_util.random_2words_not_same_inarr(id_tepm_aar)
            new_id = w1.lower() + '_' + w2.lower()
            id_old_new_dic[id_name] = new_id
            print 'id_old=%s,id_new=%s' % (id_name, new_id)

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
            new_tag =  w1.lower() + '_' + w2.lower()
            string_old_new_dic[str_name] = new_tag
            print 'string_old=%s,string_new=%s' % (str_name, new_tag)

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
            new_tag =  w1.lower() + '_' + w2.lower()
            color_old_new_dic[str_name] = new_tag
            print 'color_old=%s,color_new=%s' % (str_name, new_tag)

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
            # new_tag = 'mdimen_' + w1.lower() + '_' + w2.lower()
            new_tag = w1.lower() + '_' + w2.lower()
            dimen_old_new_dic[str_name] = new_tag
            print 'dimen_old=%s,dimen_new=%s' % (str_name, new_tag)

        file_data = re.sub(r'@dimen/%s\b' % str_name, '@dimen/%s' % new_tag, file_data)
        file_data = re.sub(r'R\.dimen\.%s\b' % str_name, 'R.dimen.%s' % new_tag, file_data)
        file_data = re.sub(r'<dimen name="%s">' % str_name, '<dimen name="%s">' % new_tag, file_data)

    return file_data

def find_R_in_code(src_path):
    #修改id
    # ids_aar = getIds(res_path)
    # # 修改string key
    # str_aar = getStringKey(res_path)
    # color_aar = getColorKey(res_path)
    # dimen_aar = getDimenKey(res_path)

    # r_layout_aar = []
    # r_layout_stem = []
    #
    # r_id_aar = []
    # r_id_stem = []
    #
    # r_string_aar = []
    # r_string_stem = []
    #
    # r_color_aar = []
    # r_color_stem = []

    R_statem_list = []


    if os.path.exists(src_path):
        list_dirs = os.walk(src_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if not file_name.endswith('.java') and root.endswith('myr'):
                    continue

                file_path = os.path.join(root, file_name)
                file_data = file_util.read_file_data(file_path)
                file_data = oc_code_util.removeAnnotate(file_data)
                has_change = 0

                # layout
                layout_list = re.findall(r'[^android\.]R.layout.\w+\b', file_data)
                if layout_list and len(layout_list) > 0:
                    has_change = 1
                    file_data = replce_R_xxx(file_data, layout_list, 'RLayout')
                # id
                id_list = re.findall(r'[^android\.]R.id.\w+\b', file_data)
                if id_list and len(id_list) > 0:
                    has_change = 1
                    file_data = replce_R_xxx(file_data, id_list, 'RId')

                # string
                string_list = re.findall(r'[^android\.]R.string.\w+\b', file_data)
                if string_list and len(string_list) > 0:
                    has_change = 1
                    file_data = replce_R_xxx(file_data, string_list,  'RString')

                # color
                color_list = re.findall(r'[^android\.]R.color.\w+\b', file_data)
                if color_list and len(color_list) > 0:
                    has_change = 1
                    file_data = replce_R_xxx(file_data, color_list, 'RColor')

                # dimen
                dimen_list = re.findall(r'[^android\.]R.dimen.\w+\b', file_data)
                if dimen_list and len(dimen_list) > 0:
                    has_change = 1
                    file_data = replce_R_xxx(file_data, dimen_list, 'RDimen')

                # drawable
                drawable_list = re.findall(r'[^android\.]R.drawable.\w+\b', file_data)
                if drawable_list and len(drawable_list) > 0:
                    has_change = 1
                    file_data = replce_R_xxx(file_data, drawable_list, 'RDrawable')

                # mipmap
                mipmap_list = re.findall(r'[^android\.]R.mipmap.\w+\b', file_data)
                if mipmap_list and len(mipmap_list) > 0:
                    has_change = 1
                    file_data = replce_R_xxx(file_data, mipmap_list, 'RMipmap')

                if has_change == 1:
                    file_util.wite_data_to_file_noencode(file_path, file_data)


def replce_R_xxx(file_data, xxx_list, class_name):

    if xxx_list and len(xxx_list) > 0:

        r_xxx_stem_list = []
        r_xxx_aar = []
        for id in xxx_list:

            id_new = id.replace('.', '_').replace('R_', '%s.' % class_name)
            file_data = re.sub(r'%s\b' % id, id_new, file_data)

            if id not in r_xxx_aar:
                new_def = id_new.replace('%s.' % class_name, '')
                stem = 'public static final int %s = %s;' % (new_def, id)
                r_xxx_aar.append(id)
                r_xxx_stem_list.append(stem)

        import_list = re.findall(r'import com\..+;', file_data)
        if import_list:
            last_import = import_list[len(import_list) - 1]
            last_import_add = last_import + '\n' + ('import com.mw.myr.%s;\n' % class_name)
            file_data = file_data.replace(last_import, last_import_add)

        print '=========start=========='
        for stem in r_xxx_stem_list:
            print stem
        print '=========end=========='

    return file_data

def insert_res_string(res_path, pref=""):

    if os.path.exists(res_path):
        list_dirs = os.walk(res_path)
        words_arr = []
        for root, dirs, files in list_dirs:

            if root.endswith('values'):

                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    str_lines = file_util.read_file_data_for_line(file_path)
                    file_content = ''
                    for str_line in str_lines:
                        file_content = file_content + str_line
                        if '<string' in str_line and '</string>' in str_line:
                            insert_count = random.randint(1, 4)
                            insert_content = ''
                            for xm in range(insert_count):
                                w1, w2 = word_util.random_2words_not_same_inarr(words_arr)
                                temmp_str = '\n\t<string name="%s">%s</string>' % (w1, w2)
                                insert_content = insert_content + temmp_str
                            file_content = file_content + insert_content + '\n'

                    file_util.wite_data_to_file_noencode(file_path, file_content)

def get_dit_md5(res_path, pref=""):

    file_md5s = []
    md5_name_dic = {}
    if os.path.exists(res_path):
        list_dirs = os.walk(res_path)
        for root, dirs, files in list_dirs:
            for file_name in files:
                file_path = os.path.join(root, file_name)
                s_md5 = md5util.md5sum(file_path)
                file_md5s.append(s_md5)
                md5_name_dic[s_md5] = file_path
    return file_md5s, md5_name_dic

def check_md5(path1, path2):
    md51s, md5_name_dic_1 = get_dit_md5(path1)
    md52s , md5_name_dic_2 = get_dit_md5(path2)
    same_md5 = []
    for mm1, name1 in md5_name_dic_1.items():
        for mm2, name2 in md5_name_dic_2.items():
            if mm1 == mm2:
                same_md5.append(name1)
                print 'same1 = %s, same2 = %s' % (name1, name2)

    print 'dir1 count = %s, with dir2 same count = %s' % (str(len(md51s)), str(len(same_md5)))



def addLajiFile():#添加垃圾文件到目录

    src_dir_path = '/Users/ganyuanrong/wbgame/lajifile'
    # src_dir_path = '/Users/ganyuanrong/ldysdk/kofts/src'
    # src_dir_path = '/Users/ganyuanrong/ldysdk/kofts/'
    # src_dir_path = '/Users/ganyuanrong/ldysdk/kofts/aaad/kdkka'
    if os.path.exists(src_dir_path):
        list_dirs = os.walk(src_dir_path)
        for root, dirs, files in list_dirs:

            for dir_name in dirs:
                if '.framework' in root or '.bundle' in root:
                    continue

                # if 'game_fanisa_' not in root:
                #     continue

                file_dir = os.path.join(root, dir_name)  # 头文件路径
                mPrpCrypt = PrpCrypt('KEY_KDAMOON88bb', 'IV_KDAMOON88bb')
                lett_src = string.letters
                lett_src = lett_src + '012dddd3456789'

                letter_count = random.randint(10, 50)
                for i in range(letter_count):
                    msg = ''
                    letter_count = random.randint(20, 800)
                    for m in range(letter_count):
                        lett = lett_src[random.randint(0, len(lett_src) - 1)]
                        msg = msg + lett
                    aaresult = mPrpCrypt.aes_encrypt_base64(msg)
                    file_name = md5util.md5hex(aaresult)
                    file_util.wite_data_to_file(os.path.join(file_dir, file_name), aaresult)

def jiamiIOSFile():

    # src_dir_path = '/Users/ganyuanrong/ldysdk/kofts-aaaraw/res/raw-assets/resources/sound'
    # new_directory11 = '/Users/ganyuanrong/ldysdk/kofts_jiami_sound'

    src_dir_path = '/Users/ganyuanrong/ldysdk/kofts-aaaraw/src'
    new_directory = '/Users/ganyuanrong/ldysdk/kofts_jiami'

    if os.path.exists(src_dir_path):
        list_dirs = os.walk(src_dir_path)
        for root, dirs, files in list_dirs:

            for file_name in files:
                if '.framework' in root or '.bundle' in root:
                    continue

                if '.DS_Store' == file_name:
                    continue

                file_path = os.path.join(root, file_name)  # 头文件路径
                file_data = file_util.read_file_data(file_path)

                # file_name_new = md5util.md5hex("UUYYAOODXX88A" + file_name)
                file_name_new = md5util.md5hex("KKDAMOONMOON888AA" + file_name)


                # new_directory = root.replace('/Users/ganyuanrong/ldysdk/kofts-aaaraw/res/raw-assets/resources/sound', new_directory11)
                # 检查目录是否存在
                if not os.path.exists(new_directory):
                    # 不存在则创建目录
                    os.makedirs(new_directory)

                file_path_new = os.path.join(new_directory, file_name_new)


                mPrpCrypt = PrpCrypt('KEY_KDAMOON88AA', 'IV_KDAMOON88AA')
                # en_data = mPrpCrypt.aes_encrypt(file_data)
                en_data = mPrpCrypt.encrypt_for_data(file_data)

                file_util.wite_data_to_file_noencode(file_path_new, en_data)


def change_aaa(arc_path):
    # "/v1/system/init";
    if os.path.exists(arc_path):
        str_lines = file_util.read_file_data_for_line(arc_path)
        content_a = ''
        for str_line in str_lines:

            if '/v1/' not in str_line:
                content_a = content_a + str_line
                continue
            w1 = word_util.random_word_dong()
            w2 = word_util.random_word_name()
            new_w = w1 + '_' + w2
            result = re.findall(r'"/v1/(.+)";', str_line)
            if result:
                aa = result[0]
                str_line = str_line.replace(aa, new_w)
                str_line = str_line.replace(';', ';   //  /v1/%s' % aa)
                content_a = content_a + str_line

            else:
                content_a = content_a + str_line
        file_util.wite_data_to_file(arc_path, content_a)

if __name__ == '__main__':

    sdk_confuse_dir = '/Users/ganyuanrong/PycharmProjects/SdkTools/modifyXcodeProject/sdk_confuse/'
    woords_file_path = sdk_confuse_dir + 'confuse_words_2.log'
    genest_word = word_util.words_reader(woords_file_path)

    words_dong = word_util.words_reader(sdk_confuse_dir + 'word_dong.log')
    words_name = word_util.words_reader(sdk_confuse_dir + 'word_ming.log')
    word_util.words_name = words_name
    word_util.words_dong = words_dong
    word_util.genest_word = genest_word

    # src_path = '/Users/ganyuanrong/AndroidProject/martial_gp2_sdk_code/quickgamesdk/src/main'
    # res_path = '/Users/ganyuanrong/AndroidProject/martial_gp2_sdk_code/quickgamesdk/src/main/res'

    # src_path = '/Users/ganyuanrong/AndroidProject/DYSDK/SDKModuleOBS1/src'
    # res_path = '/Users/ganyuanrong/AndroidProject/DYSDK/SDKModuleOBS1/src'
    src_path = '/Users/ganyuanrong/AndroidProject/martial_gp2_sdk_code/quickgamesdk/src'
    res_path = '/Users/ganyuanrong/AndroidProject/martial_gp2_sdk_code/quickgamesdk/src'

    exclude_string = ['reg_is_need_vfcode','sdk_supported_languages','dy_topon_test','dy_admob_app_id','dy_ad_placement_ids','dy_topon_appkey','dy_topon_appid','dy_adjust_token','sdk_game_code','sdk_app_key','sdk_more_language','sdk_af_dev_key','sdk_default_server_language',
                      'default_web_client_id','sdk_inner_version','scheme','facebook_app_id','facebook_client_token',
                      'facebook_authorities','fb_login_protocol_scheme','facebook_app_name','line_channelId','channel_platform','sdk_name']

    # 0.移除不用的资源
    # remove_unuse_resource(src_path, res_path)

    # 1.修改res下面的文件名字
    # change_res_file_name(src_path, src_path, "kkayumm_")

    #2.修改资源 id值
    # change_id_tag_file_name(src_path, res_path)

    # 3.添加无效string tag
    # insert_res_string(res_path)

    # find_R_in_code(src_path)

    # alla = []
    # for i in range(10000):
    #     msg = ''
    #     letter_count = random.randint(3, 8)
    #     for m in range(letter_count):
    #         lett = string.letters[random.randint(0, len(string.letters) - 1)]
    #         msg = msg + lett
    #     # msg = 'tw' + msg.lower()
    #     msg = msg.lower()
    #
    #     addd = string.letters[random.randint(0, len(string.letters) - 1)]
    #     number = random.randint(0, 99999)
    #     # for i in range(number):
    #     #     msg = msg + '0'
    #     msg = msg + str(number) + addd
    #     if msg not in alla:
    #         alla.append(msg)
    #         print msg

    # check_md5('/Users/ganyuanrong/AndroidProject/martial_gp2_sdk_code/demo/build/outputs/bundle/payGooglePlayRelease/demo-payGooglePlay-release', '/Users/ganyuanrong/Downloads/cc/')
    # jiamiIOSFile()
    # addLajiFile()

    # change_aaa('/Users/ganyuanrong/AndroidProject/martial_gp2_sdk_code/quickgamesdk/src/main/java/com/apter/sdk/http/HttpConstant.java')

    print 'end'

