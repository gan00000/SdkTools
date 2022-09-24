#coding=utf-8

import csv

import time
import types

import xlrd
import os
import sys

#解决 UnicodeDecodeError: 'ascii' codec can't decode 报错
reload(sys)
sys.setdefaultencoding('utf8')


def readInfoFromExcel(file_name,sheets):

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

    return table
        # google_price_info = []
        # for row in range(nrows):
        #     if row == 0:
        #         continue
        #     cell0 = table.cell(row, 0).value
        #     cell1 = table.cell(row, 1).value
        #     cell2 = table.cell(row, 2).value
        #     cell3 = table.cell(row, 3).value
            # cell4 = table.cell(row, 4).value
            # cell5 = table.cell(row, 5).value
            # cell6 = table.cell(row, 6).value
            # cell7 = table.cell(row, 7).value
            # cell8 = table.cell(row, 8).value

            # print sqltime_new


def handleShengao(table_index):
    height_temple_boy_table = readInfoFromExcel("/Users/gan/Desktop/jie/shengaotizhong_temple.xlsx", 0)
    height_temple_girl_table = readInfoFromExcel("/Users/gan/Desktop/jie/shengaotizhong_temple.xlsx", 1)

    height_student_table = readInfoFromExcel(data_file, table_index)
    nrows_student = height_student_table.nrows
    ncols_student = height_student_table.ncols

    for row in range(nrows_student):
        if row < 3:
            continue

        name = height_student_table.cell(row, 1).value  # 性别
        gender = height_student_table.cell(row, 2).value #性别
        gender = str(gender).strip()
        month_age = height_student_table.cell(row, 14).value
        body_height = height_student_table.cell(row, 8).value

        if month_age == "" or month_age == " ":
            print "年龄错误"
            continue

        try:
            month_age = float(month_age)
        except:
            print "年龄错误"
        try:
            body_height = float(body_height)
            if gender == "男":
                handleBodyHeightCompare(body_height, height_temple_boy_table, month_age)
            else:
                handleBodyHeightCompare(body_height, height_temple_girl_table, month_age)

        except:
            print "未知"


def handleBodyHeightCompare(body_height, height_temple_table, month_age):
    nrows_temple = height_temple_table.nrows
    for row_body_height_temple in range(nrows_temple):
        if row_body_height_temple == 0:
            continue
        boy_month_age_temple = height_temple_table.cell(row_body_height_temple, 1).value
        body_height_temple_1SD_fu = height_temple_table.cell(row_body_height_temple, 4).value
        body_height_temple_1SD_zheng = height_temple_table.cell(row_body_height_temple, 6).value

        body_height_temple_2SD_fu = height_temple_table.cell(row_body_height_temple, 3).value
        body_height_temple_2SD_zheng = height_temple_table.cell(row_body_height_temple, 7).value

        body_height_temple_3SD_fu = height_temple_table.cell(row_body_height_temple, 2).value
        body_height_temple_3SD_zheng = height_temple_table.cell(row_body_height_temple, 8).value

        boy_month_age_temple = float(boy_month_age_temple)
        body_height_temple_1SD_fu = float(body_height_temple_1SD_fu)
        body_height_temple_1SD_zheng = float(body_height_temple_1SD_zheng)
        body_height_temple_2SD_fu = float(body_height_temple_2SD_fu)
        body_height_temple_2SD_zheng = float(body_height_temple_2SD_zheng)
        body_height_temple_3SD_fu = float(body_height_temple_3SD_fu)
        body_height_temple_3SD_zheng = float(body_height_temple_3SD_zheng)

        if row_body_height_temple + 1 >= nrows_temple:
            # print "最后一个"
            if body_height >= body_height_temple_1SD_fu and body_height <= body_height_temple_1SD_zheng:
                print "正常范围"
            elif body_height >= body_height_temple_2SD_fu and body_height <= body_height_temple_2SD_zheng:
                if body_height < body_height_temple_1SD_fu:
                    print "偏矮"
                else:
                    print "偏高"
            elif body_height >= body_height_temple_3SD_fu and body_height <= body_height_temple_3SD_zheng:
                if body_height < body_height_temple_2SD_fu:
                    print "超偏矮"
                else:
                    print "超偏高"
            else:
                print "未知"
            break
        else:
            boy_month_age_temple_next = height_temple_table.cell(row_body_height_temple + 1, 1).value

            if month_age >= boy_month_age_temple and month_age < boy_month_age_temple_next:

                if body_height >= body_height_temple_1SD_fu and body_height <= body_height_temple_1SD_zheng:
                    print "正常范围"
                elif body_height >= body_height_temple_2SD_fu and body_height <= body_height_temple_2SD_zheng:
                    if body_height < body_height_temple_1SD_fu:
                        print "偏矮"
                    else:
                        print "偏高"
                elif body_height >= body_height_temple_3SD_fu and body_height <= body_height_temple_3SD_zheng:
                    if body_height < body_height_temple_2SD_fu:
                        print "超偏矮"
                    else:
                        print "超偏高"
                else:
                    print "未知"
                break

