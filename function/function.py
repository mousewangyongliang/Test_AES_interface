#coding:utf-8
import inspect
# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

class pub(object):
    def __init__(self):
        pass

    def check_res(self, data, real):
        """
        断言检测接口返回与定义是否相同，接口是否正常
        :param title:接口测试点标题
        :param think:预期结果
        :param real:实际返回结果data
        :return:
        """
        function_name = inspect.stack()[1][3]   # 动态获取当前运行的函数名
        num = inspect.stack()[1][2]     # 动态获取当前行号
        try:
            assert data['checkData'] in real, '%s-%s:---%s,%s接口测试不通过' % (function_name, num, data['url'], data['title'])
            if data['checkData'] in real:
                return u'测试通过'
        except AssertionError as e:
            print(e)


    def resultwrap(self, result):
        return result.replace(',', ','+'\n')

