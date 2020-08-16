from blitz.scraper import Herald,  Hmetro,  Dailynews,  The_Zimbabwean, NewsDay,  Exchange_Rate_data,  Covid_API
from blitz.models import Article, Exchange_rate, Covid
from blitz import celery, db
from blitz.Utils import check

def data_entry_herald():
    news = Herald()
    for i in news.getArticle():
        try:
            if i.h3.a.text not in str(check("THE Herald")):
                info = Article(title=i.h3.a.text,  source="THE Herald",   link=news.splitLink(i.h3.a, 1).split("href=")[1].replace('"', ''),  summary=i.p.text,  image_src=str(i.img).split("src=")[1].split("/>")[0].replace('"', ''))
                db.session.add(info)
                db.session.commit()
        except Exception as e:
                    pass




def data_entry_Hmetro():
    news = Hmetro()
    for i in news.getArticle():
        try:
            if i.h3.a.text not in  str(check("H-Metro")):
                    info = Article(title=i.h3.a.text,  source="H-Metro",   link=news.splitLink(i.h3.a, 1).split("href=")[1].replace('"', ''),  summary=i.p.text,  image_src=str(i.img).split("src=")[1].split("/>")[0].replace('"', ''))
                    db.session.add(info)
                    db.session.commit()
        except Exception as e:
            pass


def data_entry_Dailynews():
    news = Dailynews()
    for i in news.getArticle():
        try:
            if i.h2.text not in  str(check("Daily News")):
                info = Article(title=i.h2.text, source="Daily News", link=str(i.h2).split(" ")[5].split("href=")[1].split(">")[0].replace('"', ''),  summary=i.div.contents[3].text,   image_src=str(i.div.div).split("data-src=")[1].split("href")[0].replace('"', ''))
                db.session.add(info)
                db.session.commit()
        except Exception as e:
                    pass


def data_entry_The_Zimbabwean():
    news = The_Zimbabwean()
    for i in news.getArticle():
        try:
            if [x for x in i.h3.stripped_strings][0] not in  str(check("The Zimbabwean")):
                image = str(i.img).split("src")[1].split("=")[1]
                if "title" in image:
                    info = Article(title=[x for x in i.h3.stripped_strings][0],  source="The Zimbabwean",   link= str(i.div.contents[3]).split("href=")[1].split(">")[0].replace('"', ''),  summary=[x for x in i.a.find("", class_="post-content image-caption-format-1").stripped_strings][0], image_src=image.split("title")[0].replace('"', ''))
                else:
                    info = Article(title=[x for x in i.h3.stripped_strings][0],  source="The Zimbabwean",   link= str(i.div.contents[3]).split("href=")[1].split(">")[0].replace('"', ''),  summary=[x for x in i.a.find("", class_="post-content image-caption-format-1").stripped_strings][0], image_src=str(i.img).split("src")[1].split("=")[1].replace('"', ''))
                db.session.add(info)
                db.session.commit()
        except Exception as e:
            pass


def data_entry_NewsDay():
    news = NewsDay()
    for i in news.getArticle():
        try:
            if i.h3.a.text not in  str(check("NewsDay")):
                image =str(i.img).split("src=")[1].split("srcset")[0]
                if "title=" in image:
                    info = Article(title=i.h3.a.text,  source="NewsDay", link=str(i.h3.a).split("item")[0].split("href=")[1].replace('"', ''),  summary=[x for x in i.find_all("div", class_="post-meta")[1].stripped_strings][0],  image_src= image.split("title")[0].replace('"', '').replace('"', ''))
                else:
                    info = Article(title=i.h3.a.text,  source="NewsDay",   link=str(i.h3.a).split("item")[0].split("href=")[1].replace('"', ''),  summary=[x for x in i.find_all("div", class_="post-meta")[1].stripped_strings][0],  image_src= str(i.img).split("src=")[1].split("srcset")[0].replace('"', ''))
                db.session.add(info)
                db.session.commit()
        except Exception as e:
            pass


#needs to be worked on (find diddrent way of gathering all the data)

def data_entry_Exchange_Rate_data():
    d = Exchange_Rate_data()
    data = d.rate()
    zimrates = Exchange_rate(name= "zimrates", rtgs=float(str(data.p.text).split("(zimrates.com)")[0].split("ZWL$")[1]) )
    db.session.add(zimrates)
    OMIR = Exchange_rate(name="OMIR" , rtgs=float(str(data.p.text).split('OMIR')[1].split("USD")[0]) )
    db.session.add(OMIR )
    interbank = Exchange_rate(name="interbank" , rtgs= float(str(data.p.text).split("(interbank)")[0].split(" ZWL$")[2]))
    db.session.add(interbank)
    zimrates_bond = Exchange_rate(name="zimrates_bond" , rtgs=float(str(data.p.text).split("(zimrates.com)")[1].split("BOND")[1]))
    db.session.add(zimrates_bond)
    bluemari_info = Exchange_rate(name="bluemari.info" , rtgs= float(str(data.p.text).split("(bluemari.info)")[0].split("ZWL$")[3]))
    db.session.add(bluemari_info)
    db.session.commit()




def data_entry_Covid_API():
    cov = Covid_API()
    c19=  cov.data()
    C = Covid(cases =int(c19["confirmed"]), death= int(c19["deaths"]), recovery=int(c19["recovered"]), active=int(c19["active"]))
    db.session.add(C)
    db.session.commit()

@celery.task
def Get_data():
    data_entry_herald()
    data_entry_Hmetro()
    data_entry_Dailynews()
    data_entry_The_Zimbabwean()
    data_entry_NewsDay()
    data_entry_Covid_API()
    data_entry_Exchange_Rate_data()
    return f"Now done"
