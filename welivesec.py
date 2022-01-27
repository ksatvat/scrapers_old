from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import requests

noise = '''Similar Articles'''
junks =[]
count = 1
source =  'https://www.welivesecurity.com/2017/12/08/strongpity-like-spyware-replaces-finfisher'
req = urllib.request.Request(source, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(urlopen(req).read(),"html.parser")

# title = soup.find('div', class_= "col-md-11 col-sm-11 col-xs-12 no-padding",attrs={'h1'})
title = soup.find('h1')
print("Title: ",title.text,"\n")

date = soup.find('time')
print("Published at: ",date.text,"\n")

source_ = requests.get(source).text
soup = BeautifulSoup(source_, 'lxml')
match = soup.find('div', class_="col-md-10 col-sm-10 col-xs-12 formatted")
print(match.text)
exclude = soup.find('span', attrs={'class': 'meta'})
# final_output =match.text.replace(exclude.text, "").split(noise)[0]
final_output = match.text.replace(exclude.text, "")
print(final_output)

img_tags = soup.find_all('img')

urls = [img['src'] for img in img_tags]

count = 1
images = []
for url in urls:
    if url not in junks:
        images.append(url)
        print(count, url)
        count+=1
path = r'/Users/me/Dropbox/Python/Exercises/Modules/scrapers/welivesecurity/'
filename_path = path+title.text+".txt"
with open(filename_path, 'w+') as out:
    out.write(title.text + '\n')
    out.write(date.text + '\n')
    out.write(final_output + '\n')
    for item in images:
        out.write("%s\n" % item)



