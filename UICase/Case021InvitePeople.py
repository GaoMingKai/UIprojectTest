__author__ = 'wuranxu'
from Methods.WebDriverTools import WebDriverTools
from Methods.MemcacheTools import MemcacheTools
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import datetime, time, string, random
from Methods.LoginTools import LoginTools
from config import app
from selenium.webdriver.common.keys import Keys
import unittest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium import webdriver
import poplib



class Case021(unittest.TestCase):
    testCaseID = 'Case021'
    projectName = "不针对项目"
    buzName = '使用Kingsley账号邀请用户注册'
    start = 0.0
    now = 'None'
    startTime = ""
    url = "http://%s" % app.config['SERVERIP']
    def setUp(self):
        self.start = datetime.datetime.now()
        self.startTime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(" ")[-1]
        MemcacheTools.setMemTime(self.testCaseID,{'start':self.startTime})
        lg = LoginTools()
        self.driver = lg.InitialChrome(self.url, self.testCaseID)
        self.driver = lg.login(self.driver)

    def Test(self):
        #进入上海华为首页
        a = WebDriverTools()
        driver = self.driver
        #driver.implicitly_wait(8)
        time.sleep(4)
        #点击用户菜单
        driver.find_element_by_id("iconList").click()
        #进入员工管理界面
        driver.find_element_by_id("btnMemberManage").click()
        #找到是否有woody用户存在，如果有则删除
        rv = self.deleteNewUser(driver)
        WebDriverWait(driver,5).until(lambda x: x.find_element_by_class_name("addPersonTxt"))
        #self.addPeople(driver)
        if rv:
            self.addPeople(driver)
            driver.find_elements_by_css_selector(".infoBox-footer >button")[0].click()
            time.sleep(3)
            try:
                elements = driver.find_elements_by_class_name("succeed")
                elements2 = driver.find_elements_by_css_selector(".registered")
                if elements != []:
                    print(elements[0].text)
                elif elements2 != []:
                    print(elements2[0].text)
                    self.deleteNewUser(driver)
                    time.sleep(3)
                    self.addPeople(driver)
                else:
                    pass
                    #print(driver.find_element_by_class_name("invited").text)
            except Exception:
                driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
                assert 0,"添加用户->填写用户名和邮箱之后点击发送按钮失败或该用户已注册!"
        else:
            driver.find_element_by_css_selector(".re-invite.bg-info.cp").click()
        driver.close()
        self.CheckEmail()
        self.checkSenderMail()


    def CheckEmail(self):
        dr = webdriver.Chrome()
        dr.get("http://mail.qq.com")
        dr.maximize_window()
        #点击切换到账号密码登陆
        time.sleep(5)
        dr.switch_to.frame(dr.find_element_by_id("login_frame"))
        dr.find_element_by_id("switcher_plogin").click()
        time.sleep(5)
        dr.implicitly_wait(8)
        ele = dr.find_elements_by_class_name("inputOuter")
        time.sleep(5)
        dr.find_element_by_css_selector("#uinArea>div>input").send_keys("55497569@qq.com")
        dr.find_element_by_css_selector("#pwdArea>div input").send_keys("woody312")
        dr.find_element_by_id("login_button").click()
        time.sleep(2)
        x = WebDriverTools()
        while 1:
            if x.isElementPresent(dr,'#useraddr'):
                dr.switch_to.frame(dr.find_element_by_id("mainFrame"))
                break
            else:
                dr.find_element_by_id("login_button").click()
                time.sleep(4)
        WebDriverWait(dr,15).until(lambda x : x.find_element_by_css_selector("li[class='mailinfo1 t_left2'] >div>a"))
        time.sleep(5)
        dr.find_element_by_css_selector("li[class='mailinfo1 t_left2'] >div>a").click()
        WebDriverWait(dr,15).until(lambda x : x.find_elements_by_css_selector(".toarea table"))
        #进入第一封邮件
        dr.find_elements_by_css_selector(".toarea table")[0].click()
        # time.sleep(5)
        url = dr.find_element_by_css_selector(".contentEditable>a").get_attribute("href")
        # eles = dr.find_elements_by_css_selector(".contentEditable a")
        # for ele in eles:
        #     if ele.text is not None and "http://beop" in ele.text:
        #         print("find register url!")
        #         url = ele.text
        allmessage = [message.text for message in dr.find_elements_by_css_selector(".loginBox")]
        username = allmessage[0].split(":")[-1] if "登录名" in allmessage[0] else allmessage[1].split(":")[-1]
        passwd = allmessage[0].split(":")[-1] if "密码" in allmessage[0] else allmessage[1].split(":")[-1]
        dr.get(url)
        time.sleep(7)
        try:
            WebDriverWait(dr,8).until(lambda x:x.find_element_by_id("txtName"))
        except Exception as e:
            print(e)
            dr.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
            assert 0,"邀请用户注册->用户打开邮件后进入登录页面失败!(等待10秒)"
            dr.close()
        # dr.find_element_by_id("inputPassword1").send_keys("h=Lp4U8+Lp")
        # dr.find_element_by_id("inputPassword2").send_keys("h=Lp4U8+Lp")
        # dr.find_element_by_id("submitBtn").click()
        # time.sleep(20)
        # try:
        #     if dr.find_element_by_id("submitBtn"):
        #         assert 0,"邀请用户注册页面->点击提交按钮进行注册的时候,一直显示正在注册中!"
        # except Exception:
        #     pass
        #     # assert 0,"邀请用户注册页面->点击提交按钮进行注册的时候,一直显示正在注册中!"
        # if x.isElementPresent(dr,'#txtName'):
        #     print('登录页存在!')

        dr.find_element_by_id("txtName").clear()
        dr.find_element_by_id("txtName").send_keys(username.strip())
        dr.find_element_by_id("txtPwd").clear()
        dr.find_element_by_id("txtPwd").send_keys(passwd.strip())
        dr.find_element_by_id("btnLogin").click()
        a2 = WebDriverTools()
        #cur_time = time.time()
        self.find_alert(dr)
        #a2.find_spinner(dr, cur_time, project='新注册用户登陆页面', timeout='23',name='spinner')
        try:
            WebDriverWait(dr,20).until_not(lambda x: x.find_element_by_css_selector(".loadingMask"))
        except:
            time.sleep(5)
        try:
            dr.find_element_by_css_selector('#iconList').click()
            user = dr.find_element_by_id('paneUser')
        except Exception:
            assert 0, '登录用户名显示失败'
        name = user.text
        namenow = "Woody"
        if name == namenow:
            pass
        else:
            dr.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
            assert 0, '登录用户与显示的用户不一致'

        time.sleep(5)
        dr.quit()
        dr = webdriver.Chrome()
        dr.implicitly_wait(8)
        dr.get(self.url)
        time.sleep(10)
        dr.maximize_window()
        time.sleep(5)
        lg = LoginTools()
        dr = lg.login(dr)
        WebDriverWait(dr,20).until(lambda x: x.find_element_by_id("iconList"))
        time.sleep(5)
        #点击用户菜单
        dr.find_element_by_id("iconList").click()
        time.sleep(2)
        #进入员工管理界面
        dr.find_element_by_id("btnMemberManage").click()
        WebDriverWait(dr,5).until(lambda x: x.find_element_by_class_name("addPersonTxt"))
        '''names = dr.find_elements_by_css_selector(".userfullname")
        for name in names:
            if name.text == "Woody":
                name.find_element_by_xpath("../../dt[@class='setting']").click()'''
        dr.find_elements_by_css_selector('.setting')[-1].click()
        time.sleep(4)
        dr.find_element_by_id("userDel").click()

        time.sleep(1)
        dr.find_element_by_id("deleteUser").click()
        dr.quit()


    def deleteNewUser(self,dr):
        #点击用户菜单
        dr.find_element_by_id("iconList").click()
        #进入员工管理界面
        dr.find_element_by_id("btnMemberManage").click()
        WebDriverWait(dr,5).until(lambda x: x.find_element_by_class_name("addPersonTxt"))
        names = dr.find_elements_by_css_selector("#treeUl>li>ul>li")
        for name in names:
            texts = name.text
            if "Woody" in texts:
                if  '已过期' in texts:
                    #dr.find_element_by_css_selector('.re-invite.bg-info.cp').click()
                    return False
                else:
                    name.find_element_by_tag_name("img").click()
                    time.sleep(1)
                    dr.find_element_by_id("userDel").click()
                    time.sleep(1)
                    dr.find_element_by_id("deleteUser").click()
                    time.sleep(3)
                    print("删除用户woody成功!")
                    return False

    def addPeople(self,driver):
        #点击用户菜单
        #driver.find_element_by_id("iconList").click()
        #进入添加人员界面
        driver.find_element_by_class_name("addPersonTxt").click()
        #选择直属上级为admin
        time.sleep(8)
        Select(driver.find_element_by_id("selectSupervisor")).select_by_value("2265")
        time.sleep(3)
        #设置初始项目为中芯国际
        selectPeople = driver.find_element_by_id("selectInitProject")
        Select(selectPeople).select_by_value("1")
        time.sleep(1)
        try:
            #设置初始分组为RNB研发
            Select(driver.find_element_by_id("selectInitRole")).select_by_value("1")
        except Exception:
            assert 0,"%s--%s--添加人员--设置初始分组时出错,找不到RNB研发" % (self.testCaseID,self.buzName)
        time.sleep(1)
        #设置用户名和邮箱
        driver.find_element_by_css_selector("#directUserInfos>li>input:nth-child(1)").send_keys("Woody")
        time.sleep(1)
        driver.find_element_by_css_selector("#directUserInfos>li>input:nth-child(2)").send_keys("Woody")
        time.sleep(1)
        driver.find_element_by_css_selector("#directUserInfos>li>input:nth-child(3)").send_keys("h=Lp4U8+Lp")
        time.sleep(1)
        driver.find_element_by_css_selector("#directUserInfos>li>input:nth-child(4)").send_keys("55497569@qq.com")
        #点击确认按钮
        driver.find_element_by_id("addPersonOK").click()
        time.sleep(1)
        driver.find_element_by_css_selector(".btn.btn-info.alert-button:nth-child(1)").click()
        # try:
        #     driver.find_elements_by_css_selector('.modal-footer.tc>button')[0].click()
        # except:
        #     pass
        time.sleep(5)


    def find_alert(self,driver):
        curtime = time.time()
        while 1:
            ele = driver.find_elements_by_css_selector(".alert-msg")
            if time.time() - curtime > float(5):
                break
            if ele == []:
                continue
            else:
                time.sleep(1)
                driver.get_screenshot_as_file(r'.\ErrorPicture\%s\%s.png' % (self.testCaseID,time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())))
                assert 0,'新用户填写注册信息后->等待5秒自动跳转到Beop平台->直接登陆提示用户名或密码错误!注册成功后已等待20秒!'

    #检查邀请人的邮箱有没有收到发送的注册链接的邮件
    def checkSenderMail(self):
        try:
            pop3_server="pop3.rnbtech.com.hk"
            email="projecttest@rnbtech.com.hk"
            password="Rnbtech1103"
            # 连接到POP3服务器:
            server = poplib.POP3(pop3_server)
            # 身份认证:
            server.user(email)
            server.pass_(password)
            resp, mails, octets = server.list()
            forth_message = server.retr(len(mails))
            server.quit()
            mess1=forth_message[1][33].decode('utf-8')
            mess2=forth_message[1][9].decode('utf-8')
            mail_time=mess2.split(': ')[1]
            mailtime=datetime.datetime.strptime(mail_time[5:24],'%d %b %Y %H:%M:%S')
            hour=mailtime.hour
            minu=mailtime.minute
            now=datetime.datetime.now()
            if('邀请您加入BeOP云平台' in mess1 and hour==now.hour):
                print('邮件发送到邮箱中了')
            else:
                assert 0,'邀请人邮箱里面没有收到邀请您加入BeOP云平台的邮件'
        except Exception as e:
            print(e.__str__())
            assert 0,'receiveMail error:'+e.__str__()

    def tearDown(self):
        text=str([x[1] for x in self._outcome.errors if x[1]!=None])
        if "Exception" in text or "AssertionError" in text:
            WebDriverTools.get_pic(self.driver, self.testCaseID)
        #self.driver.quit()
        self.start = str((datetime.datetime.now() - self.start).seconds)
        self.start = self.start + "s"
        self.now = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()).split(" ")[-1]
        MemcacheTools.setMemTime(self.testCaseID,{'start':self.startTime,'end':self.now})


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Case021('Test'))
    runner = unittest.TextTestRunner()
    runner.run(suite)