__author__ = 'sophia'
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
class Case062(unittest.TestCase):
    testCaseID = 'Case062'
    projectName = "175LiverpoolStreet"
    buzName = '检查首页页面是否正常'
    now = 'None'
    url = "http://%s" % app.config['SERVERIP']
    project = (293,'175LiverpoolStreet')
    def setUp(self):
        self.start = datetime.datetime.now()
        self.startTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(" ")[-1]
        MemcacheTools.setMemTime(self.testCaseID, {'start':self.startTime})
        lg = LoginTools()
        self.driver = lg.InitialChrome(self.url, self.testCaseID)
        self.driver = lg.login(self.driver)
        self.tools = WebDriverTools()

    def Test(self):
        driver = self.driver
        self.errors = []
        self.tools.enterProject(driver, self.project[0], self.project[1], self.errors)
        sleep(3)
        self.checkIndex(driver)
        OtherTools.raiseError(self.errors)

    #检查首页
    def checkIndex(self,driver):
        page=['Home']
        self.tools.enterPage(driver,page,'#paneCenter', self.projectName)
        self.tools.checkWeather(driver,self.errors,page)
        buttons=driver.find_elements_by_css_selector('.btn-group > button')
        sleep(2)
        for index,button in enumerate(buttons):
            button.click()
            lis=driver.find_elements_by_css_selector('.divSysUnit')
            if(index==0):
                lis=lis[0:6]
            else:
                lis=lis[7:11]
            self.tools.checkHoverData(driver,self.errors,lis,page,'KPI显示鼠标放上去')

        #检查slider下面的值
        ele=driver.find_element_by_id('paneEnergyInfo')
        self.tools.checkNull(ele,self.errors,page,'Heating and Cooling Energy Use of Today处')
        ele=driver.find_element_by_id('paneEffectInfo')
        self.tools.checkNull(ele,self.errors,page,'CHW Energy Efficiency Rate处')
        #检查slider
        sleep(15)
        self.tools.checkPageCanvas(driver,page,self.errors)
        lis=driver.find_elements_by_css_selector('ol.carousel-indicators > li')
        for index,li in enumerate(lis):
            if(index!=2):
                li.click()
            sleep(2)
            container=driver.find_elements_by_css_selector('.report-content.clearfix')[index]
            self.tools.checkNull(container,self.errors,page,'第%s个slider处'%(index+1))
            if(index!=0):
                button=driver.find_element_by_css_selector('.item.active > .carousel-caption > .runRept >button')
                button.click()
                leftCtn=WebDriverWait(driver, 10).until(lambda x: x.find_element_by_css_selector('#leftCtn'))
                if('Daily Energy Report' in leftCtn.text):
                    print('点击button可以跳转到Daily Energy Report报表')
                    sleep(2)
                    driver.back()
                    sleep(5)
                    driver.find_elements_by_css_selector('ol.carousel-indicators > li')[2].click()
                else:
                    self.errors.append('点击home页面slider里面的button按钮没有跳转到报表页面')

    def tearDown(self):
        text=str([x[1] for x in self._outcome.errors if x[1]!=None])
        if "Exception" in text or "AssertionError" in text or self.errors!=[]:
            WebDriverTools.get_pic(self.driver, self.testCaseID)
        self.start = str((datetime.datetime.now() - self.start).seconds)
        self.start = self.start + "s"
        self.now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(" ")[-1]
        self.driver.quit()
        MemcacheTools.setMemTime(self.testCaseID,{'start':self.startTime,'end':self.now})

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Case062('Test'))
    runner = unittest.TextTestRunner()
    runner.run(suite)