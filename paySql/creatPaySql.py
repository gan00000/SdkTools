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

sqltime = "INSERT INTO `t_games_commodity_item` (`itemId`, `gameCode`, `productId`, `appleId`, `price`, `priceMoneyType`, `moneyBaseNum`, `moneyBaseNumType`," \
          " `stoneBaseNum`, `multiple`, `giftMultiple`, `cardTypeBaseNum`, `isCardType`," \
          " `createdTime`, `modifiedTime`, `platFormSource`, `platFormSourceMode`," \
          " `description`, `dayNumber`, `actStartTime`, `actEndTime`, `actPurchaseNum`, `cardTypeTips`, `flag`) " \
          "VALUES (null, 'shjy', '%s', '', %s, 'USD', %s, 'CNY'," \
          " %s, 0, 0, 0.00, 0, " \
          "'1638343950', 0, 'web', 'web', " \
          "'%s', 0, 0, 0, 0, '%s', 1);"

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

        google_price_info = []
        for row in range(nrows):
            if row < 1:
                continue
            productId = table.cell(row, 4).value
            cell1 = table.cell(row, 1).value
            description = table.cell(row, 3).value
            cell3 = table.cell(row, 3).value
            # cell4 = table.cell(row, 4).value
            # cell5 = table.cell(row, 5).value
            # cell6 = table.cell(row, 6).value
            # cell7 = table.cell(row, 7).value
            moneyBaseNum = table.cell(row, 6).value
            price = table.cell(row, 7).value

            sqltime_new = sqltime % (
                productId, str(price), str(moneyBaseNum), str(int(moneyBaseNum)), description, description)
            print sqltime_new



def get_second_time():
    # print time.time()
    t = int(time.time())
    return t

if __name__ == '__main__':

    # if os.path.exists(google_price_path) is not True:
    #     print 'googlepricetemplate file path error,use默认'
    #     google_price_path = os.path.join(desktop,"googlepricetemplate.xlsx");
    # get_second_time()
    readInfoFromExcel("/Users/gan/Downloads/shjy-id.xlsx", 0)

