#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import requests
from aesItools import AESmodel
import xlrd
import xlwt
from xlutils.copy import copy
import os
from function.function import pub
Dir = os.path.dirname(os.path.abspath(__file__))

class interFace(object):
    def __init__(self):
        self.ci = AESmodel()
        self.excelpath = os.path.join(os.path.dirname(Dir), 'excel\\'+self.ci.excel)     # excel表格地址
        self.excel = xlrd.open_workbook(self.excelpath)
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

        try:
            """接口正常"""
            response = self.ci.decrypt(res.text)     # 接口返回的结果
            self.write_result(data, 4, self.pub.resultwrap(response), 0)  # 写入excel实际返回结果
            is_pass = self.pub.check_res(data, response)  # 断言检测
            if is_pass == '测试通过':
                self.write_result(data, 5, is_pass, 3)  # 接口测试是否通过
            else:
                self.write_result(data, 5, u'测试不通过', 2)  # 接口测试是否通过
        except Exception as e:
            """接口报错"""
            print(e)
            print('%s-%s:---%s,%s接口报错' % ('interface/test_url', '35', data['url'], data['title']))
            response = res.text

            self.write_result(data, 4, self.pub.resultwrap(response), 0)  # 写入excel实际返回结果
            self.write_result(data, 5, u'接口报错', 2)  # 接口报错,写入字体颜色为红色



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


    def write_result(self, data, col, response, color):
        """
        将测试结果写入excel表中
        :param data:row行数据、workbook工作簿数据
        :param col: 要插入的列
        :param response: 插入的结果
        :param color: 字体颜色
        :return:
        """
        s = self.wb.get_sheet(data['workbook'])
        s.write(data['row'], col, response, self.set_color(color))
        self.wb.save(self.excelpath)


    def run_test(self):
        """
        获取excel表中所有的工作簿的名字，进行循环测试用例
        :return:
        """
        nameList = self.excel.sheet_names()
        for names in nameList:
            self.get_param_by_excel(names)

    def set_color(self, color):
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.colour_index = color
        style.font = font
        return style


if __name__ == '__main__':
    a = interFace()
    a.run_test()