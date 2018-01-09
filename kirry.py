from flask import Flask
import unittest
app = Flask(__name__)


class Test():
    name = "test"
    passwd = "12345678"
    email = "16578167845@qq.com"


class Case001(Test,unittest.TestCase):
    two = "joker"
    def setUp(self):
        pass
    def tearDown(self):
        pass


class Case002(Test,unittest.TestCase):
    two = "joker"
    def setUp(self):
        pass
    def tearDown(self):
        pass



class default(Test):
    def __init__(self):
        self.name = ""


test = {
    "Test":Test(),
    "Case001":Case001()
}

