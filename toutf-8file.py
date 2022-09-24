#coding=utf-8
import os
import codecs
import sys
import json

from requests.packages import chardet

# reload(sys)
# sys.setdefaultencoding("utf-8")


def encodeUtf8(src,dst):
    if os.path.exists(src):
        list_dirs = os.walk(src)
        if not os.path.exists(dst):
            os.mkdir(dst)
        for root, dirs, files in list_dirs:
            for f in files:

                if f == ".DS_Store":
                    continue

                f_path = os.path.join(root, f)
                print f_path
                fobj = open(f_path, "r")  # 首先先创建一个文件对象
                content = fobj.read()
                encoding_str = chardet.detect(content) #获得文件内容的编码格式
                print encoding_str
                print encoding_str['encoding']

                fobj.close()

                data = content.decode(encoding_str['encoding']).encode('utf-8') #先解码为unicode后在编码为utf-8

                dst_file_path = f_path.replace(src, dst)
                print dst_file_path

                dst_file_dir = os.path.dirname(dst_file_path)
                print 'dst_file_dir-' + dst_file_dir
                if not os.path.exists(dst_file_dir):
                    os.mkdir(dst_file_dir)

                fdst_obj = open(dst_file_path, "w")  # 首先先创建一个文件对象
                fdst_obj.write(data)
                fdst_obj.close()

if __name__ == '__main__':
    # s = '中文'  # 注意这里的 str 是 str 类型的，而不是 unicode
    # s.encode('utf-8')
    encodeUtf8("/Users/gan/Desktop/WeChatSDK_sample_Android-1/app/src/main/java/net/sourceforge/simcpux","/Users/gan/Desktop/WeChatSDK_sample_Android-1/app/src/main/java/net/sourceforge/simcpux2")