import re
import os
import sys
import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import m3u8
import subprocess
import simplejson

email = 'khandelwalpulkit007@gmail.com'
pwd = 'Puklkit@007'

driver = webdriver.Chrome('C:\\Users\\intal\\Downloads\\chromedriver')
driver.get('https://sso.teachable.com/secure/130400/users/sign_in')

time.sleep(5)

driver.find_element_by_xpath("//*[@id='user_email']").send_keys(email)
driver.find_element_by_xpath("//*[@id='user_password']").send_keys(pwd)
driver.find_element_by_xpath("//*[@id='new_user']/div[3]/input").click()

time.sleep(30)

driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div[19]/div/div[1]/a/div/div[2]").click()

time.sleep(5)

driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/ul/li[1]/a/div/div").click()

time.sleep(5)

url = "https://365datascience.teachable.com/courses/389508/lectures/5943144"

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')
s = soup.find("div", attrs={'class': 'row lecture-sidebar'})
cwd = os.path.abspath(os.getcwd())
cwd1 = cwd + '\\' +'downloads'
if not os.path.isdir(cwd1):
    os.mkdir(cwd1)

head = 0
for i in s.find_all('div', attrs={'class': 'col-sm-12 course-section'}):
    head += 1
    sub_head = 0
    hd = i.find('div', attrs={'role': 'heading'}).text
    hd = hd.strip()
    hd = hd.split('?', 1)[0].split('!', 1)[0]
    hd = hd.replace(':', '-')
    hd = hd.replace('&', '-')
    h_title = cwd1 + '\\' + hd
    if not os.path.isdir(h_title):
        os.mkdir(h_title)
    for j in i.find_all('li'):

        sub_head += 1
        element = driver.find_element_by_xpath(f'//*[@id="courseSidebar"]/div[2]/div[{head}]/ul/li[{sub_head}]').click()
        time.sleep(5)

        l_name = j.find('span', attrs={'class': 'lecture-name'}).text
        l_name = " ".join(l_name.split())
        if not j.find('i', attrs={'class': 'fa fa-file-text'}):
            l_name = l_name.rsplit('(', 1)[0].strip()
        l_name = l_name.split('?', 1)[0].split('!', 1)[0]
        l_name = l_name.replace(':', '-')
        l_name = l_name.replace('&', '-')
        l_name = l_name.replace('|', '-')
        l_name = l_name.replace('\\', ' or')
        l_name = l_name.replace('/', ' or')

        if not os.path.isdir(h_title + "\\" + l_name):
            os.mkdir(h_title + "\\" + l_name)

        if j.find('i', attrs={'class': 'fa fa-file-text'}):
            ele = driver.find_elements_by_tag_name("p")
            file1 = open(h_title + "\\" + l_name +"\\" + l_name + ".txt", "a")
            for p in ele:
                file1.write(p.text)
                file1.write("\n\n")
            file1.close()

        try:
            ele = driver.find_elements_by_class_name("download")
            for a in ele:
                url = a.get_attribute('href')
                r = requests.get(url, stream=True)
                f_name = h_title + "\\" + l_name + "\\" + a.get_attribute('data-x-origin-download-name')
                with open(f_name, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):

                        # writing one chunk at a time to pdf file
                        if chunk:
                            f.write(chunk)
        except:
            print('no download')

        if not os.listdir(h_title + "\\" + l_name):
            os.rmdir(h_title + "\\" + l_name)
