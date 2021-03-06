#coding=utf-8
__author__ = 'woody'
from Methods.WebDriverTools import WebDriverTools
from Methods.MemcacheTools import MemcacheTools
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import datetime, time, string, random
from Methods.LoginTools import LoginTools
from config import app
from selenium.webdriver.common.keys import Keys
import unittest, os
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium import webdriver




projects = (

    (71, '英文演示06', ['Diagnosis', 'Diagnosis Report'], '#reportNavList', 'old'),
    (175, '演示09', ['Diagnosis', 'Diagnosis Report'], '#reportNavList', 'old'),
    (100, '扬州高露洁', ['运营报告', 'KPI日报'], '#reportNavList', 'old'),
    (90, '顺风光电1号', ['运营报表', 'KPI日报'], '#reportNavList', 'old'),
    #(102, '杭州妇产科医院', ['运营报告', 'KPI日报'], '#reportNavList', 'old'),
    (186, '华滋奔腾大厦', ['运营报告', '运行日报'], '#reportNavList', 'old'),
    (80, '世纪商贸', ['运营报告', '运行日报'], '#reportNavList', 'old'),
    (120, 'MercedesBenz', ['诊断汇总', '诊断报告', '数据质量报表'], '#reportNavList', 'old'),



)


downloadDir = app.config.get('DOWNLOAD_DIR')

