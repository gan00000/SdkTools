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

        localLanguage = ''

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

                title = table.cell(row, 6).value
                pricingTemplateId = table.cell(row, 7).value
                mLocalLanguage = table.cell(row, 8).value
                if mLocalLanguage:
                    localLanguage = mLocalLanguage

                print title

                Local_Title_Des = cteareLocal_Title_Des_all(localLanguage,title)
                print Local_Title_Des

                pinfo = PriceInfo()

                pinfo.local_title_des = Local_Title_Des
                pinfo.productId = product_id

                if pricingTemplateId  and pricingTemplateId != '':

                    pinfo.PricingTemplateID = pricingTemplateId

                else:

                    if usd_price and hk_price:
                        if 'zh_TW' == localLanguage:
                            price_info = createPrice(hk_price, usd_price)
                            pinfo.price_info = price_info
                        elif 'en_US' == localLanguage:
                            price_info = createPrice_en(hk_price, usd_price)
                            pinfo.price_info = price_info
                        else:
                            pass


                google_price_info.append(pinfo)
        return google_price_info


def cteareLocal_Title_Des_all(local,title):

    return local + '; ' + title + '; ' + title

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
    home = os.path.expanduser('~')
    desktop = os.path.join(home, "Desktop")

    for v in cmd_argv_array:
        print v

    google_price_path = ''
    csv_file_path = ''

    sheetCode = 0
    try:
        google_price_path = cmd_argv_array[1]
        csv_file_path = cmd_argv_array[2]
        print google_price_path
        print csv_file_path + ' '

    except:
        pass

    if os.path.exists(google_price_path) is not True:
        print 'googlepricetemplate file path error,use默认'
        google_price_path = os.path.join(desktop,"googlepricetemplate.xlsx");


    if os.path.exists(google_price_path) is not True:
        print 'google_price_info file must not empty'


    if os.path.exists(csv_file_path) is not True:
        print '生成文件路径错误,use默认'
        cvs_name = 'google_price_' + get_current_time2() + '.csv'
        csv_file_path = os.path.join(desktop, cvs_name)

    if type(sheetCode) is not int:
        sheetCode = 0

    print google_price_path
    print csv_file_path
    print sheetCode
    google_price_info = readPriceInfoFromExcel(google_price_path, sheetCode)

    write_price_info_to_csv()

