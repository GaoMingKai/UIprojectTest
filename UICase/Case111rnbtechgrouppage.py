__author__ = 'kirry'
from Methods.LoginTools import LoginTools
from Methods.OtherTools import OtherTools
from Methods.MemcacheTools import MemcacheTools
import unittest
import datetime, time
from selenium import webdriver
from Methods.WebDriverTools import WebDriverTools
from config import app
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
class Case111(unittest.TestCase):
    testCaseID = 'Case111'
    projectName = "不针对项目"
    buzName = '检查官网页面内容'
    url = "http://www.rnbtechgroup.com/"


    def setUp(self):
        self.start = datetime.datetime.now()
        self.startTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(" ")[-1]
        MemcacheTools.setMemTime(self.testCaseID, {'start':self.startTime})
        self.driver = webdriver.Chrome()


    def Test(self):
        error = []
        a = WebDriverTools()
        driver = self.driver
        driver.maximize_window()
        try:
            driver.get(self.url)
        except Exception as e:
            print(e.__str__())
            error.append("打开链接%s页面失败！"%self.url)
        try:
            WebDriverWait(driver,10).until_not(lambda x:x.find_element_by_css_selector(".loadingMask"))
        except Exception as e:
            print(e.__str__())
            error.append("打开页面等待10s后没有完全加载！")
        topele = driver.find_elements_by_css_selector(".hd-bar.no-style.inline>li")
        if topele.__len__() != 6:
            error.append("官网首页上边中缺少组件！")
        #检查语言下拉框
        selectbutton = driver.find_element_by_css_selector("#divLanguage")
        ActionChains(driver).move_to_element(selectbutton).perform()
        try:
            selectbutton.find_elements_by_css_selector("ul>li")[1].click()
        except Exception as e:
            print(e.__str__())
            error.append("鼠标放在语言按钮上边，没有弹出下拉框！")
        topText = driver.find_element_by_css_selector(".container.clearfix").text.replace("中文","")
        import re
        zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
        #一个小应用，判断一段文本中是否包含简体中
        match = zhPattern.search(topText)
        if not match:
            print("表头数据正常！")
        else:
            error.append("切换到英文模式表头的数据中含有汉字！")
        for i in range(6):
            topele = driver.find_elements_by_css_selector(".hd-bar.no-style.inline>li")[i]
            texts = topele.text
            if i != 0:
                topele.click()
            try:
                WebDriverWait(driver,10).until_not(lambda x:x.find_element_by_css_selector(".loadingMask"))
            except Exception as e:
                print(e.__str__())
                error.append("%s页面加载图片不完全！"%texts)
            text = driver.find_element_by_css_selector(".main-wrap")
            a.checkNull(text,error,"官网",texts)
        OtherTools.raiseError(error)
    def tearDown(self):
        self.start = str((datetime.datetime.now() - self.start).seconds)
        self.start = self.start + "s"
        self.now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(" ")[-1]
        self.driver.quit()
        MemcacheTools.setMemTime(self.testCaseID,{'start':self.startTime,'end':self.now})


if __name__ == "__main__":
    while 1:
        suite = unittest.TestSuite()
        suite.addTest(Case111('Test'))
        runner = unittest.TextTestRunner()
        runner.run(suite)