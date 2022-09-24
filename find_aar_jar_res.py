#coding=utf-8

import csv

import time
import types

import shutil
import xlrd
import os
import sys

#解决 UnicodeDecodeError: 'ascii' codec can't decode 报错
reload(sys)
sys.setdefaultencoding('utf8')


def get_current_time2():
    # print time.time()
    t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    return t


def copyjarres(dirname, dstDirName):

    dirbasename = os.path.basename(dirname)
    aarversion = dirbasename.replace('.aar', '')
    if os.path.exists(dirname):

        if not os.path.exists(dstDirName):
            os.makedirs(dstDirName)
        for root, dirs, files in os.walk(dirname):
            if len(dirs) > 0:
                for named in dirs:
                    print named

                    isfind = 0

                    if named == 'jars':
                        isfind = 1
                        jardir = os.path.join(root, named)
                        classespath = os.path.join(jardir, 'classes.jar')
                        if os.path.exists(classespath):
                            shutil.copyfile(classespath, os.path.join(dstDirName, aarversion+".jar"))


                        resdir = os.path.join(root, 'res')
                        if os.path.exists(resdir):
                            aarversion_a = aarversion.replace('.', '-')
                            print aarversion_a
                            dstresdir = os.path.join(dstDirName, aarversion_a)
                            if os.path.exists(dstresdir):
                                shutil.rmtree(dstresdir)
                            shutil.copytree(resdir, dstresdir)

                    if isfind == 1:
                        return


def readPriceInfoFromExcel(file_name,sheets):
    if os.path.exists(file_name):
        # 打开excel
        data = xlrd.open_workbook(file_name)  # 注意这里的workbook首字母是小写
        # 查看文件中包含sheet的名称
        # data.sheet_names()
        # 得到第一个工作表，或者通过索引顺序 或 工作表名称
        table = data.sheets()[sheets]
        # #获取行数和列数
        nrows = table.nrows
        ncols = table.ncols

        excelContent = []

        for row in range(nrows):
            cellm = table.cell(row, 0).value
            excelContent.append(cellm)

        return excelContent



if __name__ == '__main__':

    dirname = '/Users/gan/.gradle/caches/transforms-1/files-1.1/'
    dstDirName = '/Users/gan/Desktop/aarclass'
    excelpath='/Users/gan/Desktop/jarlist.xlsx'

    excelContents = readPriceInfoFromExcel(excelpath,0)
    for v in  excelContents:
        dirname_a = os.path.join(dirname,v)
        if os.path.exists(dirname_a):
            copyjarres(dirname_a, dstDirName)
        else:
            print '不存在目录:' + v


