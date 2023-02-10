#coding=utf-8
import imp
import sys
# imp.reload(sys)
# sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的

import os
import re

import chardet

# 导入 random(随机数) 模块
import random

from modifyXcodeProject.utils.PrpCrypt import PrpCrypt

xcode_project_path = '/Users/gan/Desktop/黑特篮球new2/XXXHeiTaiPro.xcodeproj'

#res
modify_res_path = '/Users/gan/Desktop/黑特篮球new2/SkyBetufi/SourceCode/SkySrc'
image_old_prefix = 'desww'
image_new_prefix = 'hyes'  #PPlay

modify_xcassets_src_path = '/Users/gan/Desktop/黑特篮球new2/SkyBetufi/SourceCode/SkySrc/'
modify_xcassets_path = '/Users/gan/Desktop/黑特篮球new2/SkyBetufi/SourceCode/'
xcassets_old_prefix = 'Plove'
xcassets_new_prefix = 'gurk_'  #PPlay

#图片排除
image_exclude_files = []

# csb中直接引用文件名
image_in_csb_direct = []

ResConfig_path = '/Users/gan/iospro/game/rongyaodg/app/res/ResConfig.xml'

# cpp

#battle ForeverBattleSky, ui  PPForeverSky

cpp_all_path = ''
cpp_modify_path = ''
# cpp_modify_path = '/Users/gan/iospro/game/rongyaodg/app/Classes/game/model/template'  KKForeverSkyRun
cpp_old_prefix = ''
cpp_new_prefix = ''

# /Users/gan/Desktop/黑特篮球new2/SkyBetufi/SourceCode/SkySrc/CommonModule/GUtility/PKCategory
oc_all_path = '/Users/gan/Desktop/黑特篮球new2/SkyBetufi/SourceCode/'
oc_modify_path = '/Users/gan/Desktop/黑特篮球new2/SkyBetufi/SourceCode/SkySrc/'
# oc_modify_path = '/Users/gan/Desktop/黑特篮球new2/SkyBetufi/SourceCode/SkySrc/CommonModule/GUtility/PKCategory'
oc_old_prefix = ''
oc_new_prefix = ''

oc_old_prefix_reps = ["GlodBule","SkyBallHetiRed","KPLove", "MMToday", "YYPackage", "CCCase", "NDesk", "Sunday", "Hourse",
                      "PXFun", "KMonkey", "GGCat", "RRDog"]
oc_new_prefix_reps = ["Cfipy", "YeYee", "MMoog", "UUaks", "NSNice", "Blysa", "TuTuos",
                      "KSasx", "FFlali", "BByas", "WSKgg"]



handle_file_count = 0
file_count = 0


#specially

cpp_exclude_files = []


oc_exclude_files = ['AppDelegate.h', 'SkyBallPlay.pch']
oc_exclude_dirs = ['AppDelegate.h', 'SkyBallPlay.pch']

