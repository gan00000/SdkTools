# -*- coding: utf-8 -*-

import hashlib
import sys
import os
import json

def md5hex(word):
    """ MD5加密算法，返回32位小写16进制符号 """
    if isinstance(word, unicode):
        word = word.encode("utf-8")
    elif not isinstance(word, str):
        word = str(word)
    m = hashlib.md5()
    m.update(word)
    return m.hexdigest()


def md5sum(fname):
    """ 计算文件的MD5值 """
    def read_chunks(fh):
        fh.seek(0)
        chunk = fh.read(8096)
        while chunk:
            yield chunk
            chunk = fh.read(8096)
        else: #最后要将游标放回文件开头
            fh.seek(0)

    m = hashlib.md5()
    if isinstance(fname, basestring) \
            and os.path.exists(fname):
        with open(fname, "rb") as fh:
            for chunk in read_chunks(fh):
                m.update(chunk)
    #上传的文件缓存 或 已打开的文件流
    elif fname.__class__.__name__ in ["StringIO", "StringO"] \
                or isinstance(fname, file):
        for chunk in read_chunks(fname):
            m.update(chunk)
    else:
        return ""
    return m.hexdigest()


def md5_dir_file(parentdir,respath):

    list_dirs = os.walk(respath)

    filedic = {}

    fileMd5Info = []

    for root, dirs, files in list_dirs:

        # if 'res' in root or 'src' in root:
        for f in files:
            if f == 'filemd5List.json' or f == '.DS_Store' or f == '.tags_sorted_by_file' or f == '.tags' or f == '.git':
                continue
            filepath = os.path.join(root, f)
            file_md5 = md5sum(filepath)
            mInfo = {}
            mInfo["path"] = root[len(parentdir):] + '/'
            mInfo["name"] = f
            mInfo["md5"] = file_md5
            fileMd5Info.append(mInfo)

    count = {}
    count["allcount"] = len(fileMd5Info)

    fileMd5Info.append(count)

    filedic["listdata"] = fileMd5Info

    j = json.dumps(filedic, ensure_ascii=False)

    if j:
        j = j.replace('},', '},\n')
        md5_file_path = os.path.join(respath,'res','filemd5List.json')
        f_obj = open(md5_file_path, 'w')  # 首先先创建一个文件对象
        f_obj.write(j)
        f_obj.flush()
        f_obj.close()
        print 'md5生成完成：' + md5_file_path


def makedir(dir):

    list_dirs = os.walk(dir)
    for root, dirs, files in list_dirs:

        if 'res' in dirs and 'src' in dirs:

            if not root.endswith('plaza'):
                print root
                parent_path = os.path.dirname(root) + '/'  # 获得d所在的目录,即d的父级目录
                # print '父目录=' + parent_path
                md5_dir_file(parent_path, root)
                pass





if __name__ == '__main__':
    # / Users / gan / CocosProjects / Game / Phone316Game / androidciphercode
    makedir(os.path.join('/Users/gan/CocosProjects/Game/Phone316Game /', 'androidciphercode','base'))
    # a = sys.argv
    # if len(a) >= 2:
    #
    #     platform = a[1]
    #     print 'md5 platform = ' + platform
    #     scriptDir = os.path.dirname(os.path.abspath("__file__"))
    #     print scriptDir
    #     scriptDir = os.path.dirname(scriptDir)
    #     print scriptDir
    #     if platform == 'android':
    #         makedir(os.path.join(scriptDir,'androidciphercode'))
    #         print '开始计算MD5'
    #     elif platform == 'ios':
    #         print '开始计算MD5'
    #         makedir(os.path.join(scriptDir, 'ciphercode'))
    #     else:
    #         print '出错。。。'