def handleBodyWeightCompare(body_height, height_temple_table, month_age):
    nrows_temple = height_temple_table.nrows
    for row_body_height_temple in range(nrows_temple):
        if row_body_height_temple == 0:
            continue
        boy_month_age_temple = height_temple_table.cell(row_body_height_temple, 1).value
        body_height_temple_1SD_fu = height_temple_table.cell(row_body_height_temple, 4).value
        body_height_temple_1SD_zheng = height_temple_table.cell(row_body_height_temple, 6).value

        body_height_temple_2SD_fu = height_temple_table.cell(row_body_height_temple, 3).value
        body_height_temple_2SD_zheng = height_temple_table.cell(row_body_height_temple, 7).value

        body_height_temple_3SD_fu = height_temple_table.cell(row_body_height_temple, 2).value
        body_height_temple_3SD_zheng = height_temple_table.cell(row_body_height_temple, 8).value

        boy_month_age_temple = float(boy_month_age_temple)
        body_height_temple_1SD_fu = float(body_height_temple_1SD_fu)
        body_height_temple_1SD_zheng = float(body_height_temple_1SD_zheng)
        body_height_temple_2SD_fu = float(body_height_temple_2SD_fu)
        body_height_temple_2SD_zheng = float(body_height_temple_2SD_zheng)
        body_height_temple_3SD_fu = float(body_height_temple_3SD_fu)
        body_height_temple_3SD_zheng = float(body_height_temple_3SD_zheng)

        if row_body_height_temple + 1 >= nrows_temple:
            # print "最后一个"
            if body_height >= body_height_temple_1SD_fu and body_height <= body_height_temple_1SD_zheng:
                print "正常范围"
            elif body_height >= body_height_temple_2SD_fu and body_height <= body_height_temple_2SD_zheng:
                if body_height < body_height_temple_1SD_fu:
                    print "偏瘦"
                else:
                    print "偏胖"
            elif body_height >= body_height_temple_3SD_fu and body_height <= body_height_temple_3SD_zheng:
                if body_height < body_height_temple_2SD_fu:
                    print "超偏瘦"
                else:
                    print "超偏胖"
            else:
                if body_height < body_height_temple_3SD_fu:
                    print "超偏瘦"
                elif body_height > body_height_temple_3SD_zheng:
                    print "超偏胖"
                else:
                    print "未知"
            break
        else:
            boy_month_age_temple_next = height_temple_table.cell(row_body_height_temple + 1, 1).value

            if month_age >= boy_month_age_temple and month_age < boy_month_age_temple_next:

                if body_height >= body_height_temple_1SD_fu and body_height <= body_height_temple_1SD_zheng:
                    print "正常范围"
                elif body_height >= body_height_temple_2SD_fu and body_height <= body_height_temple_2SD_zheng:
                    if body_height < body_height_temple_1SD_fu:
                        print "偏瘦"
                    else:
                        print "偏胖"
                elif body_height >= body_height_temple_3SD_fu and body_height <= body_height_temple_3SD_zheng:
                    if body_height < body_height_temple_2SD_fu:
                        print "超偏瘦"
                    else:
                        print "超偏胖"
                else:
                    if body_height < body_height_temple_3SD_fu:
                        print "超偏瘦"
                    elif body_height > body_height_temple_3SD_zheng:
                        print "超偏胖"
                    else:
                        print "未知"
                break

def handleTizhong(table_index):
    weight_temple_boy_table = readInfoFromExcel("/Users/gan/Desktop/jie/shengaotizhong_temple.xlsx", 2)
    weight_temple_girl_table = readInfoFromExcel("/Users/gan/Desktop/jie/shengaotizhong_temple.xlsx", 3)

    weight_student_table = readInfoFromExcel(data_file, table_index)
    nrows_student = weight_student_table.nrows
    ncols_student = weight_student_table.ncols

    for row in range(nrows_student):
        if row < 3:
            continue

        name = weight_student_table.cell(row, 1).value
        gender = weight_student_table.cell(row, 2).value #性别
        gender = str(gender).strip()
        month_age = weight_student_table.cell(row, 14).value
        body_weight = weight_student_table.cell(row, 9).value

        if month_age == "" or month_age == " ":
            print "年龄错误"
            continue
        try:
            month_age = float(month_age)
        except:
            print "年龄错误"

        try:
            body_weight = float(body_weight)
            if gender == "男":

                handleBodyWeightCompare(body_weight, weight_temple_boy_table, month_age)
            else:
                handleBodyWeightCompare(body_weight, weight_temple_girl_table, month_age)
        except:
            print "未知"

def get_second_time():
    # print time.time()
    t = int(time.time())
    return t

if __name__ == '__main__':

    # if os.path.exists(google_price_path) is not True:
    #     print 'googlepricetemplate file path error,use默认'
    #     google_price_path = os.path.join(desktop,"googlepricetemplate.xlsx");
    # get_second_time()
    # readInfoFromExcel("/Users/gan/Downloads/xxxxx.xlsx", 0)

    index = 11
    data_file = '/Users/gan/Desktop/jie/aaa-1-10.xlsx'
    handleShengao(index)

    print "==========下面是体重==========="

    handleTizhong(index)

    print "==========结束==========="
    print "==========结束==========="
    print "==========结束==========="
    print "==========结束==========="
    print "==========结束==========="
    print "==========结束==========="
    print "==========结束==========="
    print "==========结束==========="
    print "==========结束==========="
    print "==========结束==========="
    print "==========结束==========="
    print "==========结束==========="