#修改cpp类名(文件名)
def modify_cpp_class_name(cpp_path):
    global file_count, handle_file_count

    # need_file_data = read_file_data('/Users/gan/Downloads/app/Classes_ios/calss_modify.h')
    #
    # if not need_file_data:
    #     return

    project_content_path = os.path.join(xcode_project_path, 'project.pbxproj')
    project_content = read_file_data(project_content_path)

    if os.path.exists(cpp_path):
        list_dirs = os.walk(cpp_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                file_count = file_count + 1


                # ======测试排除 start========

                # if '/ui' in root or '/template' in root:
                #     continue

                # ======测试排除 end========

                if file_name.endswith('.cpp'):#cpp文件


                    # ======测试排除 start========

                    if file_name == "ConfBoxPosition.cpp":
                        continue

                    # ======测试排除 end========

                    if cpp_new_prefix and file_name.startswith(cpp_new_prefix): #已经存在前缀，不处理
                        continue

                    if cpp_old_prefix and not file_name.startswith(cpp_old_prefix):#
                        continue

                    file_name_no_extension = os.path.splitext(file_name)[0]
                    file_extension = os.path.splitext(file_name)[1]



                    header_file_name = file_name_no_extension + '.h'  #cpp对应的头文件名称
                    # if header_file_name in cpp_exclude_files: #与lua相关，排除
                    #     continue
                    #
                    # if file_name_no_extension.endswith('Unit'):  # ======测试排除 end========
                    #     continue

                    header_file_path = os.path.join(root, header_file_name)   #头文件路径
                    if os.path.exists(header_file_path):

                        print '正在处理文件：' + file_name
                        file_new_name = get_new_file_name(file_name, cpp_old_prefix, cpp_new_prefix) #新文件名字

                        file_old_path = os.path.join(root, file_name)
                        file_new_path = os.path.join(root, file_new_name)

                        try:
                            os.rename(file_old_path, file_new_path)  #更改文件名
                        except:
                            print '文件无法更改名称：' + file_old_path
                            continue


                        try:

                            header_file_new_name = get_new_file_name(header_file_name, cpp_old_prefix,
                                                                     cpp_new_prefix)  # 新头文件名字
                            header_file_new_path = os.path.join(root, header_file_new_name)

                            os.rename(header_file_path, header_file_new_path)  # 更改头文件名

                        except:
                            print '文件无法更改名称：' + header_file_path
                            continue


                        file_new_name_no_extension = os.path.splitext(file_new_name)[0]
                        # 更改引用改文件类的内容
                        modify_cpp_class_reference(cpp_all_path, file_name_no_extension, file_new_name_no_extension)

                        # 更改xproject文件
                        project_content = replace_xproject_data_reference(project_content, file_name, file_new_name) #更改源文件xproject名称
                        project_content = replace_xproject_data_reference(project_content, header_file_name, header_file_new_name)#更改头文件xproject名称

                        handle_file_count = handle_file_count + 1
                        print '处理完成' + file_name #对应的头文件不存在不处理

        wite_data_to_file(project_content_path, project_content)
        print '修改完成 file_count:' + str(file_count) + "  handle_file_count:" + str(handle_file_count)

def delete_cpp_class_prefex(cpp_path):
    global file_count, handle_file_count

    # need_file_data = read_file_data('/Users/gan/Downloads/app/Classes_ios/calss_modify.h')
    #
    # if not need_file_data:
    #     return

    project_content_path = os.path.join(xcode_project_path, 'project.pbxproj')
    project_content = read_file_data(project_content_path)


    aaa = ['SSHowAreKillBaseTabsUIModule.cpp', 'SSHowAreKillAreaRect.cpp']

    cpp_new_prefix = ""

    if not cpp_old_prefix:
        return

    if os.path.exists(cpp_path):
        list_dirs = os.walk(cpp_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                file_count = file_count + 1



                if file_name.endswith('.cpp'):#cpp文件

                    if not file_name in aaa:
                        print 'not ==='
                        continue

                    if not file_name.startswith(cpp_old_prefix):#
                        print 'not file_name.startswith(cpp_old_prefix)'
                        continue

                    file_name_no_extension = os.path.splitext(file_name)[0]
                    file_extension = os.path.splitext(file_name)[1]


                    header_file_name = file_name_no_extension + '.h'  #cpp对应的头文件名称

                    header_file_path = os.path.join(root, header_file_name)   #头文件路径
                    if os.path.exists(header_file_path):

                        print '正在处理文件：' + file_name
                        file_new_name = get_new_file_name(file_name, cpp_old_prefix, cpp_new_prefix) #新文件名字

                        file_old_path = os.path.join(root, file_name)
                        file_new_path = os.path.join(root, file_new_name)

                        try:
                            os.rename(file_old_path, file_new_path)  #更改文件名
                        except:
                            print '文件无法更改名称：' + file_old_path
                            continue


                        try:

                            header_file_new_name = get_new_file_name(header_file_name, cpp_old_prefix,
                                                                     cpp_new_prefix)  # 新头文件名字
                            header_file_new_path = os.path.join(root, header_file_new_name)

                            os.rename(header_file_path, header_file_new_path)  # 更改头文件名

                        except:
                            print '文件无法更改名称：' + header_file_path
                            continue


                        file_new_name_no_extension = os.path.splitext(file_new_name)[0]
                        # 更改引用改文件类的内容
                        modify_cpp_class_reference(cpp_all_path, file_name_no_extension, file_new_name_no_extension)

                        # 更改xproject文件
                        project_content = replace_xproject_data_reference(project_content, file_name, file_new_name) #更改源文件xproject名称
                        project_content = replace_xproject_data_reference(project_content, header_file_name, header_file_new_name)#更改头文件xproject名称

                        handle_file_count = handle_file_count + 1
                        print '处理完成' + file_name #对应的头文件不存在不处理

        wite_data_to_file(project_content_path, project_content)
        print '修改完成 file_count:' + str(file_count) + "  handle_file_count:" + str(handle_file_count)


def modify_cpp_class_reference(cpp_path, old_ref, new_ref):

    if os.path.exists(cpp_path):
        list_dirs = os.walk(cpp_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if file_name.endswith('.cpp') or file_name.endswith('.h'):#cpp文件

                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)

                    if have_the_word_in_data(file_data, old_ref):

                        file_new_data = replace_data_by_word(file_data, old_ref, new_ref)
                        wite_data_to_file(file_path, file_new_data)


def modify_oc_class_name(oc_path):
    global file_count, handle_file_count

    project_content_path = os.path.join(xcode_project_path, 'project.pbxproj')
    project_content = read_file_data(project_content_path)

    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store" or file_name.endswith(".swift"):
                    continue

                file_count = file_count + 1

                if 'Masonry' in root:
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm'):#cpp文件

                    if has_new_prefix_in_start(file_name):
                        continue
                    # if oc_new_prefix and file_name.startswith(oc_new_prefix): #已经存在前缀，不处理
                    #     continue

                    if '+' in file_name and has_new_prefix_in_filename(file_name): #分类
                       continue

                    file_name_no_extension = os.path.splitext(file_name)[0]
                    file_extension = os.path.splitext(file_name)[1]

                    header_file_name = file_name_no_extension + '.h'  #cpp对应的头文件名称
                    if header_file_name in oc_exclude_files: #特殊排除
                        continue

                    oc_old_prefix = has_old_prefix_in_start(file_name)

                    if len(oc_new_prefix_reps) < 1:
                        oc_new_prefix = ""
                    else:

                        prefix_index = random.randint(0, len(oc_new_prefix_reps) - 1)
                        oc_new_prefix = oc_new_prefix_reps[prefix_index]

                    if not oc_new_prefix and not oc_old_prefix:  # 此种情况为删除前缀
                        continue

                    if not oc_old_prefix:
                        oc_old_prefix = ""

                    header_file_path = os.path.join(root, header_file_name)   #头文件路径
                    if os.path.exists(header_file_path):

                        print '正在处理文件：' + file_name
                        file_new_name = get_new_file_name_for_oc(file_name, oc_old_prefix, oc_new_prefix) #新文件名字

                        file_old_path = os.path.join(root, file_name)
                        file_new_path = os.path.join(root, file_new_name)

                        try:
                            os.rename(file_old_path, file_new_path)  #更改文件名
                        except:
                            print '文件无法更改名称：' + file_old_path
                            continue


                        try:

                            header_file_new_name = get_new_file_name_for_oc(header_file_name, oc_old_prefix,
                                                                     oc_new_prefix)  # 新头文件名字
                            header_file_new_path = os.path.join(root, header_file_new_name)

                            os.rename(header_file_path, header_file_new_path)  # 更改头文件名

                            # xib处理
                            xib_file_name = file_name_no_extension + '.xib'
                            xib_file_path = os.path.join(root, xib_file_name)
                            if os.path.exists(xib_file_path):
                                xib_file_name_new = get_new_file_name_for_oc(xib_file_name, oc_old_prefix,oc_new_prefix)
                                xib_file_new_path = os.path.join(root, xib_file_name_new)
                                os.rename(xib_file_path, xib_file_new_path)  # 更改xib文件名
                                # 更改xproject文件中的.storyboard
                                project_content = replace_xproject_data_reference(project_content, xib_file_name,
                                                                                  xib_file_name_new)

                            # storyboard处理
                            storyboard_file_name = file_name_no_extension + '.storyboard'
                            storyboard_file_path = os.path.join(root, storyboard_file_name)
                            if os.path.exists(storyboard_file_path):
                                storyboard_file_name_new = get_new_file_name_for_oc(storyboard_file_name, oc_old_prefix,
                                                                             oc_new_prefix)
                                storyboard_file_new_path = os.path.join(root, storyboard_file_name_new)
                                os.rename(storyboard_file_path, storyboard_file_new_path)  # 更改storyboard文件名

                                # 更改xproject文件中的.storyboard
                                project_content = replace_xproject_data_reference(project_content, storyboard_file_name,
                                                                                  storyboard_file_name_new)


                        except:
                            print '文件无法更改名称：' + header_file_path
                            continue


                        file_new_name_no_extension = os.path.splitext(file_new_name)[0]
                        modify_oc_class_reference(oc_all_path, file_name_no_extension, file_new_name_no_extension)

                        # 更改xproject文件中的.m
                        project_content = replace_xproject_data_reference(project_content, file_name, file_new_name)

                        # 更改xproject文件中的.h
                        project_content = replace_xproject_data_reference(project_content, header_file_name, header_file_new_name)

                        handle_file_count = handle_file_count + 1
                        print '处理完成' + file_name

        wite_data_to_file(project_content_path, project_content)
        print '修改完成 file_count:' + str(file_count) + "  handle_file_count:" + str(handle_file_count)


#oc_path 所有源文件，置于一个单独目录最好
def modify_oc_class_reference(oc_path, old_ref, new_ref):

    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm') \
                        or file_name.endswith('.h') or file_name.endswith('.pch') or \
                    file_name.endswith('.storyboard') or file_name.endswith('.xib'):    #oc文件

                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)

                    # if have_the_word_in_data(file_data, old_ref):

                    file_new_data = replace_data_by_word(file_data, old_ref, new_ref)
                    if (file_name.endswith('.m') or file_name.endswith('.h')) and new_ref in file_name and '+' in old_ref and '+' in new_ref: #分类
                        old_ref_categery = old_ref.split('+')[1]
                        new_ref_categery = new_ref.split('+')[1]
                        file_new_data = file_new_data.replace('(' + old_ref_categery + ')', '(' + new_ref_categery + ')')
                    wite_data_to_file(file_path, file_new_data)

def modify_storyboard_reference(oc_path, old_ref, new_ref):

    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm'):    #oc文件

                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)

                    # if have_the_word_in_data(file_data, old_ref):
                    file_new_data = file_data.replace(old_ref, new_ref)

                    # file_new_data = replace_data_by_word(file_data, old_ref, new_ref)
                    wite_data_to_file(file_path, file_new_data)

