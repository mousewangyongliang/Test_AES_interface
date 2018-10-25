#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import requests
from aesItools import AESmodel
import xlrd
from xlutils.copy import copy
import os
from function.function import pub
Dir = os.path.dirname(os.path.abspath(__file__))
excelpath = os.path.join(os.path.dirname(Dir), 'excel\\funsee.xls')     # excel表格地址

class interFace(object):
    def __init__(self):
        self.ci = AESmodel()
        self.excel = xlrd.open_workbook(excelpath)
        self.wb = copy(self.excel)
        self.pub = pub()
        self.headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}

    def test_url(self, data):
        """
        请求接口，返回结果，写入文件
        :param data: 请求和执行数据字典，url接口地址、params接口参数、row行、workbook工作簿....
        :return: 返回响应结果是否与预期一致
        """
        url = self.ci.cf.get("API", "host")     # config获取url前缀
        sendUrl = url + data['url']
        send_params = 'encrypt=' + self.ci.encrypt(data['params'])      # 接口定义请求参数需要encrypt=*****
        res = requests.post(url=sendUrl, data=send_params, headers=self.headers)
        response = self.ci.decrypt(res.text)     # 接口返回的结果
        print(response)
        self.write_result(data, 4, self.pub.resultwrap(response))     # 写入excel实际返回结果
        is_pass = self.pub.check_res(data['title'], data['checkData'], response)  # 断言检测
        self.write_result(data, 5, is_pass)      # 接口测试是否通过


    def get_param_by_excel(self, names):
        """
        读取excel表格，获取接口测试的参数，然后进行接口请求
        :param names: excel 的工作簿
        :return:
        """
        sheet = self.excel.sheet_by_name(names)     # 通过name使用sheet
        rows = sheet.nrows
        cols = sheet.ncols
        for i in range(1, rows):
            rowValue = sheet.row_values(i, end_colx=cols)
            data = {
                'row': i,
                'url': rowValue[0],
                'title': rowValue[1],
                'params': eval(rowValue[2]),
                'checkData': rowValue[3],
                'workbook': names
            }
            self.test_url(data)     # 循环每个参数驱动，进行接口测试


    def write_result(self, data, col, response):
        """
        将测试结果写入excel表中
        :param data:row行数据、workbook工作簿数据
        :param col: 要插入的列
        :param response: 插入的结果
        :return:
        """
        s = self.wb.get_sheet(data['workbook'])
        s.write(data['row'], col, response)
        self.wb.save(excelpath)


    def run_test(self):
        """
        获取excel表中所有的工作簿的名字，进行循环测试用例
        :return:
        """
        nameList = self.excel.sheet_names()
        for names in nameList:
            self.get_param_by_excel(names)

a = interFace()
# a.get_param_by_excel('login')
a.run_test()