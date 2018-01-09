# from selenium import webdriver
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.common.exceptions import UnexpectedAlertPresentException
# from time import sleep
#
# driver = webdriver.Chrome()
# driver.get("https://www.helloweba.com/demo/2017/unlock/")
#
#
# dragger = driver.find_elements_by_class_name("slide-to-unlock-handle")[0]
#
# action = ActionChains(driver)
#
# action.click_and_hold(dragger).perform()  #鼠标左键按下不放
#
# for index in range(200):
#     try:
#         action.move_by_offset(2, 0).perform() #平行移动鼠标
#     except UnexpectedAlertPresentException:
#         break
#     sleep(1)
# #等待停顿时间
# action.release()
#
#
# # 打印警告框提示
# success_text = driver.switch_to.alert.text
# print(success_text)
#
# sleep(5)
#
# driver.quit()
import re
import json

class test:

    def __init__(self,stringWord,chartWord = "AssertionError"):
        self.chartWord = chartWord
        self.stringWord = stringWord
        self.__rule = re.compile(chartWord)
        self.interval = self.__rule.search(self.stringWord)



    def getinterval(self):
        if not self.interval:
            assert 0,"输入字符'{}'中缺少未查询到相应的字符！".format(self.stringWord)
        start = self.interval.start()
        end = self.interval.end()
        return eval("self.stringWord[{}:{}]".format(start,end))

    def getright(self):
        if not self.interval:
            assert 0,"输入字符'{}'中缺少未查询到相应的字符！".format(self.stringWord)
        end = self.interval.end()
        return eval("self.stringWord[{}:]".format(end))

    def getlefe(self):
        if not self.interval:
            assert 0,"输入字符'{}'中缺少未查询到相应的字符！".format(self.stringWord)
        start = self.interval.start()
        return eval("self.stringWord[:{}]".format(start))

    def getChese(self):
        test(self.stringWord,chartWord="([/u4e00-/u9fa5]+)")
        if not self.interval:
            assert 0,"输入字符'{}'中缺少未查询到相应的字符！".format(self.stringWord)
        return self.interval.group()

    def getEnglist(self):
        pass

    def getNum(self):
        pass

    def getCapital(self):
        pass

    def getLowercase(self):
        pass