def rename_imageset_file_name(res_path):

    if os.path.exists(res_path):
        list_dirs = os.walk(res_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue
                if file_name == 'Contents.json':
                    contents_json_name = file_name
                    if root.endswith('.imageset') or root.endswith('.appiconset') or root.endswith('.launchimage'):
                        files2 = os.listdir(root)
                        contents_json_path = os.path.join(root, contents_json_name)
                        contents_json_file_contents = read_file_data(contents_json_path)
                        a = 0
                        for f2 in files2:
                            if f2.endswith('.png') or f2.endswith('.jpg'):
                                print 'f2=' + f2
                                if f2.startswith(image_new_prefix):  # 已经存在前缀，不处理
                                    continue
                                if f2 in image_exclude_files:
                                    print '排除修改的图片:' + f2
                                    continue
                                new_image_name = get_new_file_name(f2, image_old_prefix, image_new_prefix)
                                file_path_old = os.path.join(root, f2)
                                file_path_new = os.path.join(root, new_image_name)
                                os.rename(file_path_old, file_path_new)
                                contents_json_file_contents = replace_image_data(contents_json_file_contents, f2, new_image_name)
                                a = 1
                                print '完成修改:' + f2

                        if a == 1:
                            wite_data_to_file(contents_json_path, contents_json_file_contents)

        print '修改imageset文件完成'
    else:

        print 'res path不存在'


def rename_imageset_dir_name(res_path):

    if os.path.exists(res_path):
        project_content_path = os.path.join(xcode_project_path, 'project.pbxproj')
        project_content = read_file_data(project_content_path)
        list_dirs = os.walk(res_path)
        for root, dirs, files in list_dirs:
            for dir in dirs:

                if dir.endswith('.imageset'): #icon_film_unlike.imageset

                    if xcassets_new_prefix in dir:
                        continue

                    xcassets_dir_path_old = os.path.join(root, dir)
                    new_dir_name = get_new_file_name(dir, xcassets_old_prefix, xcassets_new_prefix)
                    xcassets_dir_path_new = os.path.join(root, new_dir_name)
                    os.rename(xcassets_dir_path_old, xcassets_dir_path_new)

                    old_ref = dir.replace('.imageset', '')
                    new_ref = new_dir_name.replace('.imageset', '')
                    modify_imageset_name_reference(modify_xcassets_path, old_ref, new_ref)
                    # 更改xproject文件中的引用
                    # project_content = replace_xproject_data_reference(project_content, dir, new_dir_name)

        # wite_data_to_file(project_content_path, project_content)


def modify_imageset_name_reference(oc_path, old_ref, new_ref):

    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm') \
                        or file_name.endswith('.h') or file_name.endswith('.pch') or \
                    file_name.endswith('.storyboard') or file_name.endswith('.xib'):    #oc文件

                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)

                    if file_name.endswith('.m') or file_name.endswith('.mm') \
                            or file_name.endswith('.h') or file_name.endswith('.pch'):
                        # imageNamed:@"icon_add_collection"
                        old_ref_b = '@"%s"' % old_ref
                        new_ref_b = '@"%s"' % new_ref
                        file_new_data = file_data.replace(old_ref_b, new_ref_b)


                    elif file_name.endswith('.storyboard') or file_name.endswith('.xib'):
                        old_ref_m = '<image name="%s"' % old_ref
                        new_ref_m = '<image name="%s"' % new_ref
                        file_new_data = file_data.replace(old_ref_m, new_ref_m)

                        # image = "icon_add_collection"

                        old_ref_c = 'image="%s"' % old_ref
                        new_ref_c = 'image="%s"' % new_ref
                        file_new_data = file_new_data.replace(old_ref_c, new_ref_c)

                        # highlightedImage =
                        old_ref_h = 'highlightedImage="%s"' % old_ref
                        new_ref_h = 'highlightedImage="%s"' % new_ref
                        file_new_data = file_new_data.replace(old_ref_h, new_ref_h)

                    wite_data_to_file(file_path, file_new_data)

