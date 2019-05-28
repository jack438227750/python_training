# --*--coding:utf-8 --*--
from selenium import webdriver
import time
# import datetime
from selenium.webdriver.common.action_chains import ActionChains
import configparser
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By


def main():
    "检查配置文件中乘车信息是否缺失"
    if(passengers == ''):  # 乘车人信息
        # print('当前日期为：' + time.strftime("%Y-%m-%d %H:%M:%S"))
        print('当前日期为：' + time.strftime("%Y-%m-%d"))
        print('没有乘车人信息，请检查配置文件！')
        driver.close()
    elif(go_date == ''):  # 出发日期为空
        print('没有指定出发日期，请检查配置文件！')
        driver.close()
    elif(time.mktime(time.strptime(go_date, "%Y-%m-%d %H:%M:%S")) <= time.time()):  # 出发日期小于当前日期
        print('指定的出发日期小于当前的日期，请检查配置文件！')
        driver.close()
    elif(trains == ''):  # 车次信息为空
        print('没有指定乘坐的车次信息，请检查配置文件！')
    else:
        login_text()
        search_ticket()
        book_ticket()


def login_text():
    "登录12306网站"
    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(20)
    # 登陆账号
    username_ele = driver.find_element_by_id('username')
    username_ele.clear()
    username_ele.send_keys(username)
    # 登陆密码
    pwd_ele = driver.find_element_by_id('password')
    pwd_ele.clear()
    pwd_ele.send_keys(pwd)
    while True:  # 手动进行图片验证，并登录
        curpage_url = driver.current_url
        # 判断当前页面是否还在登录页面
        if curpage_url != url:
            # 如果不是在登录页面，则代表登录成功
            if curpage_url[:-1] != url:
                print('.......登陆成功........')
                print(curpage_url[:-1])
                break
        else:
            time.sleep(3)
            print('--------->等待用户进行图片验证')
    print('curpage_url: ' + curpage_url)


def search_ticket():
    "通过webdriver.add_cookies方法，设置出发日期、出发站点与终到站点的信息"
    # driver.get('https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc')
    # selector = (By.XPATH, '//*[@id="J-chepiao"]/a')
    # WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable(selector))
    # 找到车票菜单
    moveticket = WebDriverWait(driver, 5).until(lambda x: x.find_element_by_xpath('//*[@id="J-chepiao"]/a'))
    # 使用ActionChains将鼠标移动到车票菜单上
    ActionChains(driver).move_to_element(moveticket).perform()
    time.sleep(1)
    # 在出现的子菜单中找到单程子菜单点击
    driver.find_element_by_link_text('单程').click()
    # 等待车次查询页面打开
    time.sleep(1)
    # 添加起点站查询的Cookie
    driver.add_cookie({
        'name': '_jc_save_fromStation',
        'value': '%u5E7F%u5DDE%2CGZQ'
    })  # 起始站点：广州
    # 添加终点站查询的Cookie
    driver.add_cookie({
        'name': '_jc_save_toStation',
        'value': '%u91CD%u5E86%2CCQW'
    })  # 终到站点：重庆
    # 添加出发日期的Cookie
    driver.add_cookie({
        'name': '_jc_save_fromDate',
        'value': go_date.split(' ')[0]
    })  # 选择出发日期
    print('选择的出发日期是：' + go_date.split(' ')[0])
    # 刷新查询页面，根据添加的Cookie自动添加起点、终点与出发日期
    driver.refresh()
    # print(driver.get_cookies())


# # 预订车票的方法
# def book_tickets():
#     # 循环查询
#     while True:
#         time.sleep(5)
#         search_btn = driver.find_element_by_link_text('查询')
#         search_btn.click()
#         trains_list = driver.find_elements_by_xpath('//*[starts-with(@id,"ticket_")]')
#         for tr in trains_list:
#             train = tr.find_element_by_xpath('.//a')
#             print('tain: ' + train.text)
#             if (train.text in trains):
#                 tr.find_element_by_xpath('./td[13]/a').click()
#                 print('找到%s车次的信息！' % train.text)
#         break


