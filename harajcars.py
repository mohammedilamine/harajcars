# import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
from selenium.webdriver.chrome.options import Options



def exitt():
    exit()

# Creates links.csv
options = Options()
options.headless = True

def adDetails ():

    with open('../output/links.csv', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        cpt = 0
        det = []
        imagelinks = []
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                linkfromfile = row[1]
                print(f'\t Ad URL: {row[1]} \n')
                line_count += 1
                my_url = linkfromfile
                uClient = uReq(my_url)
                page_html = uClient.read()
                uClient.close()

                page_soup = soup(page_html, "html.parser")
                print('\n')

                # header container
                header = page_soup.find("div", {"class": "adxHeader"})
                try:
                    p = header.findAll(attrs={'class': 'adxExtraInfoPart'})
                except AttributeError:
                     print('\n\nAD IS BEING DELETED\n\n ')
                     continue #skip to the next loop.
                else:
                    # body container
                    body = page_soup.find("div", {"class": "adxBody"})



                    # titre
                    titre = header.find("h3").get_text('', strip=True).replace('»','')

                    print(titre)

                    # place
                    place = p[0].get_text('', strip=True)
                    print(place)

                    # owner
                    owner = p[1].get_text('', strip=True)
                    print(owner)

                    # time
                    time = p[2].get_text('', strip=True)
                    print(time)

                    # description
                    description = body.get_text(' | ', strip=True)
                    print(description)

                    # contact
                    contact = body.find("div", class_="contact").find("strong").get_text('', strip=True)
                    contact = contact.strip()
                    print(contact)

                    # nummber =  [int(s) for s in contact.split() if s.isdigit()]
                    # print(nummber[0])

                    # fill details to det list
                    row = [titre, place, owner, time, contact, description]
                    det.append(row)
                    print('\n\nDET :::\n')
                    print(det[cpt])
                    cpt += 1

                    # fill image links to imagelinks list
                    print('\nimages:    ')
                    for image in body.find_all('img'):
                        imageLink = image.get('src')
                        print(imageLink)
                        # owner, url, link
                        row = [owner, my_url, imageLink]
                        imagelinks.append(row)

                    print('/\/\/\/\ \n')

        print(f'Processed {line_count} lines.\n')
        # print(det)
    csv_file.close()



    #  details file

    # file_name = str(datetime.datetime.now().replace(microsecond=0)).replace(' ', '_').replace(':', '-')
    # filename = "../output/%s_details.csv" % (file_name)
    filename = "../output/details.csv"

    headers = ["title","place","owner","time","contact","description"]

    with open(filename, "w", encoding="utf-8", newline='') as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(det)
    f.close()


    # images file

    # file_name = str(datetime.datetime.now().replace(microsecond=0)).replace(' ', '_').replace(':', '-')
    # filename = "../output/%s_images.csv" % (file_name)
    filename = "../output/images.csv"
    headers = ["owner","url","link"]
    with open(filename, "w", encoding="utf-8", newline='') as i:
        # images
        w = csv.writer(i)
        w.writerow(headers)
        w.writerows(imagelinks)
    i.close()


# Creates images.csv and details.csv

def adLinks (urlLink,nbrScroll):
    urll = urlLink

    browser = webdriver.Chrome('../../../Scrapping/chromedriver_win32/chromedriver',options=options)


    browser.get(urll)
    # time.sleep(1)

    elem = browser.find_element_by_tag_name("body")

    # Click  button
    try:
        python_button = browser.find_element_by_xpath('//*[@id="AJAXloaded"]/div/ul[1]/li/a').click()
    except:
        print('did not find the button')

    # Scroll
    scroll = int(nbrScroll)
    no_of_pagedowns = scroll
    while no_of_pagedowns:
        elem.send_keys(Keys.PAGE_DOWN)
        # time.sleep(0.2)
        no_of_pagedowns -= 1

    # Get Ads
    Ads = browser.find_elements_by_class_name("adx")

    nbr = len(Ads)
    print("there are :  {} Ads .\n".format(nbr))

    adList = []

    # Scrap by Ad
    for Ad in Ads:
        titre = Ad.find_element_by_class_name('adxTitle').text
        url = Ad.find_element_by_class_name('adxTitle').find_element_by_tag_name('a').get_attribute('href')
        time.sleep(0.2)
        adList.append([titre, url])

        print('{}\n{}\n{}\n/\/\/\/\ \n'.format(nbr, titre, url))
        nbr -= 1

    # Links file
    #
    # file_name = str(datetime.datetime.now().replace(microsecond=0)).replace(' ', '_').replace(':', '-')
    # filename = "../output/%s_links.csv" % (file_name)

    filename = "../output/links.csv"
    headers = ["titre", "url"]

    with open(filename, "w", encoding="utf-8", newline='') as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(adList)
    f.close()
    browser.quit()


def app():

    first = 'https://haraj.com.sa/tags/%D8%AD%D8%B1%D8%A7%D8%AC%20%D8%A7%D9%84%D8%B3%D9%8A%D8%A7%D8%B1%D8%A7%D8%AA'

    #  INPUT , CHANGE THE NUMBER 10 with a desired scroll number 
    secroll = 10
    
    adLinks(first,secroll)

    # print(f"Your link is: {first} ")
    print(f"scroll times: {sec}")
    print("\n\n Executing details function:\n\n")
    adDetails()

app()