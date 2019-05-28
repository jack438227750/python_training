# --*--coding:utf-8--*--
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import unittest
import selenium
import time
import HtmlTestRunner  # 生成HTML格式的测试报告
import sys
sys.path.append(r'D:\AppTest')
from models.swipescreen import SwipeScreen


class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # return super().setUpClass()
        print('selenium versions is : %s' % selenium.__version__)
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.1'
        # 设备名称。如果是真机，在'设置->关于手机->设备名称'里查看
        desired_caps['deviceName'] = '127.0.0.1:62001'
        desired_caps['appPackage'] = 'com.jm.video'
        # desired_caps['appPackage'] = 'com.tencent.mm'
        # desired_caps['app'] = 'F:// debug.apk'
        desired_caps['appActivity'] = 'com.jm.video.ui.main.SplashActivity'
        # desired_caps['appActivity'] = 'com.tencent.mm.ui.LauncherUI'
        cls.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',
                                      desired_caps)
        cls.driver.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        # return super().tearDownClass()
        print('已完成自动化测试！')
        cls.driver.quit()

    def test_something(self, n=4):
        print('test_something click ------ ')
        op = SwipeScreen(self.driver)
        num = 0
        while True:
            if (num == 2):
                time.sleep(1)
                break
            else:
                try:
                    WebDriverWait(self.driver,
                                  5).until(lambda x: x.find_element_by_id(
                                      'com.jm.video:id/imgClose')).click()
                except Exception as e:
                    print('红包提示框没有出现！' + str(e))
                time.sleep(15)
                op.swipeToUp()
                num += 1
        # self.driver.find_element_by_xpath(
        # '//android.widget.TextView[contains(@text,"任务")]').click()
        # timeset = time.strftime('%Y%m%d%H%M%S',
        #                         time.localtime(time.time()))  # 格式化时间
        # pic_name = r'D:\AppTest\screenshots\img' + timeset + '.png'
        pic_name = r'D:\AppTest\screenshots\\' + sys._getframe().f_code.co_name + ' (__main__.MyTestCase)' + '.png'
        self.driver.get_screenshot_as_file(pic_name)
        self.driver.find_element_by_android_uiautomator('text("任务")').click()
        time.sleep(5)
        # find_element_by_android_uiautomator使用方法
        # driver.find_element_by_android_uiautomator('text("Custom View")').click()         #text
        # driver.find_element_by_android_uiautomator('textContains("View")').click()        #textContains
        # driver.find_element_by_android_uiautomator('textStartsWith("Custom")').click()    #textStartsWith
        # driver.find_element_by_android_uiautomator('textMatches("^Custom.*")').click()    #textMatches
        # x0 = window['width'] * 3/4  # 起始x坐标
        # x1 = window['width'] / 4  # 终止x坐标
        # y = window['height'] /2  # y坐标
        # print('x0: %d, x1: %d, y: %d' % (x0, x1, y))
        # for i in range(n):
        #     try:
        #         self.driver.swipe(x0, y, x1, y,duration=time.sleep(2))
        #         time.sleep(1)
        #     except Exception as e:
        #         print('出错了，错误如下：' + str(e))
        # button = self.driver.find_element_by_id(
        #     "com.youdao.calculator:id/guide_button")
        # button.click()
        # for i in range(6):
        #     self.driver.find_element_by_accessibility_id(
        #         'Mathbot Editor').click()
        #     time.sleep(1)
        # btn_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout[3]/android.view.View/android.widget.GridView/android.widget.FrameLayout[{0}]/android.widget.FrameLayout'
        # self.driver.find_element_by_xpath(btn_xpath.format(7)).click()
        # self.driver.find_element_by_xpath(btn_xpath.format(10)).click()
        # self.driver.find_element_by_xpath(btn_xpath.format(8)).click()


if (__name__ == '__main__'):
    unittest.main(
        testRunner=HtmlTestRunner.HTMLTestRunner(output='webchat_report', report_title='Android测试报告'))