# 预订车票的方法
def book_ticket():
    "根据设置的出发日期、起止站信息进行车票预订操作"
    # 查询时间
    query_time = 0
    passenger_num = len(passengers.split(','))
    print('乘车人数为：%s ' % passenger_num)
    # time_begin = time.time()
    # ticket_info = ''
    sit = trains.split(',')
    print('需预订的车次为：%s, %s' % (sit[0], sit[1]))
    search_btn = driver.find_element_by_link_text('查询')
    # 循环查询
    while True:
        time_begin = time.time()
        # search_btn = driver.find_element_by_link_text('')
        WebDriverWait(driver, 5).until(lambda x: x.find_element_by_link_text('查询')).click()
        # search_btn.click()
        # 扫描查询结果
        try:
            # 获取相应车次二等座是否有票的元素
            ticket1_ele = driver.find_element_by_xpath(
                '//*[starts-with(@id,"ZE_") and contains(@id,"' + sit[0] + '")]')
            # 获取元素的文本信息
            ticket1_info = ticket1_ele.text
            print('车次：%s 二等座余票信息：===> %s' % (sit[0], ticket1_info))
            ticket2_ele = driver.find_element_by_xpath(
                '//*[starts-with(@id,"ZE_") and contains(@id,"' + sit[1] + '")]')
            # 获取元素的文本信息
            ticket2_info = ticket2_ele.text
            print('车次：%s 二等座余票信息：===> %s' % (sit[1], ticket2_info))
        except Exception as e:
            search_btn.click()
            driver.implicitly_wait(5)
            ticket1_ele = driver.find_element_by_xpath(
                '//*[contains(@id,"D1810")]')
            ticket1_info = ticket1_ele.text
            print('可能您的xpath选择错误,错误详情：%s' % format(e))
        # 如果二等座显示无或*号，则表示该车次二等座无票
        # if ((ticket1_info == '无' or ticket1_info == '*') and (ticket1_info == '无' or ticket1_info == '*')):
        #     # 查询次数加1
        #     query_time += 1
        #     cur_time = time.time()
        #     print('第%d次查询，用时%s秒!' % (query_time, cur_time - time_begin))
        # else:
        #     # 有票，则点击预订按钮
        #     driver.find_element_by_xpath(
        #         '//*[contains(@id,"' + sit[1] + '")]/td[13]/a').click()
        #     break
        # 如果二等座显示无或*号，则表示该车次二等座无票
        if(ticket1_info == '有' or ticket1_info.isdigit()):
            # 有票，则点击预订按钮
            print('开始预订 %s 车次的二等座......' % sit[0])
            driver.find_element_by_xpath(
                '//*[contains(@id,"' + sit[0] + '")]/td[13]/a').click()
            break
        elif(ticket2_info == '有' or ticket2_info.isdigit()):
            print('开始预订 %s 车次的二等座......' % sit[1])
            driver.find_element_by_xpath(
                '//*[contains(@id,"' + sit[1] + '")]/td[13]/a').click()
            break
        else:
            time.sleep(5)
            # 查询次数加1
            query_time += 1
            cur_time = time.time()
            print('无票可订，第%d次查询，用时%s秒!' % (query_time, cur_time - time_begin))
    # 确认订单的URL
    cust_url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
    # try:
    #     tips = driver.find_element_by_xpath(
    #         '//*[@id="content_defaultwarningAlert_hearder"]')
    #     if ('未完成订单' in tips.text):
    #         print('存在未完成订单！')
    # except Exception as e:
    #     print('预订失败了：' + format(e))
    while True:
        if (driver.current_url == cust_url):
            print('页面跳至选择乘客信息成功')
            break
        else:
            time.sleep(1)
            print('等待页面跳转!')
    while True:
        try:
            # 获取联系人列表元素
            passengers_list = driver.find_elements_by_xpath(
                '//*[@id="normal_passenger_id"]/li')
            for passenger in passengers_list:
                name = passenger.find_element_by_xpath('./label').text
                if(name in passengers):
                    passenger.find_element_by_class_name('check').click()
                    # try:
                    #     WebDriverWait(driver, 5).until(lambda x: x.find_element_by_link_text(
                    #         '确认')).click()
                    # except Exception as e:
                    #     print('没有找到购买儿童票的提示信息!' + str(e))
            # 选择联系人
            # driver.find_element_by_xpath(
            #     '//*[@id="normalPassenger_0"]').click()
            # driver.find_element_by_xpath(
            #     '//*[@id="normalPassenger_10"]').click()
            if(ischild == 'yes'):
                WebDriverWait(driver, 5).until(lambda x: x.find_element_by_link_text(
                    '添加儿童票')).click()
                passenger_num += 1
                print('开始添加儿童票！')
            break
        except Exception as e:
            print('联系人列表加载中......' + str(e))
    # 提交订单
    driver.find_element_by_id('submitOrder_id').click()
    time.sleep(1)
    while True:
        try:
            # windows = driver.window_handles
            # print(windows)
            # driver.switch_to.frame(
            #     driver.find_element_by_xpath('//*[@id="body_id"]/iframe[2]'))
            # selector1 = (By.XPATH, '//*[@id="1D"]')
            # selector2 = (By.XPATH, '//*[@id="1D"]')
            # WebDriverWait(driver, 10).until(
            #         EC.element_to_be_clickable(selector1))
            # WebDriverWait(driver, 10).until(
            #         EC.element_to_be_clickable(selector2))
            time.sleep(1)
            # 根据订票人数进行选座操作
            if(passenger_num == 1):
                driver.find_element_by_link_text('F').click()
            elif(passenger_num == 2):
                driver.find_element_by_link_text('D').click()
                driver.find_element_by_link_text('F').click()
            elif(passenger_num == 3):
                driver.find_element_by_link_text('A').click()
                driver.find_element_by_link_text('B').click()
                driver.find_element_by_link_text('C').click()
            elif(passenger_num == 4):
                driver.find_element_by_link_text('A').click()
                driver.find_element_by_link_text('B').click()
                driver.find_element_by_link_text('C').click()
                driver.find_element_by_link_text('D').click()
            elif(passenger_num ==5):
                driver.find_element_by_link_text('A').click()
                driver.find_element_by_link_text('B').click()
                driver.find_element_by_link_text('C').click()
                driver.find_element_by_link_text('D').click()
                driver.find_element_by_link_text('F').click()
            else:
                WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id('qr_submit_id')).click()
                # driver.find_element_by_id('qr_submit_id').click()
                print('超过5人购票，不选座，直接提交！')
                break
            time.sleep(1)
            # 确认订单按钮
            # WebDriverWait(driver, 5).until(lambda x: x.find_element_by_id('qr_submit_id')).click()
            # 返回修改按钮
            driver.find_element_by_id('back_edit_id').click()
            break
        except Exception as e:
            print('请手动选座和点击确认信息')
            print(format(e))
            time.sleep(5)
            break


if (__name__ == '__main__'):
    driver = webdriver.Chrome()
    url = 'https://kyfw.12306.cn/otn/login/init'
    config = configparser.ConfigParser()
    config.read(r'D:\pyth\MyProject\config.ini', encoding='utf-8')
    username = config.get('username', 'name')
    pwd = config.get('password', 'pwd')
    go_date = config.get('go_date', 'date')
    passengers = config.get('passengers', 'lists')
    print('passengers: ' + passengers)
    trains = config.get('trains', 'lists')
    print('trains: ' + trains)
    ischild = config.get('child', 'ischild')
    main()
