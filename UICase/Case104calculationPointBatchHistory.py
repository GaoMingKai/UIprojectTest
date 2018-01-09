__author__ = 'sophia'

import datetime
import time
import unittest
from time import sleep
from selenium.webdriver.common.keys import Keys
from Methods.LoginTools import LoginTools
from Methods.MemcacheTools import MemcacheTools
from Methods.WebDriverTools import WebDriverTools
from config import app
from Methods.OtherTools import OtherTools


class Case104(unittest.TestCase):
    testCaseID = 'Case104'
    projectName = "49Mytest"
    buzName = '计算点补数据后看不到任务列表'
    start = 0.0
    now = 'None'
    startTime = ""
    url = "http://%s" % app.config['SERVERIP']
    def setUp(self):

        self.start = datetime.datetime.now()
        self.startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split(" ")[-1]
        MemcacheTools.setMemTime(self.testCaseID, {'start': self.startTime})
        lg = LoginTools()
        self.driver = lg.InitialChrome(self.url, self.testCaseID)
        self.driver = lg.login(self.driver)

    def Test(self):
        sleep(2)
        self.errors=[]
        driver = self.driver
        # 进入Mytest导出数据页面
        WebDriverTools.enterProject(driver,"49",self.projectName,self.errors)
        WebDriverTools.enterModuleByUserMenu(driver,"btnPointManager","数据管理","#dataManagerCloudMenu")
        self.check(driver)
        OtherTools.raiseError(self.errors)

    def check(self,driver):
        sleep(4)
        ele = driver.find_elements_by_css_selector('.pointManagerCloudPointUl')[1].find_elements_by_css_selector("li")[2]
        ele.click()
        sleep(3)
        table = driver.find_elements_by_css_selector('.table.table-bordered.table-striped')[1]
        tr=table.find_elements_by_css_selector("tbody >tr")[0]
        tr.click()
        driver.find_element_by_css_selector("#batch_history").click()
        sleep(10)
        inputele1 = driver.find_element_by_id("batchHistoryTimeStart")
        inputele2 =driver.find_element_by_id("batchHistoryTimeEnd")
        buttonele = driver.find_element_by_id("batchHistoryGenerate")
        endTime = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H:%M")
        endTime2 = datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d %H")
        inputele1.clear()
        inputele1.send_keys(endTime)
        inputele2.clear()
        inputele2.send_keys(endTime)
        buttonele.click()
        sleep(2)
        driver.find_element_by_css_selector(".infoBox-footer >button").click()
        sleep(15)
        td=driver.find_elements_by_css_selector(".table.table-striped")[0].find_elements_by_css_selector("tbody >tr>td")[2]
        if(endTime2 in td.text):
            print("计算点补数之后任务列表中存在")
        else:
            assert 0,"补数之后任务列表中不存在"


    def tearDown(self):
        text=str([x[1] for x in self._outcome.errors if x[1]!=None])
        if "Exception" in text or "AssertionError" in text or self.errors!=[]:
            WebDriverTools.get_pic(self.driver, self.testCaseID)
        self.start = str((datetime.datetime.now() - self.start).seconds)
        self.start = self.start + "s"
        self.now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split(" ")[-1]
        MemcacheTools.setMemTime(self.testCaseID, {'start': self.startTime, 'end': self.now})
        self.driver.quit()


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Case104('Test'))
    runner = unittest.TextTestRunner()
    runner.run(suite)