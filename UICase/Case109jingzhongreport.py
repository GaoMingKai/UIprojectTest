__author__ = "kirrys"
from Methods.LoginTools import LoginTools
from Methods.OtherTools import OtherTools
from Methods.MemcacheTools import MemcacheTools
import unittest,os
import datetime, time
from Methods.WebDriverTools import WebDriverTools
from config import app
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

class Case109(unittest.TestCase):
    testCaseID = "Case109"
    projectName = "金钟广场"
    buzName = "检查运营报表是否正常"
    now = 'None'
    url = "http://%s" % app.config['SERVERIP']
    project = [
        [318,"金钟广场"],
    ]
    page = [
        ["报表"],
    ]
    def setUp(self):
        self.start = datetime.datetime.now()
        self.startTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        MemcacheTools.setMemTime(self.testCaseID,{"startTime":self.startTime})
        lg = LoginTools()
        self.driver = lg.InitialChrome(self.url,self.testCaseID)
        self.driver = lg.login(self.driver)
    def Test(self):
        driver = self.driver
        self.erro = []
        WebDriverTools.enterProject(driver,self.project[0][0],self.project[0][1],self.erro)
        sleep(2)
        WebDriverTools.enterPage(driver,self.page[0],'#leftCtn', self.projectName)
        sleep(2)
        WebDriverTools.CheckoperationReport(driver,self.project[0][1],self.erro)

        OtherTools.raiseError(self.erro)

    def tearDown(self):
        text=str([x[1] for x in self._outcome.errors if x[1]!=None])
        if "Exception" in text or "AssertionError" in text or self.erro!=[]:
            WebDriverTools.get_pic(self.driver, self.testCaseID)
        self.start = str((datetime.datetime.now() - self.start).seconds)
        self.start = self.start + "s"
        self.now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split(" ")[-1]
        MemcacheTools.setMemTime(self.testCaseID, {'start': self.startTime, 'end': self.now})
        self.driver.quit()

if __name__ == "__main__":
    suit = unittest.TestSuite()
    suit.addTest(Case109("Test"))
    runner = unittest.TextTestRunner()
    runner.run(suit)














