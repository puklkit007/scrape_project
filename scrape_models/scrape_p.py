import re
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

time.sleep(20)

# driver.get('https://365datascience.teachable.com/courses/709679/lectures/12746072')

driver.find_element_by_xpath("/html/body/div/div/div/div[2]/div[10]/div/div[1]/a/div/div[2]").click()

time.sleep(5)

driver.find_element_by_xpath("/html/body/div[2]/div[2]/div/ul/li[1]/a/div/div").click()

time.sleep(5)

url = "https://365datascience.teachable.com/courses/360102/lectures/5638849"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')
s = soup.find("div", attrs={'class': 'row lecture-sidebar'})

l = []
total_videos = 0
head = 0
for i in s.find_all('div', attrs={'class': 'col-sm-12 course-section'}):
    head += 1
    sub_head = 0
    content_d = {}
    hd = i.find('div', attrs={'role': 'heading'}).text
    hd = hd.strip()
    hd = hd.split('?', 1)[0].split('!', 1)[0]
    hd = hd.replace(':', '-')
    hd = hd.replace('&', '-')
    content_d['heading'] = hd
    content_d['pos'] = head
    l_list = []
    for j in i.find_all('li'):
        l_content = {}
        sub_head += 1
        if j.find('i', attrs={'class': 'fa fa-file-text'}):
            continue
        element = driver.find_element_by_xpath(f'//*[@id="courseSidebar"]/div[2]/div[{head}]/ul/li[{sub_head}]').click()
        time.sleep(5)
        try:
            clnk = driver.find_element_by_xpath("/html/head/script[1]").get_attribute("innerHTML")
            clink = json.loads(clnk)
            eurl = clink['embedUrl']
        except:
            print('JSON not loaded')
            sys.exit(-1)

        l_name = j.find('span', attrs={'class': 'lecture-name'}).text
        l_name = " ".join(l_name.split())
        l_name = l_name.rsplit('(', 1)[0].strip()
        l_name = l_name.split('?', 1)[0].split('!', 1)[0]
        l_name = l_name.replace(':', '-')
        l_name = l_name.replace('&', '-')
        l_name = l_name.replace('|', '-')
        l_name = l_name.replace('\\', ' or')
        l_name = l_name.replace('/', ' or')
        l_content['l_pos'] = sub_head
        l_content['l_name'] = l_name
        l_content['embedUrl'] = eurl
        total_videos += 1
        l_list.append(l_content)
    content_d['lecture_details'] = l_list
    l.append(content_d)

print(total_videos)
f = open('output.txt', 'w')
simplejson.dump(l, f)
f.close()

# clnk = driver.find_element_by_xpath("/html/head/script[1]").get_attribute("innerHTML")

# clink = json.loads(clnk)

# eurl = clink['embedUrl']

# l.append(eurl)

# for i in range(2,5):
# 	driver.find_element_by_xpath(f'//*[@id="courseSidebar"]/div[2]/div[1]/ul/li[{i}]').click()
# 	time.sleep(5)
# 	clnk = driver.find_element_by_xpath("/html/head/script[1]").get_attribute("innerHTML")
# 	clink = json.loads(clnk)
# 	eurl = clink['embedUrl']
# 	l.append(eurl)

# r = requests.get(eurl)
# soup = BeautifulSoup(r.content, 'html5lib')
# s = soup.find_all("script")[4].text
# subs = "https://embed-ssl.wistia.com/deliveries"
# res = [i.start() for i in re.finditer(subs, s)]
# print(s[res[1]+40:res[1]+80])
