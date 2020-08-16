import requests
import json
from bs4 import BeautifulSoup

class Herald():
    def __init__(self):
        header = {"user-agent" : 'Mozilla/5.0' }
        self.src =  requests.get("https://www.herald.co.zw/", headers= header).text
        self.soup = BeautifulSoup(self.src, "lxml")

    def splitLink(self, link, postion):
        l = str(link)
        link = l.split(" ")[postion]
        return link


    def getArticle(self):
        info = self.soup.find_all("div", class_="hentry sirius-card")
        return info
            #title = i.h3.a.text
            #summary = i.p.text
            #link = self.splitLink(info.h3.a, 1)
            #images =str(info.img).split("src=")[1]


class Hmetro():
    def __init__(self):
        header = {"user-agent" : 'Mozilla/5.0' }
        self.src =  requests.get("https://www.hmetro.co.zw/", headers= header).text
        self.soup = BeautifulSoup(self.src, "lxml")

    def splitLink(self, link, postion):
        l = str(link)
        link = l.split(" ")[postion]
        return link


    def getArticle(self):
        info = self.soup.find_all("div", class_="hentry sirius-card")
        return  info
        #return info


class Dailynews():
    def __init__(self):
        header = {"user-agent" : 'Mozilla/5.0' }
        self.src =  requests.get("https://dailynews.co.zw/", headers = header).text
        self.soup = BeautifulSoup(self.src, "lxml")

    def getArticle(self):
        info = self.soup.find_all("article", class_="listing-item-blog-5")
        return info
        #title = info.h2.text
        #summary =info.div.contents[3].text
        #link = str(info.h2).split(" ")[5].split("href=")[1].split(">")[0]
        #image_link = str(info.div.div).split("data-src=")[1].split("href")[0]




class The_Zimbabwean():
    def __init__(self):
        header = {"user-agent" : 'Mozilla/5.0' }
        self.src =  requests.get("http://www.thezimbabwean.co/", headers = header).text
        self.soup = BeautifulSoup(self.src, "lxml")

    def getArticle(self):
        info = self.soup.find_all("div", class_="post excerpt")
        return info
        #title=info.h3.stripped_strings
        #summary=info.a.find("", class_="post-content image-caption-format-1").stripped_strings
        #link= str(info.div.contents[3]).split("href=")[1].split(">")[0]
        #image_link=str(info.img).split("src")[1].split("=")[1]


class NewsDay():
    def __init__(self):
        header = {"user-agent" : 'Mozilla/5.0' }
        self.src =  requests.get("https://www.newsday.co.zw/", headers = header).text
        self.soup = BeautifulSoup(self.src, "lxml")

    def getArticle(self):
        info = self.soup.find_all("div", class_="post ws-post-sec post-1")
        return info
        #title = info.h3.a.text
        #summary=info.find_all("div", class_="post-meta")[1].stripped_strings
        #link= str(info.h3.a).split("item")[0].split("href=")[1]
        #image_link = str(info.img).split("src=")[1].split("srcset")[0]


class Exchange_Rate_data():
    def __init__(self):
        header = {"user-agent" : 'Mozilla/5.0' }
        self.marketWatch =  requests.get("https://www.marketwatch.co.zw/15-june-2020-market-rates/", headers = header).text
        self.market = BeautifulSoup(self.marketWatch, "lxml")


    def rate(self):
        info =self.market.find("div", class_="elementor-element elementor-element-19ec42ab elementor-widget elementor-widget-theme-post-content")
        return info
        #zimrates = str(info.p.text).split("(zimrates.com)")[0].split("ZWL$")[1]
        #OMIR = (str(info.p.text).split('OMIR')[1].split("USD")[0])
        #interbank = str(info.p.text).split("(interbank)")[0].split(" ZWL$")[2]
        #zimrates.com_bond = str(info.p.text).split("(zimrates.com)")[1].split("BOND")[1]
        #bluemari.info =str(info.p.text).split("(bluemari.info)")[0].split("ZWL$")[3]


class Covid_API():
    def __init__(self):
        header = {"user-agent" : 'Mozilla/5.0' }
        self.src =requests.get("https://covid2019-api.herokuapp.com/v2/country/zimbabwe")
        self.info = self.src.json()

    def data(self):
        return self.info["data"]
