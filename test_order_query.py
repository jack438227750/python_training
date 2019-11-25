'''
  Code description：测试订单查询  Create time：2019-4-22  
  Developer：Jack
'''
import re
from basepage import BasePage
from log import Logger
from browser_engine import BrowserEnginee
from readexcel import ExcelUtil
import unittest
from home_page import HomePage
from selenium.common.exceptions import NoSuchElementException
logger = Logger('OrderQuery').getlog()
excle_data = ExcelUtil(r'D:\MesTest\mestest\data\order_el.xlsx', 'Sheet1')


class OrderQuery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        browser = BrowserEnginee(cls)
        cls.driver = browser.open_browser(cls)
        cls.page_el = BasePage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        logger.info('自动测试已结束，详情请查看测试日志！')
        cls.driver.quit()

    # 进入订单信息页面的方法
    def open_order_page(self):
        home_page = HomePage(self.driver)
        self.page_el.sleep(2)
        home_page.user('admin')
        home_page.wait(1)
        home_page.pwd('123123')
        home_page.wait(1)
        home_page.login()
        home_page.wait(1)
        self.menu_base_info = excle_data.get_data(1, 1)  # 基础信息菜单
        self.submenu_order = excle_data.get_data(2, 1)  # 订单子菜单
        self.page_el.click(self.menu_base_info)  # click基础信息菜单
        self.page_el.sleep(1)
        logger.info('点击了菜单：基础信息')
        self.page_el.click(self.submenu_order)  # click订单子菜单
        self.page_el.sleep(1)
        # link = self.page_el.get_el_attr(self.submenu_order,
        #                                 'href')  # 获取订单子菜单要打开的页面链接
        # print(link)
        # self.page_el.open_new_window(link)  # 打开获取的链接，这里是订单信息的全屏窗口
        self.page_el.click(self.submenu_order)        
        self.page_el.sleep(1)
        self.page_el.switch_to_frmae('x=>//*[@id="mainTabStrip_fnode13"]/div/div[1]/iframe')

    # 查询满足一个条件的订单记录
    def test_1_order_info(self):
        self.open_order_page()
        self.page_el.sleep(2)       
        ordernum = excle_data.get_data(3, 2)
        cusid = excle_data.get_data(3, 3)
        prodname = excle_data.get_data(3, 4)
        print('订单号：%s,客户编号：%s,产品名称：%s' % (ordernum, cusid, prodname))
        if (ordernum != '' and cusid == '' and prodname == ''):
            self.page_el.clear('id=>ttbOrderNum-inputEl')
            self.page_el.type('id=>ttbOrderNum-inputEl', ordernum)
            self.page_el.sleep(1)
            self.page_el.click('//*[@id="f10"]/span/span')  # click查询按钮
            logger.info('开始进行查询！')
            self.page_el.sleep(2)
            recordnum = self.page_el.get_text('id=>fineui_7')
            rnum = re.findall('\d+', recordnum)[2]
            logger.info('共查询到了%s条订单记录！' % rnum)
            if (int(rnum) == 1):
                qordernum = self.page_el.get_text(
                    '//*[@id="Grid1"]//table/tbody/tr/td[3]/div')
                self.assertTrue(ordernum in qordernum)
                print('查询结果正确！')
            else:
                for i in range(1, int(rnum) + 1):
                    qordernum = self.page_el.get_text(
                        '//*[@id="Grid1"]//table/tbody/tr[%d]/td[3]/div' % i)
                    self.assertTrue(
                        ordernum in qordernum,
                        msg='查询得到数据与输入的条件不符！查询值是：%s,实际值是：%s' % (ordernum,
                                                                qordernum))
        elif(ordernum == '' and cusid != '' and prodname == ''):
            self.page_el.clear('id=>ttbCustomerID-inputEl')
            self.page_el.type('id=>ttbCustomerID-inputEl', cusid)
            self.page_el.sleep(1)
            self.page_el.click('//*[@id="f10"]/span/span')  # click查询按钮
            logger.info('开始进行查询！')
            self.page_el.sleep(2)
            recordnum = self.page_el.get_text('id=>fineui_7')
            rnum = re.findall('\d+', recordnum)[2]
            logger.info('共查询到了%s条订单记录！' % rnum)
            if (int(rnum) == 1):
                qcusid = self.page_el.get_text(
                    '//*[@id="Grid1"]//table/tbody/tr/td[4]/div')
                self.assertTrue(ordernum in qcusid)
                print('查询结果正确！')
            else:
                for i in range(1, int(rnum) + 1):
                    qcusid = self.page_el.get_text(
                        '//*[@id="Grid1"]//table/tbody/tr[%d]/td[4]/div' % i)
                    self.assertTrue(
                        cusid in qcusid,
                        msg='查询得到数据与输入的条件不符！查询值是：%s,实际值是：%s' % (cusid,
                                                                qcusid))

    # 查询满足三个条件的订单记录
    def test_2_order_info(self):
        # page_el = BasePage(self.driver)
        # self.open_order_page()
        ordernum = excle_data.get_data(1, 2)
        cusid = excle_data.get_data(1, 3)
        prodname = excle_data.get_data(1, 4)
        self.page_el.clear('id=>ttbOrderNum-inputEl')
        self.page_el.type('id=>ttbOrderNum-inputEl', ordernum)
        self.page_el.type('id=>ttbCustomerID-inputEl', cusid)
        self.page_el.type('id=>ttbProductName-inputEl', prodname)
        self.page_el.sleep(1)
        self.page_el.click('//*[@id="f10"]/span/span')  # click查询按钮
        logger.info('开始进行查询！')
        self.page_el.sleep(2)
        try:
            recordnum = self.page_el.get_text('id=>fineui_7')
            print('记录数为：%s' % recordnum)
            self.page_el.sleep(2)
            flag = True
            if ('没有数据' in recordnum):
                logger.info('没有找到订单号：%s，客户编号：%s,产品名称：%s的订单信息，请检查' %
                            (ordernum, cusid, prodname))
            else:
                rnum = re.findall('\d+', recordnum)[2]
                logger.info('共查询到了%s条订单记录！' % rnum)
                if (int(rnum) == 1):
                    qordernum = self.page_el.get_text(
                        '//*[@id="Grid1"]//table/tbody/tr/td[3]/div')
                    qcusid = self.page_el.get_text(
                        '//*[@id="Grid1"]//table/tbody/tr/td[4]/div')
                    qprodname = self.page_el.get_text(
                        '//*[@id="Grid1"]//table/tbody/tr/td[6]/div')
                    self.assertTrue(ordernum in qordernum and cusid in qcusid
                                    and prodname in qprodname)
                    print('查询结果正确！')
                else:
                    for i in range(1, int(rnum) + 1):
                        qordernum = self.page_el.get_text(
                            '//*[@id="Grid1"]//table/tbody/tr[%d]/td[3]/div' %
                            i)
                        qcusid = self.page_el.get_text(
                            '//*[@id="Grid1"]//table/tbody/tr[%d]/td[4]/div' %
                            i)
                        qprodname = self.page_el.get_text(
                            '//*[@id="Grid1"]//table/tbody/tr[%d]/td[6]/div' %
                            i)
                        self.assertTrue(ordernum in qordernum
                                        and cusid in qcusid
                                        and prodname in qprodname)
                        print('查询结果正确！')
        except NoSuchElementException as nse:
            flag = False
            print('没有找到页面元素！' + str(nse))
        self.assertTrue(flag, msg='测试失败，请查看日志！')


if (__name__ == '__main__'):
    unittest.main(verbosity=2)