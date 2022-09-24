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

        google_price_info = []
        for row in range(nrows):
            if row == 0:
                pass
            else:
                product_id = table.cell(row, 0).value
                usd_price = table.cell(row, 1).value
                tw_price = table.cell(row, 2).value
                hk_price = table.cell(row, 3).value
                stoneCount = table.cell(row, 4).value
                stoneName = table.cell(row, 5).value

                # pricingTemplate = table.cell(row, 6).value

                # print 'usd_price:' + str(usd_price) + ' tw_price:' + str(tw_price) + '  hk_price:' + str(hk_price) + '  normal_send:' + str(normal_send) + '  product_id:' + product_id + '  rate:' + rate

                if en == 0:

                    title = createTitle_en(usd_price, stoneCount, stoneName)
                    print title
                    price_des = createPrice_en(hk_price, usd_price)
                    print price_des
                    Local_Title_Des = cteareLocal_Title_Des_en(title)
                    print Local_Title_Des

                elif en == 100:
                    title = createTitle_ch(usd_price, stoneCount, stoneName)
                    print title
                    price_des = createPrice(hk_price, tw_price)
                    print price_des
                    Local_Title_Des = cteareLocal_Title_Des_ch(title)
                    print Local_Title_Des


                else:
                    title = createTitle(usd_price, stoneCount, stoneName)
                    print title
                    price_des = createPrice(hk_price,tw_price)
                    print price_des
                    Local_Title_Des = cteareLocal_Title_Des(title)
                    print Local_Title_Des

                pinfo = PriceInfo()

                pinfo.local_title_des = Local_Title_Des
                pinfo.price_info = price_des
                pinfo.productId = product_id
                google_price_info.append(pinfo)
        return google_price_info


def cteareLocal_Title_Des(title):

    return 'zh_TW; ' + title + '; ' + title

def cteareLocal_Title_Des_ch(title):

    return 'zh-CN; ' + title + '; ' + title

def cteareLocal_Title_Des_en(title):

    return 'en_US; ' + title + '; ' + title

def createTitle(usd_price, stoneCount, stoneName):#正常发送砖石为空，一般为卡类或者礼包

    return str(usd_price) + '美元兌換' + str(stoneCount) + stoneName

def createTitle_ch(usd_price, stoneCount, stoneName):#正常发送砖石为空，一般为卡类或者礼包

    return str(usd_price) + '美元购买' + str(stoneCount) + stoneName

def createTitle_en(usd_price, stoneCount, stoneName):#正常发送砖石为空，一般为卡类或者礼包

    print "stoneCount=" + str(stoneCount)
    if not stoneCount or stoneCount == '':
        return str(usd_price) + ' USD buy ' + stoneName

    if type(stoneCount) is types.StringType:
        return str(usd_price) + ' USD buy ' + str(stoneCount) + ' ' + stoneName
    else:
        return str(usd_price) + ' USD buy ' + str(int(stoneCount)) + ' ' + stoneName


def createPrice(hk_price, tw_price):
    if hk_price and tw_price:

        return 'HK; ' + str(int(hk_price * 1000000)) + ';' + ' TW; ' + str(int(tw_price * 1000000)) + '; ' + 'HK; ' + str(int(hk_price * 1000000))

def createPrice_en(hk_price, usd_price):
    if hk_price and usd_price:

        return 'HK; ' + str(int(hk_price * 1000000)) + ';' + ' US; ' + str(int(usd_price * 1000000))


def write_price_info_to_csv():

    csvfile = open(csv_file_path, 'w')
    writer = csv.writer(csvfile)
    # writer.writerow(['Product ID', 'Published State', 'Purchase Type','Auto Translate','Locale; Title; Description','Auto Fill Prices','Price','Pricing Template ID'])
    title = ['Product ID', 'Published State', 'Purchase Type', 'Auto Translate', 'Locale; Title; Description',
             'Auto Fill Prices', 'Price', 'Pricing Template ID']
    data = [
        title
    ]

    for info in google_price_info:
        # info_list = info.toInfoArray
        # print info_list
        a = []
        a.append(info.productId)
        a.append(info.publishedState)
        a.append(info.purchaseType)
        a.append(info.AutoTranslate)
        a.append(info.local_title_des)
        a.append(info.AutoFillPrices)
        a.append(info.price_info)
        a.append(info.PricingTemplateID)
        data.append(a)
    writer.writerows(data)
    csvfile.close()


def get_current_time2():
    # print time.time()
    t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
    return t

if __name__ == '__main__':

    cmd_argv_array = sys.argv

    # cmd_argv_array.append('aaddd')
    # cmd_argv_array.append('fadf')
    # cmd_argv_array.append('33aaa')
    # cmd_argv_array.append('adfeee')

    for v in cmd_argv_array:
        print v

    google_price_path = ''
    csv_file_path = ''
    isEn = ''
    sheetCode = 0
    try:
        # google_price_path = cmd_argv_array[1]
        # csv_file_path = cmd_argv_array[2]
        isEn = cmd_argv_array[1]
        # sheetCode = cmd_argv_array[4]

        print 'en英文 ,其他为繁体 isEn = ' + isEn
    except:
        pass

    if os.path.exists(google_price_path) is not True:
        google_price_path = '/Users/gan/Desktop/googleprice.xlsx'


    if os.path.exists(google_price_path) is not True:
        print 'google_price_info file must not empty'

    else:

        if os.path.exists(csv_file_path) is not True:
            csv_file_path = '/Users/gan/Desktop/Googleplay商品定价/google_price_' + get_current_time2() + '.csv'

        if isEn == 'en':
            en = 0

        elif isEn == 'ch':

            en = 100

        else:
            en = 1

        if type(sheetCode) is not int:
            sheetCode = 0


        print google_price_path
        print csv_file_path
        print isEn
        print sheetCode
        google_price_info = readPriceInfoFromExcel(google_price_path, sheetCode)

        write_price_info_to_csv()

# csv_file_path = '/Users/gan/Desktop/Googleplay商品定价/gbml-2.8.csv'
    #
    # en = 0  # 0為全球英文
    # # en = 1
    # google_price_info = readPriceInfoFromExcel('/Users/gan/Desktop/googleprice.xlsx', 0)
    #
    # write_price_info_to_csv()
