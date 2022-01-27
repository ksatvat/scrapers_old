#!/usr/bin/pythonx

########## Extract trendmicro!
from urllib.request import urlopen
import urllib.request
import os
import requests
from bs4 import BeautifulSoup
try:
    from PIL import Image
except ImportError:
    import Image
bad_links = []
count = 1

for page in range(1,203):
    source = 'https://www.trendmicro.com/vinfo/us/threat-encyclopedia/search/tspy/' + str(page)
    print("search page: ",source)
    url_list = []
    with open("/Users/me/Dropbox/Python/Exercises/Modules/scrapers/trendmicro/threats/data/summary/trendmicro_malware_names.txt", 'a+') as ml_names:
        req = urllib.request.Request(source, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(urlopen(req).read(), "html.parser")
        for name in soup.find_all('div', class_='resultbox_title'):
            print(name.text)
            ml_names.write(name.text)
            ml_names.write('\n')


    with open("/Users/me/Dropbox/Python/Exercises/Modules/scrapers/trendmicro/threats/data/summary/trendmicro_malware_links.txt", 'a+') as ml_links:
        req = urllib.request.Request(source, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(urlopen(req).read(), "html.parser")
        for a in soup.find_all('a', href=True):
            if "trendmicro.com/vinfo/us/threat-encyclopedia/malware" in a['href']:

                url_list.append(a['href'])
        ml_links.write('\n'.join(url_list))
        ml_links.write('\n')
    url_list = list(set(url_list))
    print(url_list)

    for link in url_list:
        print('=====******====== ',str(count),' =====******======')
        count+=1
        print("working on link...", link)
        try:
            req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(urlopen(req).read(),"html.parser")
            os.chdir(os.path.dirname(__file__))
            layer_1 = os.getcwd()
            if not os.path.exists("data"):
                try:
                    os.mkdir("data")
                except OSError:
                    print("Creation of the directory %s failed" % "data")
                else:
                    print("Successfully created the directory %s " % "data")

            data =  str(os.getcwd()) + "/" + "data"
            os.chdir(data)
            data_layer = os.getcwd()

            ##title
            title = soup.find('h1',class_= 'lessen_h1')
            print(title.text)
            with open(str(title.get_text()), 'w+') as file_:
                # try:
                file_.write('Page URL: ')
                file_.write(link)
                file_.write('\n')

                print(title.get_text())
                file_.write('Title: ')
                file_.write(str(title.get_text()))
                file_.write('\n')

                #date
                match = soup.find('div', class_="HolderDateShare")
                if match == None:
                    print("NO PUBLISH DATE")
                    file_.write("No publish date")
                else:
                    print("publish date: ", match.get_text("").split("\n\n")[0])
                    file_.write("publish date: ")
                    file_.write(match.text.split("\n\n")[0])
                    file_.write("\n\n\n")


                for match in range(len(soup.find_all('div', class_="entityHeader"))):
                    # print(soup.find_all('div', class_="entityHeader")[match].get_text(" "))
                    file_.write(soup.find_all('div', class_="entityHeader")[match].get_text(" "))
                    file_.write('\n')


                for match in range(len(soup.find_all('div', id="listDesc"))):
                    if match==0:
                        print('\t'+'-----'+ "OVERVIEW" +'-----'+'\n')
                        # print(soup.find_all('div', id="listDesc")[match].get_text(" ")+ '\n')
                        file_.write(soup.find_all('div', id="listDesc")[match].get_text(" "))
                        file_.write('\n\n\n')
                    elif match==1:
                        print('\t'+'-----'+ "TECHNICAL" +'-----'+'\n')
                        # print(soup.find_all('div', id="listDesc")[match].get_text(" ") + '\n')
                        file_.write(soup.find_all('div', id="listDesc")[match].get_text(" "))
                        file_.write('\n\n\n')
                    elif match==2:
                        print('\t'+'-----'+ "SOLTION" +'-----'+'\n')
                        # print(soup.find_all('div', id="listDesc")[match].get_text(" ") + '\n')
                        file_.write(soup.find_all('div', id="listDesc")[match].get_text(" "))
                        file_.write('\n\n\n')
                    else:
                        print('\t'+'-----'+ "ELSE!" +'-----'+'\n')
                        # print(soup.find_all('div', id="listDesc")[match].get_text(" ") + '\n')
                        file_.write(soup.find_all('div', id="listDesc")[match].get_text(" "))
                        file_.write('\n\n\n')

                    print('********************')

        except urllib.error.HTTPError:
            bad_links.append(link)
            print(bad_links)
            print("HTTP Error 404: Not Found")


