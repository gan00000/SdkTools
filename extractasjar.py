#coding=utf-8
import os

import shutil


def extractarr(dirname,dstDirName):

    if os.path.exists(dirname):

        if not os.path.exists(dstDirName):
            os.makedirs(dstDirName)
        for root, dirs, files in os.walk(dirname):
            for name in files:
                if name == 'inputs':
                    f_path = os.path.join(root, name)
                    fobj = open(f_path, "r")  # 首先先创建一个文件对象
                    # print f_txt  # 打印所读取到的内容
                    for line in fobj.readlines():
                        print line
                        if 'FILE_PATH=' in line:
                            strings = line.split('=')
                            arrpath = strings[1]

                            arrpath = arrpath.strip('\n')

                            fileName = os.path.basename(arrpath)

                            outFileName = os.path.join(dstDirName,fileName)
                            if os.path.exists(arrpath):
                                shutil.copyfile(arrpath,outFileName)
                    fobj.close()

if __name__ == '__main__':
    srcDir = '/Users/gan/.android/build-cache/'
    outputDir = '/Users/gan/asarroutput/'
    extractarr(srcDir, outputDir)