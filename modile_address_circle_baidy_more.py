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

from selenium import webdriver

def get_address(mobile_number,fileptr):
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
            #with open(finename, 'a+') as f:
            fileptr.write('{} {} {}\n'.format(mobile_number, "invalid","invalid"))
            fileptr.flush()
            #print(mobile_number, "invalid","invalid")
            return 0
        res_address = browser.find_element_by_css_selector('span.c-gap-right:nth-child(2)')
        address = res_address.text
        res_yunyingshang = browser.find_element_by_css_selector('.op-phoneajax-answer-font > span:nth-child(3)')
        yunyingshang = res_yunyingshang.text
        #with open(finename, 'a+') as f:
        fileptr.write('{} {} {}\n'.format(mobile_number, address, yunyingshang))
        fileptr.flush()
        #print(mobile_number, address, yunyingshang)
        return 0
    except Exception as e:
        return -1

def GetAddressByPre(browser, filenamepre, str):
    # 输入url地址
    url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E6%89%8B%E6%9C%BA%E5%BD%92%E5%B1%9E%E5%9C%B0&rsv_pq=e797ca61000af364&rsv_t=210aQzOr2cQr%2FwIqnFzK8hYJmEqKGncwLswHkPBFD1fW2ty8qfsmTcrEgLk&rqlang=cn&rsv_enter=1&rsv_dl=ib&rsv_sug3=13&rsv_sug1=2&rsv_sug7=100&rsv_sug2=0&inputT=3630&rsv_sug4=3630'
    browser.get(url)
    lenstr = len(str)
    range_size = 10000
    sufixnumber = '8888'
    if lenstr == 4:
        sufixnumber = '888'
    filename = filenamepre +'_' + str + '.txt'
    fileptr = open(filename,"w")
    for i in range(range_size):
        mobile_number = "{}{:0>4d}{}".format(str, i, sufixnumber)
        while 1:
            ret = get_address(mobile_number, fileptr)
            if ret != 0:
                browser.get(url)
            else:
                break
    fileptr.close()

# 启动浏览器
browser = webdriver.Firefox()
browser.implicitly_wait(20)

try:
    Section_yidong = ["134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "157", "158", "159", "172",
                      "178", "182", "183", "184", "187", "188", "198"]
    Section_liantong = ["130", "131", "132", "145", "155", "156", "166", "171", "175", "176", "185", "186", "166"]
    Section_dianxin = ["133", "149", "153", "173", "177", "180", "181", "189", "199"]
    Section_xuniyunyingshang = ["1700", "1701", "1702", "1703", "1704","1705", "1706", "1707", "1708", "1709", "171"]

    print(len(Section_yidong) + len(Section_liantong) + len(Section_dianxin) + len(Section_xuniyunyingshang))

    # yidong
    for i in Section_yidong:
        GetAddressByPre(browser, 'yidong', i)

    # lian tong
    for i in Section_liantong:
        GetAddressByPre(browser, 'liangtong', i)

    # dian xing
    for i in Section_dianxin:
        GetAddressByPre(browser, 'dianxin', i)

    # xuniyunyingshang
    for i in Section_xuniyunyingshang:
        GetAddressByPre(browser, 'xuniyunyingshang', i)

except Exception as e:
    print(e)
#browser.quit()
