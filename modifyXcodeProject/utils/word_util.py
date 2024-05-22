#coding=utf-8
import imp
import random
import string
import sys

imp.reload(sys)
sys.setdefaultencoding('utf-8') #设置默认编码,只能是utf-8,下面\u4e00-\u9fa5要求的

import os
import re

word_26 = 'qwertyuiopasdfghjklzxcvbnm'

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

def random_property():

    ww = ''
    aa = random.randint(0, 6)
    if aa <= 2:
        w1_name = random_word_name()
        w1_dong = random_word_dong()
        ww = w1_dong.lower() + w1_name.capitalize()
    elif aa == 3:
        w1_name = random_word_name()
        w2_name = random_word_name()
        ww = w1_name.lower() + w2_name.capitalize()
    elif aa == 4:
        w1_name = random_word_name()
        w2_name = random_word_name()
        ww = w1_name.lower() + w2_name
    else:
        w1_name = random_word_name()
        w1_dong = random_word_dong()
        ww = w1_dong.lower() + w1_name

    return ww

# words_name_alary = []
def random_2word():#随机生成两个单词

    word_aar = []
    for i in range(2):
        word_str = random_1word()
        while word_str in word_aar:
            word_str = random_1word()
        word_aar.append(word_str)

    return word_aar[0], word_aar[1]

w_count = 0
def random_1word():

    w_index = random.randint(0, len(genest_word) - 1)
    first_word = genest_word[w_index]
    # while first_word in words_name_alary:
    #     first_index = random.randint(0, len(genest_word) - 1)
    #     first_word = genest_word[first_index]
    # words_name_alary.append(first_word)
    global w_count
    w_count = w_count + 1

    aa = random.randint(1, 6)
    for ii in range(aa):
        addd = string.letters[random.randint(0, len(string.letters) - 1)]
        first_word = first_word + addd
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


def generateIntArr(count):

    intArr = []
    for i in range(count):

        a_value = random.randint(1, 100000)
        while a_value in intArr:
            a_value = random.randint(1, 100000)

        intArr.append(str(a_value))

    return intArr