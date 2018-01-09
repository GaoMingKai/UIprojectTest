import os


# def listdir(level,path):
#     for i in os.listdir(path):
#         print(" "*(level+1)+i)
#         if os.path.isdir(path+'\\'+i):
#             listdir(level+1,path+"\\"+i)
# rootpath = os.path.abspath(".")
# print(rootpath)
# listdir(0,rootpath)
# def test(n):
#     yield {0:"test",1:"test1",2:"test2"}.get(n,"没有该数字！")
#
# x = 5
# y = 6
# x,y = y,x
# for i in range(5):
#     kk=test(1)
#     print(kk)

# def fib():
#     a,b = 0,1
#     for i in range(10):
#         print("test")
#         yield a
#         a,b = b,a+b
#         print("test%s"%a)
#
# a = fib()
# print(a)




# from enum import Enum
#
# class Test(Enum):
#     one = 1
#     two = 2
#     three = 3
#     four = 4
#     five = 5
# sessoin = Enum("Test",)


##收邮件《。。。。。。》


import poplib

emaill = poplib.POP3_SSL(host="pop.qq.com" )
username = emaill.user("2232502139@qq.com")
passwd = emaill.pass_("dkoepsisrhqdebfa")
emaill.set_debuglevel(1)
emailnumber,emailsize = emaill.stat()
print("email number is %s and size is %s"%(emailnumber,emailsize))
lists = emaill.list()[1]
index = lists.__len__()
#lines =[str(i) for i in email.retr(index)[1]]
resp, lines, octets = emaill.retr(index)
msg_connect = "\r\n".join([line.decode("gbk") for line in lines])
#email.dele(index)
emaill.quit()


import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.mime.multipart import MIMEMultipart
import re

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get("Content-Type","").lower()
        pos = content_type.find("charset=")
        if pos>0:
            charset = content_type[pos+8:].strip()
    return charset

msg = Parser().parsestr(msg_connect)
headers = ["From","To","Subject"]
headers = ["From","To","Subject","Message"]
for header in headers:
    values = msg.get(header,"")
    if values:
        if header == "Subject":
            values = decode_str(values)
    else:
        hdr,adr = parseaddr(values)
        name = decode_str(hdr)
        values = "%s<%s>"%(name,adr)

    if msg.is_multipart():
        parts = msg.get_payload()
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == "text/html":
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content=content.decode(charset)
            print(content)







# import imaplib,string,email
#
# conn = imaplib.IMAP4_SSL("imap.qq.com" )
# conn.login("2232502139@qq.com","dkoepsisrhqdebfa")







import unittest

class Case001(unittest.TestCase):
    test001 = None
    test002 = None



    def  setUpClass(cls):
        pass

    def setUp(self):
        pass
    @unittest.skipIf()
    def Test(self):
        pass
    @unittest.skip
    def Test1(self):
        pass


    def tearDownClass(cls):
        pass


    def tearDown(self):
        pass



















def main():
    hour=datetime.now().hour
    if(1<=hour<=7):
        return None
    bNeedProcess = fault_need_check(60, 60)#若上次检查有错则30分钟后复查，若无错则2小时后复查
    if not bNeedProcess:
        log_str('检查时间间隔未到，不需执行!')
        return None

    errors = []
    log_str('我的测试点')
    num = checjPointupdate(errors)
    if errors and num:
        return reasonAnalysis(errors,num)


def checkPointupdate(error):
    rv = None
    errordata = {}
    data = {"projectId":457,"text":None,"isAdvance":False,"order":"asc","flag":0,"starred":"","item":"time","page_size":200,"current_page":1}
    url = "http://beop.rnbtech.com.hk/admin/dataPointManager/search/"
    try:
        rv = http_post_json_with_cookie(url=url,data=data,t=30)
    except:
        error.append("发送参数%s请求%s接口出错,错误内容为%s!" % (str(data), url, e.__str__()))
    log_str('我的测试点')
    if rv:
        datalist = rv.get("list",False)
        totalnum = rv.get("total",False)
        if datalist and totalnum:
            for num in datalist:
                for i in num:
                    now = datetime.now()
                    pointName = i.get("pointname")
                    pointTime = i.get("time")
                    Times = datetime.strftime(pointTime,"%Y-%m-%d %H:%M:%S")
                    deltimes = (Times-now).total_seconds() if Times>now else (now-Times).total_seconds()/60
                    if deltimes>60:
                        errordata[pointName] = pointTime
            if len(errordata)/len(toatalnum) > 0.1:
                for index,i in enumerate(errordate):
                    error.append(i)
                    if index>5:
                        break
                return len(errordata)
            else:
                return None


def reasonAnalysis(errors,num):
    log_str(errors)
    strWorkOrderName = 'AT报警--calc012'
    dealUserList = ['kirry.gao@rnbtech.com.hk']
    if errors and len(errors)!=0:
        log_str('fail')
        fn = None
        errors = "未更新的点的个数为%s"%num+'<br><br>'.join(errors)
        fn = FaultNotice('TWS项目原始数据60分钟内没有更新', errors, '点值不能及时更新',
                             '验证问题,解决问题使其恢复正常不再延迟更新')
        #send_work_order_smart(strWorkOrderName, fn, dealUserList, 60*24,60,boom=True)
        send_message_by_email(dealUserList,strWorkOrderName , fn.str())
        return fn
    else:
        log_str('success')
        reset_work_order_if_open(strWorkOrderName, dealUserList)
        return True






