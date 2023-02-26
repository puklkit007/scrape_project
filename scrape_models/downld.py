import re
import os
import sys
import simplejson
import requests
import m3u8
import subprocess
from bs4 import BeautifulSoup

with open("output.txt") as f:
    all_lectures = simplejson.load(f)

for lec in all_lectures:
    for l in lec['lecture_details']:
        r = requests.get(l['embedUrl'])
        soup = BeautifulSoup(r.content, 'html5lib')
        s = soup.find_all("script")[4].text
        res = [i.start() for i in re.finditer('720p', s)]
        if not res:
            res = [i.start() for i in re.finditer('1080p', s)]
        q = s.find('https://embed-ssl.wistia.com/deliveries', res[0])
        l['access-key'] = s[q + 40:q + 80]

f = open('output1.txt', 'w')
simplejson.dump(all_lectures, f)
f.close()

with open("output1.txt") as f:
    all_lectures_a = simplejson.load(f)

for lec_a in all_lectures_a:
    cwd = os.path.abspath(os.getcwd())
    cwd1 = cwd + '\\' + str(lec_a['pos']) + '.' + lec_a['heading']
    if not os.path.isdir(cwd1):
        os.mkdir(cwd1)
    for la in lec_a['lecture_details']:

        if os.path.isfile(cwd1 + "\\" + str(la['l_pos']) + '.' + la['l_name'] + '.mp4'):
            continue

        base_url = f"https://embed-fastly.wistia.com/deliveries/{la['access-key']}.m3u8?origin_v2=1"

        r = requests.get(base_url)
        m3u8_master = m3u8.loads(r.text)
        root_url = "https://embed-fastly.wistia.com"

        for url in m3u8_master.data['segments']:
            url['uri'] = root_url + url['uri']

        vname = cwd1 + "\\" + str(la['l_pos']) + '.' + la['l_name'] + '.ts'
        with open(vname, "wb") as f:
            for segment in m3u8_master.data['segments']:
                url = segment['uri']
                r = requests.get(url)
                f.write(r.content)

        test = os.listdir(cwd1)
        count = 0
        for item in test:
            if item.endswith(".ts"):
                count += 1
        if count == 0:
            print('the .ts file is corrupt')
            sys.exit(-1)

        infile = cwd1 + '\\' + str(la['l_pos']) + '.' + la['l_name'] + '.ts'
        outfile = cwd1 + '\\' + str(la['l_pos']) + '.' + la['l_name'] + '.mp4'

        subprocess.run(['ffmpeg', '-i', infile, '-c', 'copy', outfile], shell=True)
        test = os.listdir(cwd1)
        for item in test:
            if item.endswith(".ts"):
                os.remove(os.path.join(cwd1, item))
