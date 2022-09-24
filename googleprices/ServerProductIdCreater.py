#coding=utf-8

import csv

import time
import types

import xlrd
import os
import sys
from priceinfo import *

#解决 UnicodeDecodeError: 'ascii' codec can't decode 报错
reload(sys)
sys.setdefaultencoding('utf8')


def get_current_time2():
    # print time.time()
    t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    return t

if __name__ == '__main__':

    file_name = '/Users/gan/Downloads/副本《元神修真傳》参数&定价表(1).xlsx'
    sheets = 2

    game_code = 'sczg'
    rate = 30

    templete_sql = 'INSERT INTO `games`.`t_games_commodity_item`(`itemId`, `gameCode`, `productId`, `appleId`, `price`, ' \
                   '`priceMoneyType`, `moneyBaseNum`, `moneyBaseNumType`, `stoneBaseNum`, `multiple`, `giftMultiple`, `cardTypeBaseNum`, `isCardType`,' \
                   ' `createdTime`, `modifiedTime`, `platFormSource`, `platFormSourceMode`, `description`, `dayNumber`, `actStartTime`, `actEndTime`,' \
                   ' `actPurchaseNum`, `cardTypeTips`, `flag`) VALUES ' \
                   '(null, \'%s\', \'%s\', \'\', %s, \'USD\', %s, \'TWD\', %s, %s, 0, 0.00, 0, 1564416000, 0, \'google\', \'google\', \'%s\', 0, 0, 0, 0, \'%s\', 1);'

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

        for row in range(nrows):

            if row != 0:

                s_value_0 = table.cell(row, 0).value  #美金
                s_value_1 = table.cell(row, 1).value
                s_value_2 = table.cell(row, 2).value
                s_value_3 = table.cell(row, 3).value #台币
                s_value_4 = table.cell(row, 4).value #描述
                s_value_5 = table.cell(row, 5).value #id
                # s_value_6 = table.cell(row, 6).value
                # s_value_7 = table.cell(row, 7).value
                # s_value_8 = table.cell(row, 8).value
                # s_value_9 = table.cell(row, 9).value
                # s_value_10 = table.cell(row, 10).value

                sql_full = templete_sql % (game_code, s_value_5, s_value_0, s_value_3, int(s_value_3), rate, s_value_4, s_value_4)
                print sql_full
