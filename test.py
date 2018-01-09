# import xlrd,os
# from config import app
#
#
# kk = app.config['BASE_DIR']
# cc = os.path.join(kk,"Other","UIconfig.xlsx")
# file = xlrd.open_workbook(cc)
# tables = file.sheets()[0]
# nrowsdata = tables._cell_values
# nrowsdata.pop(0)
# importlist = []
# xx = 0
# for table in nrowsdata:
#     if "N" in table:
#         pass
#     else:
#         importlist.append(table[1])
# if xx == 0:
#     print(importlist)
# else:
#     print(nrowsdata)
# class kk:
#     def __init__(self):
#         pass
#     def test(self):
#         print("begin!")
#
# class ll:
#     def __init__(self):
#         pass
#     def hir(self):
#         print("start!")
#
# class cc(kk,ll):
#     def __call__(self, *args, **kwargs):
#         pass
#     def hir(self):
#         print("45")
#     pass
#
#
# bb = cc()
# print(bb.hir())
# from echarts import Echart,Legend,Bar,Axis
# import os
# chart = Echart("GDP","this is a test")
# chart.use(Bar("China",[2,3,4,5]))
# chart.use(Legend("GDP"))
# chart.use(Axis("category","bottom",data=["Nov","Tom","Jan","Feb"]))
# #chart.plot()
# chart.save(os.path.abspath("."),"kirryTest")



# class scores(object):
#     num = None
#
#     @property
#     def score(self):
#         return  self.num
#
#     @score.setter
#     def score(self,num):
#         self.num = num*num


    # @score.setter
    # def score(self,num):
    #     if num> 12 or num < 0:
    #         assert 0,ValueError("数据值应该在0-12之间！")
    #     else:
    #         print("good boy!")

    # @score.setter
    # def score(self,num):
    #     if num:
    #         print("year boy!")
    #     else:
    #         assert 0,ValueError("传入数据为0！")




# import os
# class Brase(object):
#
#     while True:
#         try:
#             from selenium.webdriver.chrome.webdriver import WebDriver as chrome
#             driver = chrome()
#             driver.set_page_load_timeout(16)
#             if  driver.find_elements_by_css_selector("ele"):
#                 driver.execute_script("window.close()")
#             else:
#                 assert 0,"加载超时"
#
#         except:
#             os.system("pip install selenium")
#
#     def test(self):
#         kk = object()
from PIL import Image
from pytesseract import *

filename = "D:\\123.png"
kk = image_to_string(Image.open(filename))
print(kk)









































