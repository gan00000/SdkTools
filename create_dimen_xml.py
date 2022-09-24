#coding=utf-8
import imp
import sys
import re
import os

if __name__ == '__main__':

    filePath = '/Users/gan/dimen_px.txt'
    if os.path.exists(filePath):

        fp = open(filePath,'w')

        beishu = 1/1.6

        for i in range(801):

            data_dimen_temp = '<dimen name="px_%s">%sdp</dimen>\n' % (str(i), str(round(i * beishu,2)))
            fp.write(data_dimen_temp)

        fp.close()