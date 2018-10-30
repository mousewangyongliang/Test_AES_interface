# Test_AES_interface

# 需准备库：pycryptodome,configparser,requests,xlrd,xlutils,inspect，xlwt
加密接口自动化测试

config.ini文件为配置文件，代码读取文件执行

[KEY]：AES加密key，

[API]:接口host地址

[PADDING]:填充边界值

excel目录中存储接口测试用例，代码将读取该xls文件的case进行测试

表格格式：

接口地址、测试驱动、请求参数、预期结果、实际结果、是否通过

接口地址：要测试接口的path地址

测试驱动：及测试点，如：正常参数、缺失id、缺少name...

请求参数：要发送的请求参数，request params

预期结果：要断言的字段

实际结果：response，执行完接口请求，将会把响应结果写入excel文件

是否通过：通过断言判断接口测试是否通过

注意：执行时，excel表为关闭，避免不必要麻烦。

itools目录下为核心，实现AES加密和接口请求


