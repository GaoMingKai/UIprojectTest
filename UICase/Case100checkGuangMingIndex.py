__author__ = 'sophia'
import unittest
import datetime, time
from Methods.LoginTools import LoginTools
from Methods.MemcacheTools import MemcacheTools
from Methods.WebDriverTools import WebDriverTools
from Methods.OtherTools import OtherTools
from config import app
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
class Case100(unittest.TestCase):
    testCaseID = "Case100"
    projectName = "光明乳业"
    buzName = "检查首页选中设备不要弹出 no history data,选中设备后右侧出现详情以及温度趋势和合格率趋势的显示,搜索框可以用 "
    now = 'None'
    url = "http://%s" % app.config['SERVERIP']
    points=[("9L1227","#navPoint_20020000000271"),("9L1228","#navPoint_20020000000272"),("9L1423","#navPoint_20020000000001")]
    page=["光明首页"]
    def setUp(self):
        self.start = datetime.datetime.now()
        self.startTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(" ")[-1]
        MemcacheTools.setMemTime(self.testCaseID,{"startTime":self.startTime})
        lg = LoginTools()
        self.driver = lg.InitialChrome(self.url, self.testCaseID)
        self.driver = lg.login(self.driver,user="guangming")
        self.tools = WebDriverTools()


    def Test(self):
        driver = self.driver
        self.errors = []
        self.check(driver)
        for p in self.points:
            self.checkPoint(driver,p[0],p[1])
        if self.points[0][0] and self.points[1][0] and self.points[1][0] in str(self.errors):
            OtherTools.raiseError(self.errors)

    def check(self,driver):
        WebDriverTools.enterProject(driver,425,projName=self.projectName,errors=self.errors)
        iframe = driver.find_element_by_tag_name("iframe")
        driver.switch_to_frame(iframe)
        ele=driver.find_element_by_css_selector(".pointList")
        WebDriverTools.checkNull(ele,self.errors,self.page,"点击固定点左侧设备名称")
        driver.find_element_by_css_selector("#movePointBtn").click()
        sleep(2)
        ele=driver.find_elements_by_css_selector(".pointList")[1]
        WebDriverTools.checkNull(ele,self.errors,self.page,"点击移动点左侧设备名称")

    def checkPoint(self,driver,point,id):
        driver.find_element_by_id("pointTitleIpt").clear()
        driver.find_element_by_id("pointTitleIpt").send_keys(point)
        driver.find_element_by_id("pointSearch").click()
        sleep(2)
        driver.find_element_by_css_selector(id).click()
        try:
            nohistroy=driver.find_element_by_css_selector(".infoBox.infoBox-unique.infoBoxAlert")
            self.errors.append("点击设备弹出了没有历史数据的对话框")
        except Exception as e:
            print("没有出现对话框")
        sleep(2)
        WebDriverTools.checkCanvas(driver,self.errors,self.page)
        canvas=driver.find_elements_by_tag_name("canvas")
        if(len(canvas)==2):
            print("合格率曲线和温度曲线都出来了")
        else:
            self.errors.append("%s合格率曲线或温度曲线没有显示出来" %point)
        ele=driver.find_element_by_id("MFPointContainer")
        WebDriverTools.checkNull(ele,self.errors,self.page,"选中设备后页面右侧")

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
    suit = unittest.TestSuite()
    suit.addTest(Case100('Test'))
    runner = unittest.TextTestRunner()
    runner.run(suit)
