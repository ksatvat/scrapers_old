

import pytesseract
from PIL import Image
import os
import requests
from bs4 import BeautifulSoup



junks =[]
links = []


for link in links:
    source_ = requests.get(link).text
    soup = BeautifulSoup(source_, 'lxml')
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

    file_name = link.rsplit("/")[-1]
    with open(link.rsplit("/")[-1],"w+") as file_:
        file_.write("Page URL: ")
        file_.write(link)
        print("Page URL: ",link)

        ## date
        match = soup.find('div', class_= 'panel-pane pane-node-created')
        if match == None:
            print("No publish date: ", link)
        else:
            print("publish date:", match.text.split("   ")[1])
            file_.write(match.text.split("   ")[1])
            pb_date = match.text.split("   ")[1]

        ## content
        match = soup.find('div', {'class': 'container'})
        if match == None or "If you think you have reached this page in error, let us know by emailing sitefeedback@forcepoint.com" in match.text:
            print("No text scraped! ", link)
        else:
            # print(match.text.split(ends)[0].split(pb_date)[1])
            file_.write(match.text.split(ends)[0].split(pb_date)[1])

        img_tags = soup.find_all('img')
        print(img_tags)
        if img_tags == None:
            print("No img tag in the page", link)
        else:
            urls = [img['src'] for img in img_tags]
            images = []
            count = 1
            for url in urls:
                if url not in junks and "sites/default/files/styles/blog_author_teaser/public" not in url:
                    if "https://" in url or "http://" in url:
                        images.append(url)
                    if "https://www.forcepoint.com" not in url:
                        # if url not in junks:
                        url = "https://www.forcepoint.com"+ url
                        images.append(url)
                        count+=1

        folder_name = link.rsplit("/")[-1] #notnotpetya-bad-rabbit
        path = __file__.strip(__file__.split('/')[-1:][0])  # /Users/me/Dropbox/Python/Exercises/Modules/scrapers/forcepoint
        os.chdir(layer_1)
        if not os.path.exists("images"):
            try:
                os.mkdir("images")
            except OSError:
                print("Creation of the directory %s failed" % "images")
            else:
                print("Successfully created the directory %s " % "images")

        os.chdir("images")
        # print("am i inside images?????",os.getcwd())
        if not os.path.exists(folder_name):
            try:
                os.mkdir(folder_name)
            except OSError:
                print("Creation of the directory %s failed" % folder_name)
            else:
                print("Successfully created the directory %s " % folder_name)

        file_name = link.split("/")[-1]
        # print(file_name)
        os.chdir(folder_name)
        print("i am inside folder:::", os.getcwd())
        print(images)
        for link in images:
            file = link.split("/")[-1]
            # print(file)
            with open(file, 'wb') as handle:
                try:
                    response = requests.get(link, stream=True)
                    if not response.ok:
                        print(response)
                    for block in response.iter_content(1024):
                        if not block:
                            break
                        handle.write(block)
                except requests.exceptions.ConnectionError:
                    requests.status_code = "Connection refused"
                    print("connection refused", link)

        for image in os.listdir(os.getcwd()):
            if image.endswith('.png'):
                try:
                    print(pytesseract.image_to_string(Image.open(image)))
                    file_.write("\n\n\nOCR Extracted data:\n")
                    file_.write("===================\n\n\n")
                    file_.write(pytesseract.image_to_string(Image.open(image)))
                except OSError:
                    print("OSError error occured:", image)
        file_.write("\n\n\n===================\n")
        file_.write("\n\n\nLink to Images: \n\n\n")
        file_.write(" , ".join(images))
        file_.write("\n\n\n=========END OF FILE=========\n")


        print("\n\n\n===================\n")
        print("\n\n\nLink to Images: \n\n\n")
        print(" , ".join(images))
        print("\n\n\n=========END OF FILE=========\n")






