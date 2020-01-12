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



# 启动浏览器
browser = webdriver.Firefox()
browser.implicitly_wait(20)

try:
    # 输入url地址
    browser.get("http://www.ip138.com:8080/search.asp?mobile=1385111&action=mobile")

    #tr.tdc:nth-child(3) > td:nth-child(2)
    #body > table: nth - child(6) > tbody > tr:nth - child(3) > td.tdc2
    # 输入手机号的前7位
    browser.find_element_by_css_selector('input[name="mobile"]').send_keys("1382111")
    #browser.find_element_by_css_selector('input[name="txtPassword"][type="password"]').send_keys("681214")
    browser.find_element_by_css_selector('input[type="submit"]').click()
    time.sleep(1)

    #res = browser.find_element_by_css_selector('body>table>td>tr[class="tdc2"]')
    res = browser.find_element_by_css_selector('tr.tdc:nth-child(3) > td:nth-child(2)')
    print(res.text)

    # 查找结果
    a = 4
    b=a+4

except Exception as e:
    print(e)
browser.quit()
