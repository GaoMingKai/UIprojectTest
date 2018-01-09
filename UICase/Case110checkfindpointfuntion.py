__author__ = 'kirry'
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
class Case110(unittest.TestCase):
    testCaseID = 'Case110'
    projectName = "上海中芯国际"
    buzName = '检查现场点，虚拟点，计算点搜索点击按钮是否正常'
    now = 'None'
    url = "http://%s" % app.config['SERVERIP']
    project = (1,'上海中芯国际')
    point = {"现场点":"Accum_AvgPointValueCost","虚拟点":"test_kirry","计算点":"Autorepair_Test"}
    pointName = ["现场点","虚拟点","计算点","标记结构"]
    tagpoint = ["Accum_gasmeter_useD_T_confirm_real","AHU"]
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
        self.tools.enterModuleByUserMenu(driver,"btnPointManager","数据管理","#dataManagerCloudMenu")
        self.enterPage(driver,self.errors)



    def enterPage(self,driver,error):
        WebDriverWait(driver,10).until_not(lambda x:x.find_element_by_css_selector(".loadingMask"))
        ele = driver.find_elements_by_css_selector("#dataManagerCloudMenu>li")[1]
        testEle = ele.find_elements_by_css_selector("ul>li")
        for pointName,i in zip(self.pointName,testEle):
            i.click()
            WebDriverWait(driver,10).until_not(lambda x:x.find_element_by_css_selector(".loadingMask"))
            if i != testEle[-1]:
                self.checkfindfunction(driver,self.point[pointName],pointName,self.errors)
            else:
                self.checktagfind(driver,self.errors)

    def checkfindfunction(self,driver,point,pointName,error):
        driver.find_element_by_css_selector("#text_search").clear()
        driver.find_element_by_css_selector("#text_search").send_keys(point)
        driver.find_element_by_css_selector(".text_search_box.ml10>span").click()
        WebDriverWait(driver,10).until_not(lambda x:x.find_element_by_css_selector(".loadingMask"))
        now = driver.find_elements_by_css_selector(".table-body.gray-scrollbar>table>tbody>tr")
        if now.__len__() == 1 and point in [ele.text.split("\n")[0] for ele in now]:
            print("查询点%s点击按钮正常！"%pointName)
        else:
            error.append("%s页面中查询数据错误，查询按钮有误！"%pointName)

    def checktagfind(self,driver,error):
        try:
            driver.find_element_by_css_selector("#finishFolder").click()
            sleep(2)
        except:
            pass
        driver.find_element_by_css_selector("#editFolder").click()
        try:
            WebDriverWait(driver,15).until_not(lambda x:x.find_element_by_css_selector(".loadingMask"))
        except Exception as e:
            assert 0,"编辑页面加载10s超时！"
        driver.find_element_by_css_selector("#searchPointInput").clear()
        driver.find_element_by_css_selector("#searchPointInput").send_keys(self.tagpoint[0])
        driver.find_element_by_css_selector(".icon.iconfont.cp.searchIcon").click()
        WebDriverWait(driver,15).until_not(lambda x:x.find_element_by_css_selector(".loadingMask"))
        now = driver.find_elements_by_css_selector(".table.table-bordered.table-striped>tbody>tr")
        if now.__len__() == 1 and self.tagpoint[0] in [ele.text.split("\n")[0] for ele in now]:
            print("tag标记结构页面查询按钮正常！")
        else:
            error.append("tag标记结构编辑页面中查询数据错误，查询按钮有误！")
        #点击完成进入标记tag页面
        driver.find_element_by_css_selector("#finishFolder").click()
        WebDriverWait(driver,15).until_not(lambda x:x.find_element_by_css_selector(".loadingMask"))
        driver.find_element_by_css_selector("#mode-data-Search").clear()
        driver.find_element_by_css_selector("#mode-data-Search").send_keys(self.tagpoint[0])
        driver.find_element_by_css_selector(".icon.iconfont.icon_position.modeDataSearchIcon.cp.dmPointHover").click()
        WebDriverWait(driver,15).until_not(lambda x:x.find_element_by_css_selector(".loadingMask"))
        now = driver.find_elements_by_css_selector(".table.table-bordered.table-striped>tbody>tr")
        if now.__len__() == 1 and self.tagpoint[0] in [ele.text.split("\n")[0] for ele in now]:
            print("标记tag查询按钮正常！")
        else:
            error.append("标记tag页面中查询数据错误，查询按钮有误！")

        #点击查看tag进入tag查看页面
        driver.find_element_by_css_selector("#check-mode").click()
        WebDriverWait(driver,10).until_not(lambda x:x.find_element_by_css_selector(".loadingMask"))
        driver.find_element_by_css_selector("#mode-data-Search").clear()
        driver.find_element_by_css_selector("#mode-data-Search").send_keys(self.tagpoint[0])
        driver.find_element_by_css_selector(".icon.iconfont.icon_position.modeDataSearchIcon.cp.dmPointHover").click()
        WebDriverWait(driver,10).until_not(lambda x:x.find_element_by_css_selector(".loadingMask"))
        now = driver.find_elements_by_css_selector(".table.table-bordered.table-striped>tbody>tr")
        if now.__len__() == 1 and self.tagpoint[0] in [ele.text.split("\n")[0] for ele in now]:
            print("tag查看页面查询按钮正常！")
        else:
            error.append("tag查看页面中查询数据错误，查询按钮有误！")
        #查询tag分类标签
        driver.find_element_by_css_selector("#tagSearchValue").clear()
        driver.find_element_by_css_selector("#tagSearchValue").send_keys(self.tagpoint[1])
        driver.find_element_by_css_selector("#tagSearchBox>span").click()
        WebDriverWait(driver,10).until_not(lambda x:x.find_element_by_css_selector(".loadingMask"))
        now = driver.find_elements_by_css_selector(".tagTypeBox.active>div>ul")
        if now.__len__() == 1 and self.tagpoint[1] in [i.text for i in now]:
            print("tag分类标签查询按钮正常！")
        else:
            error.append("tag分类标签页面中查询数据错误，查询按钮有误！")
        OtherTools.raiseError(self.errors)






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
    while 1:
        suite = unittest.TestSuite()
        suite.addTest(Case110('Test'))
        runner = unittest.TextTestRunner()
        runner.run(suite)