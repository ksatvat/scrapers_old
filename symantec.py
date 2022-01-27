#!/usr/bin/python

##########  Symantec!

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request

source =  'https://www.symantec.com/security-center/risks'
req = urllib.request.Request(source, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(urlopen(req).read(),"html.parser")
count = 1
for source in soup.find_all('a', href=True):
    if "/content/symantec/english/en/security-center/writeup.html/" in source['href']:
        link = "https://www.symantec.com"+source['href']

        source_ = requests.get(link).text
        soup = BeautifulSoup(source_, 'lxml')
        match = soup.find('section', class_="content-band").text
        print("COUNT:    ",count)

        with open('risks072019.txt', 'a') as out:
            out.write("=============================================== " + "Num: " +str(count) + "   " + link +" ==========================================")
            count += 1
            out.write(match + '\n')

