# coding=utf-8
import datetime
import time
import sys
import pymd5
import  os
# NO.2 使用hashlib
import hashlib
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import requests

# 获取文件的MD5
def GetFileMd5(data):
    m1 = hashlib.md5()
    m1.update(data)
    return m1.hexdigest()


driver = webdriver.Firefox()
driver.implicitly_wait(30)

# 下载12306
url = 'https://www.12306.cn/index/'
driver.get(url)
time.sleep(5)
login = driver.find_element_by_css_selector('#J-header-login > a:nth-child(1)')
login.click()
time.sleep(1)
zhpass=driver.find_element_by_css_selector('.login-hd-account > a:nth-child(1)')
zhpass.click()
time.sleep(1)
forget_passwd = driver.find_element_by_css_selector('.txt-lighter')
forget_passwd.click()
time.sleep(1)
repeat_count=0
while 1:
    imgbtn = driver.find_element_by_css_selector('#img_rand_code')
    res_src = imgbtn.get_attribute('src')
    # 通过requests发送一个get请求到图片地址，返回的响应就是图片内容
    r = requests.get(res_src)
    file_md5 = GetFileMd5(r.content)
    file_name = "pictures/"+ file_md5 + ".png"
    ex = os.access(file_name, os.R_OK)
    if ex:
        repeat_count += 1
        with open('repeat_count.txt', 'w') as fc:
            fc.write('repeat_count:{}'.format(repeat_count))
        print('repeat_count:{}'.format(repeat_count))
        continue
    # 将获取到的图片二进制流写入本地文件
    with open(file_name, 'wb') as f:
        # 对于图片类型的通过r.content方式访问响应内容，将响应内容写入baidu.png中
        f.write(r.content)
    imgbtn.click()
    time.sleep(0.5)