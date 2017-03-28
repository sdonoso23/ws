import pandas as pd
from selenium import webdriver
import os
import time
import pickle
import random as rn
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def changeUserAgent(dcap_profile, userAgent):
    dcap = dict(dcap_profile)
    dcap["phantomjs.page.settings.userAgent"] = userAgent
    return dcap

dcap = changeUserAgent(
    dcap_profile=DesiredCapabilities.PHANTOMJS,
    userAgent="Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0")

driver =  webdriver.PhantomJS(executable_path="C:/Users/Administrador.000/Downloads/phantomjs/bin/phantomjs",
                              desired_capabilities=dcap)


matches = []

for matchid in matches:
    path = "../JSON/"
    url = "https://www.whoscored.com/Matches/" + str(matchid) + "/Live/"
    driver.get(url)
    text1 = driver.find_element_by_css_selector("#breadcrumb-nav").find_element_by_css_selector("a").text.split(" - ")
    league = text1[0]
    year = text1[1].replace("/","-")
    source_code = driver.page_source

#search for piece with data
    start = "var matchCentreData = "
    end = ";"

#remove useless info
    try:
        source_code = source_code.split(start)[1].split(end)[0]
    except IndexError as e:
        print(matchid," Error")
    if not os.path.exists(str(path)+"/"+str(league)+"/"+str(year)):
        os.makedirs(str(path)+"/"+str(league)+"/"+str(year))
    f = open(str(path)+"/"+str(league)+"/"+str(year)+"/"+str(matchid)+".json", 'w',encoding="utf-8")
    print(time.strftime("%Y-%m-%d %H:%M:%S")," ",source_code[0],source_code[1],source_code[-1])
    try:
        f.write(source_code)
    except UnicodeEncodeError:
        pass
        print("Unicode error")
    f.close()
    time.sleep(10)
driver.close()
