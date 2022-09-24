#coding=utf-8

import csv

import time
import types

import xlrd
import os
import sys

from flask import json

#解决 UnicodeDecodeError: 'ascii' codec can't decode 报错
reload(sys)
sys.setdefaultencoding('utf8')

sql_model = ''

# INSERT INTO `games`.`t_games_commodity_item`(`itemId`, `gameCode`, `productId`, `appleId`, `price`, `priceMoneyType`, `moneyBaseNum`, `moneyBaseNumType`, `stoneBaseNum`, `multiple`, `giftMultiple`, `cardTypeBaseNum`, `isCardType`, `createdTime`, `modifiedTime`, `platFormSource`, `platFormSourceMode`, `description`, `dayNumber`, `actStartTime`, `actEndTime`, `actPurchaseNum`, `cardTypeTips`, `flag`) VALUES (19893, 'sds', 'SPS0013380', 'com.web.50twd', 0.00, 'USD', 50.00, 'TWD', 50, 2, 0, 0.00, 0, 0, 0, 'FA200000002', 'mycardBilling', 'MyCard測試金流', 0, 0, 0, 0, '鑽石', 1);

sdd='{"ReturnCode":"1","ReturnMsg":"查詢成功","IngameItems":{"PaymentType":"INGAME","PaymentTypeDesc":"實體卡","ItemList":[{"ItemCode":"Gmama300","ItemCodeDesc":"Gmamamobi遊戲平台300元","TradePointType":"2","Amount":"300","Currency":"TWD"},{"ItemCode":"Gmama50","ItemCodeDesc":"Gmamamobi遊戲平台50元","TradePointType":"2","Amount":"50","Currency":"TWD"},{"ItemCode":"Gmama450","ItemCodeDesc":"Gmamamobi遊戲平台450元","TradePointType":"2","Amount":"450","Currency":"TWD"},{"ItemCode":"Gmama400","ItemCodeDesc":"Gmamamobi遊戲平台400元","TradePointType":"2","Amount":"400","Currency":"TWD"},{"ItemCode":"Gmama500","ItemCodeDesc":"Gmamamobi遊戲平台500元","TradePointType":"2","Amount":"500","Currency":"TWD"},{"ItemCode":"Gmama1000","ItemCodeDesc":"Gmamamobi遊戲平台1000元","TradePointType":"2","Amount":"1000","Currency":"TWD"},{"ItemCode":"Gmama1150","ItemCodeDesc":"Gmamamobi遊戲平台1150元","TradePointType":"2","Amount":"1150","Currency":"TWD"},{"ItemCode":"Gmama350","ItemCodeDesc":"Gmamamobi遊戲平台350元","TradePointType":"2","Amount":"350","Currency":"TWD"},{"ItemCode":"Gmama150","ItemCodeDesc":"Gmamamobi遊戲平台150元","TradePointType":"2","Amount":"150","Currency":"TWD"},{"ItemCode":"Gmama5000","ItemCodeDesc":"Gmamamobi遊戲平台5000元","TradePointType":"2","Amount":"5000","Currency":"TWD"},{"ItemCode":"Gmama3000","ItemCodeDesc":"Gmamamobi遊戲平台3000元","TradePointType":"2","Amount":"3000","Currency":"TWD"},{"ItemCode":"Gmama2000","ItemCodeDesc":"Gmamamobi遊戲平台2000元","TradePointType":"2","Amount":"2000","Currency":"TWD"},{"ItemCode":"Gmama10000","ItemCodeDesc":"Gmamamobi遊戲平台10000元","TradePointType":"2","Amount":"10000","Currency":"TWD"},{"ItemCode":"Gmama30","ItemCodeDesc":"Gmamamobi遊戲平台30元","TradePointType":"2","Amount":"30","Currency":"TWD"},{"ItemCode":"Gmama90","ItemCodeDesc":"Gmamamobi遊戲平台90元","TradePointType":"2","Amount":"90","Currency":"TWD"},{"ItemCode":"Gmama750","ItemCodeDesc":"Gmamamobi遊戲平台750元","TradePointType":"2","Amount":"750","Currency":"TWD"},{"ItemCode":"Gmama1490","ItemCodeDesc":"Gmamamobi遊戲平台1490元","TradePointType":"2","Amount":"1490","Currency":"TWD"}]},"MemberItems":{"PaymentType":"COSTPOINT","PaymentTypeDesc":"會員扣點","ItemList":[{"ItemCode":"MFSD003330","ItemCodeDesc":"Gmamamobi遊戲平台","TradePointType":"1","Amount":"20000","Currency":"TWD"}]},"BillingItems":[{"PaymentType":"99","PaymentTypeDesc":"合作金庫WebATM","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493628","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"DF6000001","PaymentTypeDesc":"ezPay簡單付","PaymentGroup":"area6","PaymentGroupDesc":"電子/行動支付","ItemList":[{"ItemCode":"SPS0493637","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"50000","Currency":"TWD"}]},{"PaymentType":"DF6200001","PaymentTypeDesc":"街口支付","PaymentGroup":"area6","PaymentGroupDesc":"電子/行動支付","ItemList":[{"ItemCode":"SPS0493638","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"50000","Currency":"TWD"}]},{"PaymentType":"DF6300001","PaymentTypeDesc":"台灣Pay","PaymentGroup":"area6","PaymentGroupDesc":"電子/行動支付","ItemList":[{"ItemCode":"SPS0493636","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"5000","Currency":"TWD"}]},{"PaymentType":"DG0700001","PaymentTypeDesc":"Apple Pay","PaymentGroup":"area6","PaymentGroupDesc":"電子/行動支付","ItemList":[{"ItemCode":"SPS0493635","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"10000","Currency":"TWD"}]},{"PaymentType":"DJ1900001","PaymentTypeDesc":"微信支付","PaymentGroup":"area20","PaymentGroupDesc":"大陸地區支付","ItemList":[{"ItemCode":"SPS0493641","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"F1","PaymentTypeDesc":"PPS繳費靈(香港地區)","PaymentGroup":"area22","PaymentGroupDesc":"香港地區支付","ItemList":[{"ItemCode":"SPS0493678","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台300元)","TradePointType":"2","Amount":"300","Currency":"TWD"},{"ItemCode":"SPS0493679","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台350元)","TradePointType":"2","Amount":"350","Currency":"TWD"},{"ItemCode":"SPS0493680","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台400元)","TradePointType":"2","Amount":"400","Currency":"TWD"},{"ItemCode":"SPS0493681","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台450元)","TradePointType":"2","Amount":"450","Currency":"TWD"},{"ItemCode":"SPS0493682","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台500元)","TradePointType":"2","Amount":"500","Currency":"TWD"},{"ItemCode":"SPS0493683","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台1000元)","TradePointType":"2","Amount":"1000","Currency":"TWD"},{"ItemCode":"SPS0493689","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台20000元)","TradePointType":"2","Amount":"20000","Currency":"TWD"},{"ItemCode":"SPS0493690","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台30000元)","TradePointType":"2","Amount":"30000","Currency":"TWD"},{"ItemCode":"SPS0493684","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台1150元)","TradePointType":"2","Amount":"1150","Currency":"TWD"},{"ItemCode":"SPS0493685","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台2000元)","TradePointType":"2","Amount":"2000","Currency":"TWD"},{"ItemCode":"SPS0493686","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台3000元)","TradePointType":"2","Amount":"3000","Currency":"TWD"},{"ItemCode":"SPS0493687","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台5000元)","TradePointType":"2","Amount":"5000","Currency":"TWD"},{"ItemCode":"SPS0493688","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台10000元)","TradePointType":"2","Amount":"10000","Currency":"TWD"}]},{"PaymentType":"F2","PaymentTypeDesc":"信用卡(香港地區 Visa)","PaymentGroup":"area22","PaymentGroupDesc":"香港地區支付","ItemList":[{"ItemCode":"SPS0493664","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台50元)","TradePointType":"2","Amount":"50","Currency":"TWD"},{"ItemCode":"SPS0493665","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台150元)","TradePointType":"2","Amount":"150","Currency":"TWD"},{"ItemCode":"SPS0493666","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台300元)","TradePointType":"2","Amount":"300","Currency":"TWD"},{"ItemCode":"SPS0493667","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台350元)","TradePointType":"2","Amount":"350","Currency":"TWD"},{"ItemCode":"SPS0493668","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台400元)","TradePointType":"2","Amount":"400","Currency":"TWD"},{"ItemCode":"SPS0493669","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台450元)","TradePointType":"2","Amount":"450","Currency":"TWD"},{"ItemCode":"SPS0493674","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台3000元)","TradePointType":"2","Amount":"3000","Currency":"TWD"},{"ItemCode":"SPS0493675","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台5000元)","TradePointType":"2","Amount":"5000","Currency":"TWD"},{"ItemCode":"SPS0493676","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台10000元)","TradePointType":"2","Amount":"10000","Currency":"TWD"},{"ItemCode":"SPS0493677","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台30000元)","TradePointType":"2","Amount":"30000","Currency":"TWD"},{"ItemCode":"SPS0493670","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台500元)","TradePointType":"2","Amount":"500","Currency":"TWD"},{"ItemCode":"SPS0493671","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台1000元)","TradePointType":"2","Amount":"1000","Currency":"TWD"},{"ItemCode":"SPS0493672","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台1150元)","TradePointType":"2","Amount":"1150","Currency":"TWD"},{"ItemCode":"SPS0493673","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台2000元)","TradePointType":"2","Amount":"2000","Currency":"TWD"}]},{"PaymentType":"F7","PaymentTypeDesc":"八達通","PaymentGroup":"area22","PaymentGroupDesc":"香港地區支付","ItemList":[{"ItemCode":"SPS0493691","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台150元)","TradePointType":"2","Amount":"150","Currency":"TWD"},{"ItemCode":"SPS0493692","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台300元)","TradePointType":"2","Amount":"300","Currency":"TWD"},{"ItemCode":"SPS0493693","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台350元)","TradePointType":"2","Amount":"350","Currency":"TWD"},{"ItemCode":"SPS0493694","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台400元)","TradePointType":"2","Amount":"400","Currency":"TWD"},{"ItemCode":"SPS0493695","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台450元)","TradePointType":"2","Amount":"450","Currency":"TWD"},{"ItemCode":"SPS0493696","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台500元)","TradePointType":"2","Amount":"500","Currency":"TWD"},{"ItemCode":"SPS0493702","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台10000元)","TradePointType":"2","Amount":"10000","Currency":"TWD"},{"ItemCode":"SPS0493703","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台20000元)","TradePointType":"2","Amount":"20000","Currency":"TWD"},{"ItemCode":"SPS0493697","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台1000元)","TradePointType":"2","Amount":"1000","Currency":"TWD"},{"ItemCode":"SPS0493698","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台1150元)","TradePointType":"2","Amount":"1150","Currency":"TWD"},{"ItemCode":"SPS0493699","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台2000元)","TradePointType":"2","Amount":"2000","Currency":"TWD"},{"ItemCode":"SPS0493700","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台3000元)","TradePointType":"2","Amount":"3000","Currency":"TWD"},{"ItemCode":"SPS0493701","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台5000元)","TradePointType":"2","Amount":"5000","Currency":"TWD"}]},{"PaymentType":"FA031","PaymentTypeDesc":"PayPal","PaymentGroup":"area8","PaymentGroupDesc":"全球支付","ItemList":[{"ItemCode":"SPS0493639","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"10000","Currency":"TWD"}]},{"PaymentType":"FA035","PaymentTypeDesc":"彰化銀行WebATM","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493615","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"FA036","PaymentTypeDesc":"兆豐銀行WebATM","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493627","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"FA038","PaymentTypeDesc":"銀行轉帳","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493630","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"FA04","PaymentTypeDesc":"中國信託信用卡紅利兌換","PaymentGroup":"area12","PaymentGroupDesc":"紅利抵扣","ItemList":[{"ItemCode":"SPS0493648","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台50元)","TradePointType":"2","Amount":"50","Currency":"TWD"},{"ItemCode":"SPS0493649","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台150元)","TradePointType":"2","Amount":"150","Currency":"TWD"}]},{"PaymentType":"FS0018","PaymentTypeDesc":"亞太電信","PaymentGroup":"area2","PaymentGroupDesc":"行動電話","ItemList":[{"ItemCode":"SPS0493609","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"5000","Currency":"TWD"}]},{"PaymentType":"HA0001","PaymentTypeDesc":"國泰世華MyATM","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493614","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"HA0006","PaymentTypeDesc":"華南銀行WebATM","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493619","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"HA0007","PaymentTypeDesc":"中國信託WebATM","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493616","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"HA0008","PaymentTypeDesc":"玉山銀行WebATM","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493617","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"HA0010","PaymentTypeDesc":"台新銀行WebATM","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493624","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"HA0013","PaymentTypeDesc":"台北富邦WebATM","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493626","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"HA0014","PaymentTypeDesc":"土地銀行WebATM","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493620","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"HA0015","PaymentTypeDesc":"新光銀行WebATM","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493623","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"HA0016","PaymentTypeDesc":"上海銀行WebATM","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493622","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"HA0017","PaymentTypeDesc":"台灣銀行WebATM","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493625","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"HA0018","PaymentTypeDesc":"日盛銀行WebATM","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493629","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"HA0019","PaymentTypeDesc":"第一銀行WebATM","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493618","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]},{"PaymentType":"HC0028","PaymentTypeDesc":"大陸地區網銀支付","PaymentGroup":"area20","PaymentGroupDesc":"大陸地區支付","ItemList":[{"ItemCode":"SPS0493645","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"10000","Currency":"TWD"}]},{"PaymentType":"HC0035","PaymentTypeDesc":"支付寶","PaymentGroup":"area20","PaymentGroupDesc":"大陸地區支付","ItemList":[{"ItemCode":"SPS0493646","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"10000","Currency":"TWD"}]},{"PaymentType":"HC0036","PaymentTypeDesc":"信用卡(台灣地區3D驗證)","PaymentGroup":"area3","PaymentGroupDesc":"信用卡","ItemList":[{"ItemCode":"SPS0493632","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"20000","Currency":"TWD"}]},{"PaymentType":"HC0037","PaymentTypeDesc":"銀聯在線支付","PaymentGroup":"area20","PaymentGroupDesc":"大陸地區支付","ItemList":[{"ItemCode":"SPS0493643","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"10000","Currency":"TWD"}]},{"PaymentType":"HC0038","PaymentTypeDesc":"LINE Pay","PaymentGroup":"area6","PaymentGroupDesc":"電子/行動支付","ItemList":[{"ItemCode":"SPS0493634","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"5000","Currency":"TWD"}]},{"PaymentType":"HE0001","PaymentTypeDesc":"台灣大哥大電信","PaymentGroup":"area2","PaymentGroupDesc":"行動電話","ItemList":[{"ItemCode":"SPS0493608","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"5000","Currency":"TWD"}]},{"PaymentType":"HE0003","PaymentTypeDesc":"中華電信寬頻上網帳單","PaymentGroup":"area1","PaymentGroupDesc":"ADSL電信數據","ItemList":[{"ItemCode":"SPS0493607","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"5000","Currency":"TWD"}]},{"PaymentType":"HE0004","PaymentTypeDesc":"中華電信行動電話帳單","PaymentGroup":"area2","PaymentGroupDesc":"行動電話","ItemList":[{"ItemCode":"SPS0493606","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"5000","Currency":"TWD"}]},{"PaymentType":"HE0011","PaymentTypeDesc":"中華電信市內電話帳單","PaymentGroup":"area4","PaymentGroupDesc":"市內電話","ItemList":[{"ItemCode":"SPS0493605","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"2000","Currency":"TWD"}]},{"PaymentType":"HE0017","PaymentTypeDesc":"Seednet","PaymentGroup":"area1","PaymentGroupDesc":"ADSL電信數據","ItemList":[{"ItemCode":"SPS0493655","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台50元)","TradePointType":"2","Amount":"50","Currency":"TWD"},{"ItemCode":"SPS0493656","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台150元)","TradePointType":"2","Amount":"150","Currency":"TWD"},{"ItemCode":"SPS0493657","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台300元)","TradePointType":"2","Amount":"300","Currency":"TWD"},{"ItemCode":"SPS0493658","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台350元)","TradePointType":"2","Amount":"350","Currency":"TWD"},{"ItemCode":"SPS0493659","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台400元)","TradePointType":"2","Amount":"400","Currency":"TWD"},{"ItemCode":"SPS0493660","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台450元)","TradePointType":"2","Amount":"450","Currency":"TWD"},{"ItemCode":"SPS0493661","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台500元)","TradePointType":"2","Amount":"500","Currency":"TWD"},{"ItemCode":"SPS0493662","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台1000元)","TradePointType":"2","Amount":"1000","Currency":"TWD"},{"ItemCode":"SPS0493663","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台2000元)","TradePointType":"2","Amount":"2000","Currency":"TWD"}]},{"PaymentType":"HE0021","PaymentTypeDesc":"台灣之星","PaymentGroup":"area2","PaymentGroupDesc":"行動電話","ItemList":[{"ItemCode":"SPS0493610","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"5000","Currency":"TWD"}]},{"PaymentType":"HE0033","PaymentTypeDesc":"免費MyCard抵扣","PaymentGroup":"area12","PaymentGroupDesc":"紅利抵扣","ItemList":[{"ItemCode":"SPS0493613","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"2000","Currency":"TWD"}]},{"PaymentType":"HE0037","PaymentTypeDesc":"遠傳電信","PaymentGroup":"area2","PaymentGroupDesc":"行動電話","ItemList":[{"ItemCode":"SPS0493612","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"5000","Currency":"TWD"}]},{"PaymentType":"HF0001","PaymentTypeDesc":"中華郵政WebATM","PaymentGroup":"area5","PaymentGroupDesc":"ATM/銀行轉帳","ItemList":[{"ItemCode":"SPS0493621","ItemCodeDesc":"MyCard點數(Gmamamobi遊戲平台)","TradePointType":"1","Amount":"30000","Currency":"TWD"}]}]}'

