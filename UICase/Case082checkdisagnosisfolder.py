__author__ = 'sophia'
import unittest
import datetime
import time
from time import sleep

from Methods.LoginTools import LoginTools
from Methods.OtherTools import OtherTools
from Methods.MemcacheTools import MemcacheTools
from Methods.WebDriverTools import WebDriverTools
from config import app
from selenium.webdriver.common.keys import Keys

class Case082(unittest.TestCase):
    testCaseID = "Case082"
    projectName = "中芯国际"
    buzName = "检查数据诊断诊断文件夹,增删改"
    now = 'None'
    url = "http://%s" % app.config['SERVERIP']
    project = [1, "上海中芯国际"]

    def setUp(self):
        self.start = datetime.datetime.now()
        self.startTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split(" ")[-1]
        MemcacheTools.setMemTime(self.testCaseID, {"startTime": self.startTime})
        lg = LoginTools()
        self.driver = lg.InitialChrome(self.url, self.testCaseID)
        self.driver = lg.login(self.driver)

    def Test(self):
        driver = self.driver
        self.errors = []
        WebDriverTools.enterProject(driver, self.project[0], self.projectName, self.errors)
        sleep(3)
        self.check(driver)
        OtherTools.raiseError(self.errors)

    def check(self, driver):
        now= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        WebDriverTools.enterModuleByUserMenu(driver, 'btnPointManager', '数据管理', '#dataManagerCloudMenu')
        sleep(5)
        driver.find_elements_by_css_selector('.pointManagerCloudPointUl')[3].find_elements_by_css_selector('li')[-1].click()
        sleep(5)
        be_len = driver.execute_script("be_len=$('#diagnosisFilesUl >li').length;return be_len;")
        driver.execute_script("$('#addTreeFolder').click()")
        driver.execute_script("$('input[class=\"form-control\"]').val('"+now+"')")
        driver.execute_script("$('.infoBox-footer >button')[0].click()")
        sleep(5)
        af_len = driver.execute_script("af_len=$('#diagnosisFilesUl >li').length;return af_len;")
        if (af_len - be_len == 1):
            print('新建诊断文件夹成功')
        else:
            self.errors.append('新建诊断文件夹失败')

        driver.execute_script("$('#diagnosisFilesUl >li>a').last().click()")
        driver.execute_script("$('span[title=\"rename\"]').click()")
        driver.find_element_by_css_selector('input[class="form-control"]').clear()
        driver.find_element_by_css_selector('input[class="form-control"]').send_keys("UI")
        driver.find_elements_by_css_selector('.btn.btn-info.alert-button')[0].click()
        sleep(3)
        name = driver.execute_script("name=$('#diagnosisFilesUl >li >a').last().attr('title');return name;")
        if (name == 'UI'):
            print('更改文件夹名字成功')
        else:
            self.errors.append('更改文件夹名字失败')
        driver.execute_script("$('.cp.button.treeCustomIcon.removeNode').click()")
        driver.execute_script("$('.infoBox-footer >button')[0].click()")
        sleep(5)
        delete_len = driver.execute_script("delete_len=$('#diagnosisFilesUl >li').length;return delete_len;")
        if (delete_len == be_len):
            print('删除文件夹成功')
        else:
            self.errors.append('删除文件夹失败')

    def tearDown(self):
        text=str([x[1] for x in self._outcome.errors if x[1]!=None])
        if "Exception" in text or "AssertionError" in text or self.errors!=[]:
            WebDriverTools.get_pic(self.driver, self.testCaseID)
        self.start = str((datetime.datetime.now() - self.start).seconds)
        self.start = self.start + "s"
        self.now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split(" ")[-1]
        self.driver.quit()
        MemcacheTools.setMemTime(self.testCaseID, {'start': self.startTime, 'end': self.now})


if __name__ == "__main__":
    suit = unittest.TestSuite()
    suit.addTest(Case082('Test'))
    runner = unittest.TextTestRunner()
    runner.run(suit)
