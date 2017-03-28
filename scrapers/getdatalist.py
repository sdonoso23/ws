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

#set parameters

number = 45
league = "La Liga"
year = "2012-2013"
file = "../CSV/Lists/"+str(league)+" "+str(year)+" Matches.csv"


listofmatches = pd.read_csv(file,index_col=0)
matches = listofmatches['matchid'].values.tolist()
deletematches = []

for match in matches:
    if os.path.exists("../JSON/"+str(league)+"/"+str(year)+"/"+str(match)+".json"):
        deletematches.append(match)

print("you already have ", len(deletematches)," matches")
print("you are missing", len(matches)-len(deletematches)," matches")

if len(deletematches) > 0:
    for match in deletematches:
        matches.remove(match)

matches = matches[0:number]
print("starting scraping of ",len(matches)," matches")

count = 0

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
    count = count + 1
    print(time.strftime("%Y-%m-%d %H:%M:%S")," ",count, "matches done " ,source_code[0],source_code[1],source_code[-1])
    try:
        f.write(source_code)
    except UnicodeEncodeError:
        pass
        print("Unicode error")
    f.close()
    time.sleep(rn.randint(3,5))

driver.close()
driver.quit()
