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
class Case102(unittest.TestCase):
    testCaseID = "Case102"
    projectName = "光明乳业"
    buzName = "选中一个点,点击轨迹回放,有轨迹曲线,切换日期,拖拽控件处时间也应该变,回到地图是否可用"
    now = 'None'
    url = "http://%s" % app.config['SERVERIP']
    points=[("9L1227","#navPoint_20020000000271","20020000000271"),("9L1228","#navPoint_20020000000272","20020000000272"),("9L1423","#navPoint_20020000000001","20020000000001")]
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
        WebDriverTools.enterProject(driver,425,projName=self.projectName,errors=self.errors)
        WebDriverTools.switchToIframe(driver,self.testCaseID,pageName=self.page)
        driver.find_element_by_css_selector("#movePointBtn").click()
        sleep(2)
        for p in self.points:
            self.check(driver,p[0],p[1],p[2])
        if self.points[0][0] and self.points[1][0] and self.points[1][0] in str(self.errors):
            OtherTools.raiseError(self.errors)

    def check(self,driver,point,id,path_id):
        driver.find_element_by_css_selector(id).click()
        sleep(10)
        js="div[_id='"+path_id+"']>.dataContainer>button"
        driver.find_element_by_css_selector(js).click()
        sleep(5)
        self.checkPath(driver,point)
        yes=datetime.datetime.now()-datetime.timedelta(days=1)
        start=datetime.datetime.strftime(yes, '%Y-%m-%d 00:00')
        end=datetime.datetime.strftime(yes, '%Y-%m-%d 23:59')
        driver.execute_script("$('.startTime >input').attr('value','"+start+"')")
        driver.execute_script("$('.endTime>input').attr('value','"+end+"')")
        driver.execute_script("$('.selectBtn.btn.btn-success').click()")
        start_down=driver.find_element_by_css_selector(".currentStartDate").text
        end_down=driver.find_element_by_css_selector(".currentEndDate").text
        if(start==start_down and end==end_down):
            print("时间正确")
        else:
            self.errors.append("切换日期,拖拽控件处的时间没有改变")
        sleep(5)
        self.checkPath(driver,point)
        driver.find_element_by_css_selector(".backMap.btn.btn-primary").click()
        try:
            sleep(3)
            driver.find_element_by_css_selector("div[_id='%s']"%path_id)
            print('转回到地图了')
        except Exception as e:
            self.errors.append("点击回到地图没有返回到地图页面")

    def checkPath(self,driver,point):
        try:
            sleep(10)
            path=driver.find_element_by_css_selector("svg>path")
            print("历史轨迹路线出来了")
        except Exception as e:
            self.errors.append("%s这个移动点的历史轨迹路线没有出来"%point)



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
    suit.addTest(Case102('Test'))
    runner = unittest.TextTestRunner()
    runner.run(suit)