ingame_sql_model = 'INSERT INTO `games`.`t_games_productid_item`(`id`, `productId`, `moneyBaseNum`, `moneyBaseNumType`, `flag`, `goldFlow`) VALUES (null, \'com.web._money_twd\', _money_.00, \'TWD\', 1, \'mycard\');'

def read_file_data(file_path):
    f_obj = open(file_path, mode="r")  # 首先先创建一个文件对象
    f_data = f_obj.read()  # 用read()方法读取文件内容
    f_obj.close()
    return f_data

def create_sql(data_sql_model, productId, appleId, moneyBaseNum, PaymentType,description, platFormSourceMode):
    s_gameCode = 'sds'
    s_productId = productId
    s_appleId = appleId
    s_moneyBaseNum = moneyBaseNum
    s_moneyBaseNumType = 'TWD'
    s_stoneBaseNum = moneyBaseNum
    s_multiple = '2'
    s_platFormSource = PaymentType
    s_platFormSourceMode = platFormSourceMode
    s_description = description

    s_createdTime = (int)(time.time())

    data_sql_model_1 = data_sql_model.replace('s_gameCode', s_gameCode) \
        .replace('s_productId',s_productId) \
        .replace('s_appleId', s_appleId) \
        .replace('s_moneyBaseNum', s_moneyBaseNum) \
        .replace('s_NumType', s_moneyBaseNumType) \
        .replace('s_stoneBaseNum', s_stoneBaseNum) \
        .replace('s_multiple', s_multiple) \
        .replace('s_platFormSource', s_platFormSource) \
        .replace('s_Mode', s_platFormSourceMode) \
        .replace('s_description', s_description) \
        .replace('s_createdTime', str(s_createdTime)) \

    print data_sql_model_1