# highlightedImage="
def find_highlightedImage(res_path):

    if os.path.exists(res_path):
        list_dirs = os.walk(res_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm') \
                        or file_name.endswith('.h') or file_name.endswith('.pch') or \
                        file_name.endswith('.storyboard') or file_name.endswith('.xib'):  # oc文件

                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)
                    if 'highlightedImage=' in file_data:
                        print file_name


storyboard_new_prefix = "FaCai"
storyboard_old_prefix = "UKRosRed"
def rename_storyboard_name(storyboard_path):

    project_content_path = os.path.join(xcode_project_path, 'project.pbxproj')
    project_content = read_file_data(project_content_path)

    if os.path.exists(storyboard_path):
        list_dirs = os.walk(storyboard_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name.endswith(".storyboard"):

                    if storyboard_new_prefix and file_name.startswith(storyboard_new_prefix): #已经存在前缀，不处理
                        continue

                    file_name_no_extension = os.path.splitext(file_name)[0]
                    file_extension = os.path.splitext(file_name)[1]

                    if not storyboard_new_prefix and not storyboard_old_prefix:  # 此种情况为删除前缀
                        continue

                    print '正在处理文件：' + file_name
                    file_new_name = get_new_file_name_for_oc(file_name, storyboard_old_prefix, storyboard_new_prefix)  # 新文件名字
                    file_old_path = os.path.join(root, file_name)
                    file_new_path = os.path.join(root, file_new_name)

                    try:
                        os.rename(file_old_path, file_new_path)  # 更改文件名

                        file_new_name_no_extension = os.path.splitext(file_new_name)[0]

                        old_xxx = 'kLoadStoryboardWithName(@"' + file_name_no_extension + '")'

                        new_xxx = 'kLoadStoryboardWithName(@"' + file_new_name_no_extension + '")'

                        modify_storyboard_reference(oc_all_path, old_xxx, new_xxx)

                        project_content = replace_xproject_data_reference(project_content, file_name, file_new_name)

                        print '处理完成' + file_name
                    except:
                        print '文件无法更改名称：' + file_old_path
                        continue


        wite_data_to_file(project_content_path, project_content)
        # print '修改完成 file_count:' + str(file_count) + "  handle_file_count:" + str(handle_file_count)

def replace_xproject_data_reference(xproject_data, old_file_name, new_file_name):
    return replace_data_by_word(xproject_data, old_file_name, new_file_name)


def has_new_prefix_in_start(file_name):
    for v in oc_new_prefix_reps:
        if file_name.startswith(v):  # 已经存在前缀，不处理
            return True

    return False

def has_old_prefix_in_start(file_name):

    for v in oc_old_prefix_reps:

        if '+' in file_name:#分类
            vvv = '+' + v
            if vvv in file_name:
                return v

        if file_name.startswith(v):  # 已经存在前缀，不处理
            return v

    return None

def has_new_prefix_in_filename(file_name):
    for v in oc_new_prefix_reps:
        if v in file_name:  # 已经存在前缀，不处理
            return True

    return False


def has_old_prefix_in_filename(file_name):
    for v in oc_old_prefix_reps:
        if v in file_name:  # 已经存在前缀，不处理
            return v

    return None



def get_new_file_name_image(file_name):

    if file_name.startswith(image_new_prefix):  # 已经存在前缀，不处理
        return file_name

    if image_old_prefix.strip() and file_name.startswith(image_old_prefix):  # 存在旧前缀，替换掉
        new_file_name = file_name.replace(image_old_prefix, image_new_prefix)
    else:

        new_file_name = image_new_prefix + file_name
    return new_file_name


def get_new_file_name(file_name, old_prefix, new_prefix): #new_prefix为空表示去掉前缀

    if new_prefix and file_name.startswith(new_prefix):  # 已经存在前缀，不处理
        return file_name

    if old_prefix.strip() and file_name.startswith(old_prefix):  # 存在旧前缀，替换掉
        new_file_name = file_name.replace(old_prefix, new_prefix)
    else:

        new_file_name = new_prefix + file_name
    return new_file_name



def get_new_file_name_for_oc(file_name, old_prefix, new_prefix): #new_prefix为空表示去掉前缀

    if '+' in file_name: #分类
        file_name_s = file_name.split('+')
        category_class = file_name_s[0]
        category_name = file_name_s[1]
        if new_prefix and category_name.startswith(new_prefix):  # 已经存在前缀，不处理
            return file_name

        if old_prefix.strip() and category_name.startswith(old_prefix):  # 存在旧前缀，替换掉
            category_name_new = category_name.replace(old_prefix, new_prefix)
        else:

            category_name_new = new_prefix + category_name

        return category_class + '+' + category_name_new


    if new_prefix and file_name.startswith(new_prefix):  # 已经存在前缀，不处理
        return file_name

    if old_prefix.strip() and file_name.startswith(old_prefix):  # 存在旧前缀，替换掉
        new_file_name = file_name.replace(old_prefix, new_prefix)
    else:

        new_file_name = new_prefix + file_name
    return new_file_name



def replace_file_content_by_word(file_path, old_content, new_content):

    file_data = read_file_data(file_path)

    # have_the_word_in_data(file_data, old_content)
    old_content = '\\b' + old_content + '\\b'
    png_old_name_re = re.compile(old_content)
    result2 = re.sub(png_old_name_re, new_content, file_data)
    # new_f_all_txt = file_data.replace(png_old_name, png_new_name)

    f_obj = open(file_path, 'w')  # 首先先创建一个文件对象
    f_obj.write(result2)
    f_obj.flush()
    f_obj.close()

def wite_data_to_file(file_path, data):
    f_obj = open(file_path, 'w')  # 首先先创建一个文件对象
    f_obj.write(data)
    f_obj.flush()
    f_obj.close()


def replace_data_by_word(data, old_content, new_content):

    if '+' in old_content:
        new_data = data.replace(old_content, new_content)
    else:

        old_content = '\\b' + old_content + '\\b'
        png_old_name_re = re.compile(old_content)
        new_data = re.sub(png_old_name_re, new_content, data)
    return new_data

def replace_image_data(data, old_content, new_content):
    old_content = '"' + old_content + '"'
    new_content = '"' + new_content + '"'
    # png_old_name_re = re.compile(old_content)
    # new_data = re.sub(png_old_name_re, new_content, data)
    new_data = data.replace(old_content, new_content)
    return new_data


def replace_data_content(data, old_content, new_content):

    png_old_name_re = re.compile(old_content)

    new_data = re.sub(png_old_name_re, new_content, data)
    return new_data


def replace_data_content22(data, old_content, new_content, delete):

    png_old_name_re = re.compile(old_content)

    if delete:
        aaa = png_old_name_re.match(data)
        new_data = data.replace(old_content, aaa.group(0))

    else:
        new_data = re.sub(png_old_name_re, new_content, data)
    return new_data


def have_the_word_in_data(data, the_str):

    word_pattern = '\\b' + the_str + '\\b'
    match_obj = re.search(re.compile(word_pattern), data)
    # if match_obj:
    #     print match_obj.group()
    return match_obj

def read_file_data(file_path):
    f_obj = open(file_path, mode="r")  # 首先先创建一个文件对象
    f_data = f_obj.read()  # 用read()方法读取文件内容
    f_obj.close()
    return f_data


def get_image_in_source_():

    dir_path = '/Users/gan/iospro/game/rongyaodg/app/Classes/'

    if os.path.exists(dir_path):
        list_dirs = os.walk(dir_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                file_path = os.path.join(root, file_name)  # 文件路径
                file_data = read_file_data(file_path)

                match_obj = re.findall(re.compile('\"\w+\(%s|%d\)\w+\.png\\b'), file_data)
                if match_obj:

                    print 'file match'
                    for v in match_obj:

                        print v
                        image_name = v.replace('\"','')

                        if image_name in image_exclude_files:
                            pass
                        else:

                            image_exclude_files.append(image_name)

                # print 'no match'
        print image_exclude_files

def rename_all_res_file():

    res_dir_path = '/Users/gan/iospro/game/res/'

    if os.path.exists(res_dir_path):
        list_dirs = os.walk(res_dir_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                new_file_name = get_new_file_name(file_name, image_old_prefix, image_new_prefix)

                file_old_path = os.path.join(root, file_name)
                file_new_path = os.path.join(root, new_file_name)
                os.rename(file_old_path, file_new_path)

def rename_class():

    # class_data = read_file_data('/Users/gan/iospro/game/rongyaodg/app/Classes/KKForverSkyRunClassHeader.h')
    file_path = '/Users/gan/iospro/game/rongyaodg/app/Classes/KKForverSkyRunClassHeader.h'
    file = open(file_path, 'r')

    new_data = ''
    try:
        text_lines = file.readlines()
        # print(type(text_lines), text_lines)

        for line in text_lines:
            # print(line)
            str_arr = line.split(' ')
            if '#define' in line and len(str_arr) >= 3:

                calssName = str_arr[1]
                calssName_2 = str_arr[2]
                line_new = line.replace(calssName_2, 'KKForeverSkyRun' + calssName)
                new_data = new_data + line_new + '\n'

            else:
                new_data = new_data + line + '\n'

    finally:
        file.close()

    if new_data:
        wite_data_to_file(file_path,new_data)


def rename_method():

    # class_data = read_file_data('/Users/gan/iospro/game/rongyaodg/app/Classes/KKForverSkyRunMethodHeader.h')
    file_path = '/Users/gan/iospro/game/rongyaodg/app/GameIOS/KKForverSkyRunMethodHeader.h'
    file = open(file_path, 'r')

    new_data = ''
    try:
        text_lines = file.readlines()
        # print(type(text_lines), text_lines)

        for line in text_lines:
            # print(line)

            str_arr = line.split(' ')
            if '#define' in line and len(str_arr) >= 3:

                calssName = str_arr[1]
                calssName_2 = str_arr[2]
                line_new = line.replace(calssName_2, 'yyFoverDiamond' + calssName[0:1].upper() + calssName[1:])
                new_data = new_data + line_new + '\n'

            else:
                new_data = new_data + line + '\n'

    finally:
        file.close()

    if new_data:
        wite_data_to_file(file_path, new_data)

def deleteComments():#还有问题

    source_dir = '/Users/gan/iospro/game/rongyaodg/app/Classes/device'

    if os.path.exists(source_dir):
        list_dirs = os.walk(source_dir)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if 'google' in root or 'bind' in root:
                    continue

                if file_name.endswith('.h') or file_name.endswith('.m') or file_name.endswith('.mm') or file_name.endswith('.cpp'):

                    file_path = os.path.join(root, file_name)
                    file_data = read_file_data(file_path)

                    file_data_0 = replace_data_content(file_data,'/\\*\\*/', '')
                    file_data_1 = replace_data_content(file_data_0,'([^:/])//.*', '\\1')
                    file_data_2 = replace_data_content(file_data_1,'^//.*', '')
                    file_data_3 = replace_data_content(file_data_2,'/\\*{1,2}[\\s\\S]*?\\*/', '')
                    file_data_4 = replace_data_content(file_data_3,'\\s*\\n', '\\n')

                    wite_data_to_file(file_path, file_data_4)

def addComments():#还有问题

    source_dir = '/Users/gan/iospro/game/rongyaodg/app/Classes/game/battle/proxy'

    aaa_data = read_file_data('/Users/gan/iospro/game/afaefae.txt')

    str2 = aaa_data.decode('windows-1252')
    aaa_data = str2.encode('utf-8')

    # wite_data_to_file('/Users/gan/iospro/game/afaefae22222.txt', aaa_data)
    # fencoding = chardet.detect(aaa_data)
    # print 'fencoding ' + fencoding
    # aa = 'eee'
    # if aa:
    #     return
    data_length = len(aaa_data)
    mmm_not = ['#ifndef','#import','#include','#endif','#define']

    if os.path.exists(source_dir):
        list_dirs = os.walk(source_dir)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if 'google' in root or 'bind' in root:
                    continue

                if file_name.endswith('.h') or file_name.endswith('.m') or file_name.endswith(
                        '.mm') or file_name.endswith('.cpp'):
                    file_path = os.path.join(root, file_name)

                    f_obj = open(file_path, "r")
                    text_lines = f_obj.readlines()

                    content = ''
                    print '处理中  ' + file_name
                    for line in text_lines:

                        # str2 = line.decode('windows-1252')
                        # line = str2.encode('utf-8')

                        if '//' in line or '#import' in line or '#include' in line or '#ifndef' in line or '#endif' in line or '#define' in line or line.endswith('\\'):
                            content = content + line

                        elif '{' == line.strip() or '}' == line.strip() or 'else' == line.strip() or 'break;' == line.strip():
                            content = content + line

                        else:

                            isneed = random.randint(1, 3)
                            if isneed == 2:
                                content = content + line

                            else:

                                start = random.randint(1, data_length - 600)
                                comment_length = random.randint(1, 300)
                                comment_data = aaa_data[start: start + comment_length]

                                comment_type = random.randint(1, 3)

                                if comment_type == 2:

                                    comment_data_2 = comment_data.replace('\n', '')
                                    comment_data_2 = '\n// ' + comment_data_2 + '\n'
                                    content = content + comment_data_2 + line

                                else:

                                    comment_data_2 = '\n/**\n  ' + comment_data + ' \n**/\n'
                                    content = content + comment_data_2 + line

                    wite_data_to_file(file_path, content)

def addFunction_furee(oc_path):
    file_path = '/Users/gan/Desktop/黑特篮球new2/all_function.log'
    f_obj = open(file_path, "r")
    text_lines = f_obj.readlines()

    xx = '#define %s axxp%s'
    for line in text_lines: #define left_controller_click_name @"left_controller_click_name"
        xline = line.strip()

        bb = '_'+xline
        if haveOfforceInSources(oc_path, bb):
            continue
        print xx % (xline, xline)

def haveOfforceInSources(oc_path, xofforce):
    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store":
                    continue

                if file_name.endswith('.m') or file_name.endswith('.mm'):  # oc文件

                    file_path = os.path.join(root, file_name)  # 头文件路径
                    file_data = read_file_data(file_path)
                    if xofforce in file_data:
                        return True

        return False

    return False

def fix_oc_catgery_class_name(oc_path):

    project_content_path = os.path.join(xcode_project_path, 'project.pbxproj')
    project_content = read_file_data(project_content_path)

    if os.path.exists(oc_path):
        list_dirs = os.walk(oc_path)
        for root, dirs, files in list_dirs:
            for file_name in files:

                if file_name == ".DS_Store" or file_name.endswith(".swift"):
                    continue

                if 'Masonry' in root:
                    continue

                if file_name.endswith('.m') or file_name.endswith('.h'):#cpp文件

                    if '+' in file_name and 'GlodBule' in file_name: #分类

                        file_new_name = file_name.replace('GlodBule','')
                        file_old_path = os.path.join(root, file_name)
                        file_new_path = os.path.join(root, file_new_name)
                        try:
                            os.rename(file_old_path, file_new_path)  # 更改文件名

                            # file_new_name_no_extension = os.path.splitext(file_new_name)[0]
                            # modify_oc_class_reference(oc_all_path, file_name_no_extension, file_new_name_no_extension)

                            # 更改xproject文件中的文件名
                            project_content = replace_xproject_data_reference(project_content, file_name, file_new_name)

                        except:
                            print '文件无法更改名称：' + file_old_path
                            continue
        wite_data_to_file(project_content_path, project_content)


if __name__ == '__main__':


    rename_imageset_dir_name(modify_xcassets_src_path)  #.xcassets 目录手动改一下
    # find_highlightedImage(modify_xcassets_src_path)

   #3 # rename_imageset_file_name(modify_res_path) 更改图片名称

   #1 # modify_oc_class_name(oc_modify_path)

   #2 # rename_storyboard_name(oc_modify_path)
    # addFunction_furee(oc_modify_path) #playOrPauseBtn

    # temp = '"filename" : "数据 (1).png"'
    # aa = replace_image_data(temp, '数据 (1).png', 'eeee数据 (1).png')
    # print aa
    # fix_oc_catgery_class_name(oc_modify_path)



    pass
