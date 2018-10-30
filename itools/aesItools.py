#coding:utf-8

from Crypto.Cipher import AES
from Crypto.Util import Padding
import json
import base64
import configparser
import os
from urllib import quote
Dir = os.path.dirname(os.path.abspath(__file__))
configpath = os.path.join(os.path.dirname(Dir), 'config.ini')

class AESmodel(object):
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(configpath, encoding='utf-8')  # 通过utf-8编码读取文件
        key = str(self.cf.get("KEYS", u'key'))   # 读取的key是unicode编码，使用str()转换为字符串
        self.block_size = int(self.cf.get("PADDING", 'block_size'))
        # self.cipher = AES.new(self.pad_key(key), AES.MODE_ECB)
        self.cipher = AES.new(key, AES.MODE_ECB)
        self.excel = self.cf.get("EXCEL", 'excelname')      # 获取excel文件名

    # # 加密内容需要长达16位字符，所以进行空格拼接
    # def pad(self, text):
    #     while (len(text) % 16 != 0):
    #         # text += '\0'
    #         text += b' '
    #     # BS = 16
    #     # pad_it = text + (BS - len(text) % BS) * chr(BS - len(text) % BS)  # 自己进行PKCS5填充计算，使用空格进行填充
    #     return text
    #
    # # 加密秘钥需要长达16位字符，所以进行空格拼接
    # def pad_key(self, key):
    #     while len(key) % 16 != 0:
    #         key += b' '
    #         # key += '\0'
    #     return key

    def encrypt(self, info):

        byte_info = str.encode(json.dumps(info), encoding='utf8')
        # byte_info = str.encode(info, encoding='utf8')
        block_info = Padding.pad(byte_info, block_size=self.block_size , style='pkcs7')      # 使用库自带的填充方式
        # ci_info = self.pad(byte_info)     # 使用自己写的填充方式
        res = self.cipher.encrypt(block_info)
        baseres = base64.b64encode(res)
        return quote(baseres)


    def decrypt(self, info):
        data = json.loads(info)['result']
        # data = info
        basedata = base64.b64decode(data)
        res = self.cipher.decrypt(basedata)
        result = Padding.unpad(res, block_size=self.block_size, style='pkcs7')      # 使用库自带的删除填充
        # return json.loads(result)
        return result.decode('unicode_escape')

# a = AESmodel()
# a.encrypt('1234567890')
# res = 'kcIai%2BNnFfvHRm0UxXpd/SGEUndd8gJoMQG6MsL014CIdefx5DECmrDy/yqX8TSBJPKxA%2BJ8v7ZkLDnZjLb89202omIMyZwJ7%2Bqg7BSRrHDjVOXBFQHzTRt62nubP1ymPHb1xbQus%2BvwzgECyw8cPofzFMX0gNrhH2LbtXxT%2By%2BvsdOu8XiB9W7bW9VuxNnpZhl2NSkVy1w6IitjGJgBfAL8eA9ZgkidSpUOjmNfxkfywoNYtczV0b%2BXFME89nZf6ZvwJXScLPphl6F6wOoKEndM5PVKOEFkA4fVWrxOz7sIliJqr/gdecJfcqN7bi6wW2XxlD1hOOztZf/opI0EcEN1qqhu52/Ylo9WSVD7Oy8L551qdFuaMAVlCvBh38/c5WpHhCJ6AtUrXstXyNqjFCvFNi4PX7d3DZV69/sc%2B4KVwWHOd6hABhetAYrs32qusWX%2BUKxJra%2BSxoggiavDESnEy1fhOHR/CH3KpbGGeU0cMLEu51V4WjSo6%2BzzI8kYM4o5%2BiAwCBWF0BZn/8AnJAFdSTsNMK08K6spcjn/hiO7acJXZzw%2BwSpxNwzO69YJ/N17kTX3nC4OMm1eYYDcqLONg8pm%2BNm/Nk3Ur/0Uk/TCvtpOXNBykaUS/0p%2BzpMBZv6nXegnqccXnnPkTmmn0JC1oijX6je%2B6JXLJ6pOoAID5tDDuOLmsLqJtH3ixsqSiO6wD/YN1uBTh3gRwx1Ktw%3D%3D'
# a.decrypt(res)