if __name__ == '__main__':

    moneyBaseNum = ['50', '150', '300', '500', '1000', '2000']

    f_path = '/Users/gan/Desktop/payitemsql.txt'

    data_sql_model = read_file_data(f_path)

    data = json.loads(sdd)

    IngameItems = data['IngameItems']

    if IngameItems:
        ItemList = IngameItems['ItemList']
        PaymentType = IngameItems['PaymentType']
        PaymentTypeDesc = IngameItems['PaymentTypeDesc']
        print '\n-- mycard 点数卡========\n'
        # for item in ItemList:
        #     Amount = item['Amount']
        #     ingame_sql = ingame_sql_model.replace('_money_', Amount)
        #     print ingame_sql


        for item_1 in ItemList:
            ItemCode = item_1['ItemCode']
            Amount = item_1['Amount']

            appleId = 'com.web.' + Amount + 'twd'
            create_sql(data_sql_model, ItemCode, appleId, Amount, PaymentType, 'MyCard點數卡', 'mycardIngame')


        print '\n-- mycard 点数卡========\n'


    MemberItems = data['MemberItems']
    if MemberItems:
        PaymentTypeDesc = MemberItems['PaymentTypeDesc']
        PaymentType = MemberItems['PaymentType']
        ItemList = MemberItems['ItemList']
        ItemCode = ItemList[0]['ItemCode']

        print '\n-- mycardVisa 会员扣点========\n'
        for m in moneyBaseNum:
            # com.web.150twd
            appleId = 'com.web.' + m + 'twd'
            create_sql(data_sql_model, ItemCode, appleId, m, PaymentType, PaymentTypeDesc, 'mycardMember')
        print '\n-- mycardVisa 会员扣点========\n'


    BillingItems = data['BillingItems']

    print '\n-- billing ========\n'

    for item in BillingItems:
        PaymentGroupDesc = item['PaymentGroupDesc']
        PaymentTypeDesc_ddd = item['PaymentTypeDesc']
        PaymentType_ddd = item['PaymentType']
        items = item['ItemList']

        if '行動電話' == PaymentGroupDesc or '市內電話' == PaymentGroupDesc:
            PaymentType = item['PaymentType']
            PaymentTypeDesc = item['PaymentTypeDesc']
            ItemCode = item['ItemList'][0]['ItemCode']

            for m in moneyBaseNum:
                # com.web.150twd
                appleId = 'com.web.' + m + 'twd'
                create_sql(data_sql_model, ItemCode, appleId,m,PaymentType,PaymentTypeDesc,'mycardBilling')

        elif 'ATM/銀行轉帳' == PaymentGroupDesc:
            PaymentType = item['PaymentType']
            PaymentTypeDesc = item['PaymentTypeDesc']
            ItemCode = item['ItemList'][0]['ItemCode']

            for m in moneyBaseNum:
                # com.web.150twd
                appleId = 'com.web.' + m + 'twd'
                create_sql(data_sql_model, ItemCode, appleId, m, PaymentType, PaymentTypeDesc, 'mycardWebATM')

        elif 'F2' == PaymentType_ddd:
            PaymentType = item['PaymentType']
            PaymentTypeDesc = item['PaymentTypeDesc']
            ItemList = item['ItemList']
            print '\n-- mycardVisa 信用卡(香港地區 Visa)========\n'
            for item_1 in ItemList:
                ItemCode = item_1['ItemCode']
                Amount = item_1['Amount']
                # if Amount in moneyBaseNum:
                appleId = 'com.web.' + Amount + 'twd'
                create_sql(data_sql_model, ItemCode, appleId, Amount, PaymentType, PaymentTypeDesc, 'mycardVisa')

            print '\n-- mycardVisa 信用卡(香港地區 Visa) end ========\n'

        elif 'HC0036' == PaymentType_ddd:
            PaymentType = item['PaymentType']
            PaymentTypeDesc = item['PaymentTypeDesc']
            ItemList = item['ItemList']
            print '\n-- mycardVisa 信用卡(台灣地區3D驗證)========\n'

            ItemCode = ItemList[0]['ItemCode']
            for m in moneyBaseNum:
                # com.web.150twd
                appleId = 'com.web.' + m + 'twd'
                create_sql(data_sql_model, ItemCode, appleId, m, PaymentType, PaymentTypeDesc, 'mycardVisa')

            print '\n-- mycardVisa 信用卡(台灣地區3D驗證) end ========\n'

        elif 'ADSL電信數據' == PaymentGroupDesc:
            PaymentType = item['PaymentType']
            PaymentTypeDesc = item['PaymentTypeDesc']
            ItemList = item['ItemList']
            print '\n-- mycardBilling ADSL電信數據========\n'

            if len(ItemList) > 1:
                for item_1 in ItemList:
                    ItemCode = item_1['ItemCode']
                    Amount = item_1['Amount']
                    # if Amount in moneyBaseNum:
                    appleId = 'com.web.' + Amount + 'twd'
                    create_sql(data_sql_model, ItemCode, appleId, Amount, PaymentType, PaymentTypeDesc, 'mycardBilling')

            else:
                ItemCode = ItemList[0]['ItemCode']
                for m in moneyBaseNum:
                    # com.web.150twd
                    appleId = 'com.web.' + m + 'twd'
                    create_sql(data_sql_model, ItemCode, appleId, m, PaymentType, PaymentTypeDesc, 'mycardBilling')
            print '\n-- mycardBilling ADSL電信數據 end ========\n'

        else:

            PaymentType = item['PaymentType']
            PaymentTypeDesc = item['PaymentTypeDesc']
            ItemList = item['ItemList']
            print '\n-- mycardBilling 其他========\n'

            if len(ItemList) > 1:
                for item_1 in ItemList:
                    ItemCode = item_1['ItemCode']
                    Amount = item_1['Amount']
                    # if Amount in moneyBaseNum:
                    appleId = 'com.web.' + Amount + 'twd'
                    create_sql(data_sql_model, ItemCode, appleId, Amount, PaymentType, PaymentTypeDesc,'mycardPay')

            else:
                ItemCode = ItemList[0]['ItemCode']
                for m in moneyBaseNum:
                    # com.web.150twd
                    appleId = 'com.web.' + m + 'twd'
                    create_sql(data_sql_model, ItemCode, appleId, m, PaymentType, PaymentTypeDesc, 'mycardPay')
            print '\n-- mycardBilling 其他 end ========\n'








