#!/usr/bin/env python
#coding=utf-8
import base64
import binascii
import logging

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex, b2a_base64, a2b_base64
from  Crypto import Random
from Crypto.Util.Padding import pad


class PrpCrypt(object):

    def __init__(self, key, iv):
        if len(key) > 16:
            key = key[0:16]
        if len(iv) > 16:
            iv = iv[0:16]
        key = key.encode('utf-8')
        while len(key) % 16 != 0:
            key += '\0'
        self.key = key #self.add_to_16(key)
        self.mode = AES.MODE_CBC
        self.block_size = 16
        while len(iv) % 16 != 0:
            iv += '\0'
        self.iv = iv#Random.new().read(AES.block_size)

        # 填充函数
        # self.padding = lambda data: data + (self.block_size - len(data) % self.block_size) * chr(self.block_size - len(data) % self.block_size)
        # 此处为一坑,需要现将data转换为byte再来做填充，否则中文特殊字符等会报错
        # self.padding_for_str = lambda data: data + (self.block_size - len(data.encode('utf-8')) % self.block_size) * chr(
        #     self.block_size - len(data.encode('utf-8')) % self.block_size)

        self.padding_for_data = lambda data: data + (self.block_size - len(data) % self.block_size) * chr(
            self.block_size - len(data) % self.block_size)

        # bs = AES.block_size
        # pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

        # 截断函数
        self.unpadding = lambda data: data[:-ord(data[-1])]


    def encrypt_for_data(self, file_data):
        # cipher = AES.new(self.key, self.mode, self.iv)
        # base64_text = base64.b64encode(file_data)
        # ciphertext = self.aes_encrypt(base64_text)

        try:
            # 填充16位
            padding_text = self.padding_for_data(file_data)
            # 初始化加密器
            cryptor = AES.new(self.key, self.mode, self.iv)
            # 进行AES加密
            encrypt_aes = cryptor.encrypt(padding_text)
            # 进行BASE64转码
            # encrypt_text = (base64.b64encode(encrypt_aes)).decode()
            return encrypt_aes
        except Exception as e:
            logging.exception(e)

    def aes_encrypt_base64(self, plaintext):
        """
        加密
        :param plaintext: 明文
        :return:
        """
        try:
            # 填充16位
            # padding_text = self.padding_for_str(plaintext).encode("utf-8")
            # # 初始化加密器
            # cryptor = AES.new(self.key, self.mode, self.iv)
            # # 进行AES加密
            # encrypt_aes = cryptor.encrypt(padding_text)
            padding_text = plaintext.encode("utf-8")
            encrypt_aes = self.encrypt_for_data(padding_text)
            # 进行BASE64转码
            encrypt_text = (base64.b64encode(encrypt_aes)) #.decode()
            return encrypt_text
        except Exception as e:
            logging.exception(e)

    def aes_decrypt_base64(self, ciphertext):
        """
        解密
        :param ciphertext: 密文
        :return:
        """
        try:
            # 密文必须是16byte的整数倍
            # if len(ciphertext) % 16 != 0:
            #     raise binascii.Error('密文错误!')
            cryptor = AES.new(self.key, self.mode, self.iv)
            # 进行BASE64转码
            plain_base64 = base64.b64decode(ciphertext)
            # 进行ASE解密
            decrypt_text = cryptor.decrypt(plain_base64)
            # 截取
            decrypt_text = self.unpadding(decrypt_text)
            return decrypt_text
        except UnicodeDecodeError as e:
            logging.error('解密失败,请检查密钥是否正确!')
            logging.exception(e)
        except binascii.Error as e:
            logging.exception(e)
        except Exception as e:
            logging.exception(e)

    # 加密函数，如果text不足16位就用空格补足为16位，
    # 如果大于16当时不是16的倍数，那就补足为16的倍数。
    # def encrypt(self, text):
    #     text = text.encode('utf-8')
    #
    #     cryptor = AES.new(self.key, self.mode, self.iv)
    #     # 这里密钥key 长度必须为16（AES-128）,
    #     # 24（AES-192）,或者32 （AES-256）Bytes 长度
    #     # 目前AES-128 足够目前使用
    #     length = 16
    #     count = len(text)
    #     if count < length:
    #         add = (length - count)
    #         # \0 backspace
    #         # text = text + ('\0' * add)
    #         text = text + ('\0' * add).encode('utf-8')
    #     elif count > length:
    #         add = (length - (count % length))
    #         # text = text + ('\0' * add)
    #         text = text + ('\0' * add).encode('utf-8')
    #     text = pad(text, 16, style='pkcs7')
    #     self.ciphertext = cryptor.encrypt(text)
    #     # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
    #     # 所以这里统一把加密后的字符串转化为16进制字符串
    #     # return b2a_hex(self.ciphertext)
    #     return b2a_base64(self.ciphertext)
    #
    # # 解密后，去掉补足的空格用strip() 去掉
    # def decrypt(self, text):
    #     cryptor = AES.new(self.key, self.mode, self.iv)
    #     # plain_text = cryptor.decrypt(a2b_hex(text))
    #     plain_text = cryptor.decrypt(a2b_base64(text))
    #     # return plain_text.rstrip('\0')
    #     return bytes.decode(plain_text).rstrip('\0')


if __name__ == '__main__':
    pc = PrpCrypt('mplaywlzhsKEY','mplaywlzhsIV')  # 初始化密钥
    # data = input("请输入待加密数据：")#
    data = 'userId'

    aes_decrypt_a = pc.aes_encrypt_base64(data)
    print("aes_encrypt2:", aes_decrypt_a)
    aes_decode_data = aes_decrypt_a
    aes_decrypt_a = pc.aes_decrypt_base64(aes_decode_data)
    print("aes_decrypt2:", aes_decrypt_a)

    print 'aaddd'.encode("utf-8").encode("utf-8")