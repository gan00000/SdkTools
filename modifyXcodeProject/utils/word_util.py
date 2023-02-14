#coding=utf-8
import imp
import random
import sys

imp.reload(sys)
sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的

import os
import re

genest_word = []
words_dong = []
words_name = []

words_dong_s = []
def random_word_dong():
    temp_int = random.randint(0, len(words_dong) - 1)
    temp = words_dong[temp_int]
    while temp in words_dong_s:
        temp_int = random.randint(0, len(words_dong) - 1)
        temp = words_dong[temp_int]
    words_dong_s.append(temp)
    return temp


words_name_s = []
def random_word_name():
    temp_int = random.randint(0, len(words_name) - 1)
    temp = words_name[temp_int]
    while temp in words_name_s:
        temp_int = random.randint(0, len(words_name) - 1)
        temp = words_name[temp_int]
    words_name_s.append(temp)
    return temp

# words_name_alary = []
def random_2word():#随机生成两个单词

    word_aar = []
    for i in range(2):
        word_str = random_1word()
        while word_str in word_aar:
            word_str = random_1word()
        word_aar.append(word_str)

    return word_aar[0], word_aar[1]


def random_1word():

    w_index = random.randint(0, len(genest_word) - 1)
    first_word = genest_word[w_index]
    # while first_word in words_name_alary:
    #     first_index = random.randint(0, len(genest_word) - 1)
    #     first_word = genest_word[first_index]
    # words_name_alary.append(first_word)
    return first_word


def random_2words_not_same_inarr(word_aar):
    w_temp = []
    for i in range(2):
        word_str = random_1word()
        while word_str in word_aar:
            word_str = random_1word()
        word_aar.append(word_str)
        w_temp.append(word_str)
    return w_temp[0], w_temp[1]


def random_1words_not_same_inarr(word_aar):

    word_str = random_1word()
    while word_str in word_aar:
        word_str = random_1word()
    word_aar.append(word_str)

    return word_str

def words_reader(word_file_path):

    words = []
    f_obj = open(word_file_path, "r")
    text_lines = f_obj.readlines()
    for line in text_lines:
        line = line.decode('utf-8')
        word = line.strip().replace(' ', '')
        if len(word) > 2:  # 太短的单词去掉
            words.append(word)
    return words