from Methods.LoginTools import LoginTools
from Methods.OtherTools import OtherTools
from Methods.MemcacheTools import MemcacheTools
import unittest
import datetime, time
from Methods.WebDriverTools import WebDriverTools
from config import app
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

class Case106(unittest.TestCase):
    testCaseID = "Case106"
    projectName = "金钟广场"
    buzName = "检查页面KPI概览是否正常"
    now = 'None'
    url = "http://%s" % app.config['SERVERIP']
    project = [318,"金钟广场"]
    page = ["KPI概览"]
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
        WebDriverTools.enterProject(driver,self.project[0],self.project[1],self.erro)
        WebDriverTools.enterPage(driver,self.page,'#paneCenter', self.projectName)
        self.checkhome(driver)
        OtherTools.raiseError(self.erro)
    def checkhome(self,driver):
        tool=WebDriverTools()
        #检查左侧页面信息
        leftare = driver.find_elements_by_css_selector("#accordion > div")
        for index,ele in enumerate(leftare):
            if index != 0:
                ele.click()
            tool.checkNull(ele,self.erro,self.project[1],ele.text.split("\n")[0])
        #检查页面图片据信息
        tool.checkCanvas(driver,self.erro,self.projectName)
        slidePage = driver.find_elements_by_css_selector("ol.carousel-indicators > li")
        for index,ele in enumerate(slidePage):
            ele.click()
            tool.checkCanvas(driver,self.erro,self.project[-1]+"第%sslide"%(index+1))
    def tearDown(self):
        text=str([x[1] for x in self._outcome.errors if x[1]!=None])
        if "Exception" in text or "AssertionError" in text or self.erro!=[]:
            WebDriverTools.get_pic(self.driver, self.testCaseID)
        self.start = str((datetime.datetime.now() - self.start).seconds)
        self.start = self.start + "s"
        self.now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(" ")[-1]
        self.driver.quit()
        MemcacheTools.setMemTime(self.testCaseID,{'start':self.startTime,'end':self.now})
if __name__ == "__main__":
    suit = unittest.TestSuite()
    suit.addTest(Case106("Test"))
    runner = unittest.TextTestRunner()
    runner.run(suit)