class Case051(unittest.TestCase):
    testCaseID = 'Case051'
    projectName= '早班巡查项目2'
    buzName = '检查报表内容以及是否能下载'
    start = 0.0
    now = 'None'
    startTime = ""
    url = 'http://' + app.config['SERVERIP']
    errors = []
    def setUp(self):
        self.start = datetime.datetime.now()
        self.startTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(" ")[-1]
        MemcacheTools.setMemTime(self.testCaseID,{'start':self.startTime})
        lg = LoginTools()
        self.driver = lg.InitialChrome(self.url, self.testCaseID)
        self.driver = lg.login(self.driver)


    def Test(self):
        self.errors = []
        a = WebDriverTools()
        driver = self.driver
        time.sleep(4)
        for proj in projects:
            a.enterProject(driver, proj[0], proj[1], self.errors)
            WebDriverTools.enterPage(driver, proj[2], proj[3], proj[1], timeout=180)
            time.sleep(5)
            if proj[4] == 'old':
                self.checkOld(driver, proj[1])
            else:
                self.checkNew(driver, proj[1])
        #抛出异常
        self.raiseError(self.errors)




    def checkOld(self, driver, projectName):
        a = WebDriverTools()
        time.sleep(2)
        reports = driver.find_elements_by_css_selector("li[class~='list-group-item']")
        if reports == []:
            a.get_pic(driver, self.testCaseID)
            self.errors.append("进入%s项目找不到左侧报表栏!" % projectName)
        for i in range(len(reports)):
            driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].click()
            time.sleep(6)
            WebDriverTools.waitElementNotFound(driver, '.spinnerMask', self.testCaseID)
            contents = driver.find_elements_by_css_selector('#report-unit-1 .report-unit .summary')
            if contents != []:
                textEle = driver.find_element_by_css_selector('.step-play-list')
                WebDriverTools.checkNull(textEle, self.errors, [projectName, driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text], '内容')
                print('%s项目->%s报表存在!' % (projectName, driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text))
                if not i:
                    self.downloadPDF(driver, downloadDir, projectName,
                                     driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text, 'old')
                    self.downloadWORD(driver, downloadDir, projectName,
                                     driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text)
            else:
                reportName = driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text
                if ("月" in reportName or "onth" in reportName or reportName == 'Diagnosis Report' or reportName == '诊断报表') and int(datetime.datetime.now().day) <= 5:
                    print("5号之前月报还没生成!")
                else:
                    WebDriverTools.get_pic(driver, self.testCaseID)
                    self.errors.append('%s项目->%s报表内容为空!' % (projectName, reportName))
            '''txt = driver.find_elements_by_css_selector('#report-unit-1 .report-unit .summary')
            if len(txt) > 0:
                pass
            else:

                driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
                errors.append('%s项目->%s报表内容为空!' % (project,driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text))
                #assert 0,'%s项目->%s报表内容为空!' % (project,driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text)'''


        time.sleep(2)


    def checkNew(self, driver, projectName):
        a = WebDriverTools()
        time.sleep(5)
        reports = driver.find_elements_by_css_selector(".reportListName")
        if reports == []:
            a.get_pic(driver, self.testCaseID)
            self.errors.append("进入%s项目找不到左侧报表栏!" % projectName)
        for i in range(len(reports)):
            driver.find_elements_by_css_selector(".reportListName")[i].click()
            WebDriverTools.waitSpinner(driver, projectName + "报表--%s" % driver.find_elements_by_css_selector('.reportListName a')[i].text, timeout=23)
            time.sleep(1.5)
            contents = driver.find_elements_by_css_selector('.report-container-wrap.report-module-text')
            if contents != []:
                textEle = driver.find_element_by_css_selector(".center.report-wrap.gray-scollbar")
                WebDriverTools.checkNull(textEle, self.errors, [projectName, driver.find_elements_by_css_selector('.reportListName a')[i].text], '内容')
                print('%s项目->%s报表存在!' % (projectName, driver.find_elements_by_css_selector('.reportListName a')[i].text))
                if not i:
                    self.downloadPDF(driver, downloadDir, projectName,
                                     driver.find_elements_by_css_selector('.reportListName a')[i].text, 'new')
            else:
                reportName = driver.find_elements_by_css_selector('.reportListName a')[i].text
                if ("月" in reportName or "onth" in reportName or reportName == 'Diagnosis Report' or reportName == '诊断报表') and int(datetime.datetime.now().day) <= 5:
                    print("5号之前月报还没生成!")
                else:
                    WebDriverTools.get_pic(driver, self.testCaseID)
                    self.errors.append('%s项目->%s报表内容为空!' % (projectName, reportName))
            '''txt = driver.find_elements_by_css_selector('#report-unit-1 .report-unit .summary')
            if len(txt) > 0:
                pass
            else:

                driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
                errors.append('%s项目->%s报表内容为空!' % (project,driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text))
                #assert 0,'%s项目->%s报表内容为空!' % (project,driver.find_elements_by_css_selector("li[class~='list-group-item']")[i].text)'''


        time.sleep(2)


    def downloadPDF(self, driver, dir, project, report, mode):
        status = False
        time.sleep(2)
        #点击下载PDF按钮
        try:
            if mode == 'old':
                driver.find_element_by_id("exportPDF").click()
            else:
                driver.find_element_by_css_selector(".pdfDownCtn.in").click()
            time.sleep(10)
        except Exception as e:
            print(e.__str__())
            WebDriverTools.get_pic(driver, self.testCaseID)
            self.errors.append("%s项目->%s报表下载PDF失败!<br>" % (project, report))
        for root,dirs,files in os.walk(dir):
            for file in files:
                if report in file and '.pdf' in file:
                    status = True
                    break
        if not status:
            print("下载PDF失败!")
            self.errors.append("%s项目->%s报表下载PDF失败!因为下载目录中未包含%s文件!" % (project, report, report))
        else:
            print("下载PDF成功!")




    def downloadWORD(self,driver,dir,project,report):
        status = False
        time.sleep(2)
        #点击下载word按钮
        try:
            driver.find_element_by_id("exportWord").click()
            time.sleep(10)
        except Exception as e:
            print(e.__str__())
            WebDriverTools.get_pic(driver, self.testCaseID)
            self.errors.append("%s项目->%s报表下载PDF失败!<br>" % (project,report))
        for root,dirs,files in os.walk(dir):
            for file in files:
                if report in file and '.doc' in file:
                    status = True
                    break
        if not status:
            print("下载WORD失败!")
            self.errors.append("%s项目->%s报表下载WORD失败!因为下载目录中未包含%s文件!" % (project, report, report))
        else:
            print("下载WORD成功!")





    def raiseError(self,error):
        if error != []:
            assert 0,"<br>".join(error)




    def tearDown(self):
        text=str([x[1] for x in self._outcome.errors if x[1]!=None])
        if "Exception" in text or "AssertionError" in text or self.errors!=[]:
            WebDriverTools.get_pic(self.driver, self.testCaseID)
        self.driver.quit()
        self.start = str((datetime.datetime.now() - self.start).seconds)
        self.start = self.start + "s"
        self.now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(" ")[-1]
        MemcacheTools.setMemTime(self.testCaseID,{'start':self.startTime,'end':self.now})
        #删除下载的PDF文件





if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Case051('Test'))
    runner = unittest.TextTestRunner()
    runner.run(suite)
