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
import threading

def get_address(browser, mobile_number,fileptr):
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
            fileptr.write('{} {} {}\n'.format(mobile_number, "invalid","invalid"))
            fileptr.flush()
            #print(mobile_number, "invalid","invalid")
            return 0
        res_address = browser.find_element_by_css_selector('span.c-gap-right:nth-child(2)')
        address = res_address.text
        res_yunyingshang = browser.find_element_by_css_selector('.op-phoneajax-answer-font > span:nth-child(3)')
        yunyingshang = res_yunyingshang.text
        fileptr.write('{} {} {}\n'.format(mobile_number, address, yunyingshang))
        fileptr.flush()
        #print(mobile_number, address, yunyingshang)
        return 0
    except Exception as e:
        return -1

def GetFinishedNum(qq):
    filename = qq + '.txt'
    ex = os.access(filename, os.R_OK)
    if ex:
        fp = open(filename, 'r', encoding='utf-8')
        fishdata = fp.readlines()
        linecount = len(fishdata)
        if linecount < 1:
            return -1
        lastline = fishdata[linecount - 1]
        n1 = len(qq)
        n2 = n1 + 4
        num = lastline[n1:n2]
        return int(num)
    else:
        return -1

def GetAddressByPre(str):
    # 输入url地址
    browser = webdriver.Firefox()
    browser.implicitly_wait(20)
    url = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E6%89%8B%E6%9C%BA%E5%BD%92%E5%B1%9E%E5%9C%B0&rsv_pq=e797ca61000af364&rsv_t=210aQzOr2cQr%2FwIqnFzK8hYJmEqKGncwLswHkPBFD1fW2ty8qfsmTcrEgLk&rqlang=cn&rsv_enter=1&rsv_dl=ib&rsv_sug3=13&rsv_sug1=2&rsv_sug7=100&rsv_sug2=0&inputT=3630&rsv_sug4=3630'
    browser.get(url)
    lenstr = len(str)
    range_size = 10000

    firstnum = GetFinishedNum(str) + 1
    if firstnum >= 10000:
        return

    sufixnumber = '8888'
    if lenstr == 4:
        sufixnumber = '888'
    filename = str + '.txt'
    fileptr = open(filename,"a+", encoding='utf-8')
    for i in range(firstnum, range_size):
        if (i+1) % 5000 == 0:
            browser.quit()
            browser = webdriver.Firefox()
            browser.implicitly_wait(40)
            browser.get(url)
        mobile_number = "{}{:0>4d}{}".format(str, i, sufixnumber)
        while 1:
            ret = get_address(browser, mobile_number, fileptr)
            if ret != 0:
                browser.get(url)
            else:
                break
    fileptr.close()
    browser.quit()

def SectionFinished(yy):
    filename = yy + '.txt'
    ex = os.access(filename, os.R_OK)
    if ex:
        fp = open(filename, 'r', encoding='utf-8')
        fishdata = fp.readlines()
        ln = len(fishdata)
        if ln >= 10000:
            return True
        else:
            return False
    else:
        return False

def WorkThread(tt):
    try:
        # 启动浏览器
        print("decet:{}".format(tt))
        str = '{}'.format(tt)
        GetAddressByPre(str)
    except Exception as e:
        print(e)

def Execuse(pnum):
    arrthd = []
    while len(pnum) > 0:
        thd = threading.Thread(target=WorkThread, args=(pnum[0],))
        arrthd.append(thd)
        if len(arrthd) >= 2:
            for i in arrthd:
                i.start()
            for i in arrthd:
                i.join()
            arrthd.clear()
        pnum.pop(0)
    for i in arrthd:
        i.start()
    for i in arrthd:
        i.join()

try:
    Section_yidong = ["134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "157", "158", "159", "172",
                      "178", "182", "183", "184", "187", "188", "198"]
    Section_liantong = ["130", "131", "132", "145", "155", "156", "166", "171", "175", "176", "185", "186"]
    Section_dianxin = ["133", "149", "153", "173", "177", "180", "181", "189", "199"]
    Section_xuniyunyingshang = ["1700", "1701", "1702", "1703", "1704","1705", "1706", "1707", "1708", "1709"]

    print(len(Section_yidong) + len(Section_liantong) + len(Section_dianxin) + len(Section_xuniyunyingshang))

    PreNum = ["134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "157", "158", "159", "172",
              "178", "182", "183", "184", "187", "188", "198",
              "130", "131", "132", "145", "155", "156", "166", "171", "175", "176", "185", "186",
              "133", "149", "153", "173", "177", "180", "181", "189", "199",
              "1700", "1701", "1702", "1703", "1704", "1705", "1706", "1707", "1708", "1709"]

    print(len(PreNum))

    while 1:
        # is all finish
        chknum = []
        for w in PreNum:
            fd = SectionFinished(w)
            if fd == False:
                chknum.append(w)
        if len(chknum) == 0:
            break
        Execuse(chknum)
    print('all finished')
except Exception as e:
    print(e)

