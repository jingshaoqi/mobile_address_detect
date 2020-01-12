#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import datetime
import os
import re,sys
import  pymysql

from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.color import Color

from pyquery import PyQuery as pq
from selenium import webdriver
from craw_data_win.craw_data.competition_catalogue import *

def get_address(mobile_number,count):
    try:

        # 输入手机号的前7位
        browser.find_element_by_css_selector('.c-input').clear()
        browser.find_element_by_css_selector('.c-input').send_keys(mobile_number)
        # browser.find_element_by_css_selector('input[name="txtPassword"][type="password"]').send_keys("681214")
        browser.find_element_by_css_selector('.c-btn').click()

        # res = browser.find_element_by_css_selector('body>table>td>tr[class="tdc2"]')
        res = browser.find_element_by_css_selector('.op-phoneajax-tip')
        att = res.get_attribute('style')
        if att.find('block') != -1:
            return 0
        res_address = browser.find_element_by_css_selector('span.c-gap-right:nth-child(2)')
        address = res_address.text
        res_yunyingshang = browser.find_element_by_css_selector('.op-phoneajax-answer-font > span:nth-child(3)')
        yunyingshang = res_yunyingshang.text
        if address.find('重庆') != -1:
            with open('mobile_address_baidu.txt', 'a+') as f:
                f.write('{} {} {}\n'.format(mobile_number, address, yunyingshang))
        print(mobile_number, address, yunyingshang,count)
        return 0
    except Exception as e:
        return -1


# 启动浏览器
browser = webdriver.Firefox()
browser.implicitly_wait(20)

try:
    # 输入url地址
    url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E6%89%8B%E6%9C%BA%E5%BD%92%E5%B1%9E%E5%9C%B0&rsv_pq=e797ca61000af364&rsv_t=210aQzOr2cQr%2FwIqnFzK8hYJmEqKGncwLswHkPBFD1fW2ty8qfsmTcrEgLk&rqlang=cn&rsv_enter=1&rsv_dl=ib&rsv_sug3=13&rsv_sug1=2&rsv_sug7=100&rsv_sug2=0&inputT=3630&rsv_sug4=3630'
    browser.get(url)
    #tr.tdc:nth-child(3) > td:nth-child(2)
    #body > table: nth - child(6) > tbody > tr:nth - child(3) > td.tdc2  .op-phoneajax-tip

    count = 0
    regeturlcount=0
    for i in range(10):
        for j in range(10):
            for k in range(10):
                for m in range(10):
                    mobile_number= "138{}{}{}{}2345".format(i,j,k,m)
                    while 1:
                        count += 1
                        ret = get_address(mobile_number,count)
                        if ret != 0:
                            browser.get(url)
                            regeturlcount += 1
                        else:
                            break




    # 查找结果
    print("total count:{} regeturlcount:{}".format(count,regeturlcount))

except Exception as e:
    print(e)
browser.quit()
