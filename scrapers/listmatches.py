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

#set url

url = "https://www.whoscored.com/Regions/252/Tournaments/2/Seasons/2458"

driver.get(url)
league = driver.find_element_by_css_selector("#breadcrumb-nav").find_element_by_css_selector("#tournaments").find_element_by_css_selector("[selected]").text
year = driver.find_element_by_css_selector("#breadcrumb-nav").find_element_by_css_selector("#seasons").find_element_by_css_selector("[selected]").text

driver.find_element_by_css_selector("#sub-navigation").find_elements_by_css_selector("a")[1].click()
time.sleep(5)
matches_df = pd.DataFrame(columns=["league","year","matchid","home_team","away_team","home_team_score","away_team_score"])
matches = driver.find_element_by_id("tournament-fixture").find_elements_by_css_selector("tr")
matchcount = 0

while driver.find_element_by_id("date-controller").find_elements_by_css_selector("a")[0].get_attribute("title") == "View previous month":
    for match in matches:
        if match.get_attribute("data-id") != None:
            matches_dict = {
                    "league": league,
                    "year": year,
                    "matchid": match.find_elements_by_css_selector("td")[4].find_element_by_css_selector("a").get_attribute("href").split("/")[4],
                    "home_team": match.find_elements_by_css_selector("td")[3].get_attribute("data-id"),
                    "away_team": match.find_elements_by_css_selector("td")[5].get_attribute("data-id"),
                    "home_team_score": None,
                    "away_team_score": None,
                     }
            if match.find_elements_by_css_selector("td")[4].find_element_by_css_selector("a").text != "vs":
                matches_dict["home_team_score"] = match.find_elements_by_css_selector("td")[4].find_element_by_css_selector("a").text.split(" : ")[0]
                matches_dict["away_team_score"] = match.find_elements_by_css_selector("td")[4].find_element_by_css_selector("a").text.split(" : ")[1]
            matches_df.loc[len(matches_df)] = matches_dict
            matchcount = matchcount+1
            continue
    print(matchcount, " matches done!")
    driver.find_element_by_id("date-controller").find_elements_by_css_selector("a")[0].click()
    time.sleep(rn.randint(3,5))
    matches = driver.find_element_by_id("tournament-fixture").find_elements_by_css_selector("tr")

for match in matches:
    if match.get_attribute("data-id") != None:
        matches_dict = {
                "league": league,
                "year": year,
                "matchid": match.find_elements_by_css_selector("td")[4].find_element_by_css_selector("a").get_attribute("href").split("/")[4],
                "home_team": match.find_elements_by_css_selector("td")[3].get_attribute("data-id"),
                "away_team": match.find_elements_by_css_selector("td")[5].get_attribute("data-id"),
                "home_team_score": None,
                "away_team_score": None,
                 }
        if match.find_elements_by_css_selector("td")[4].find_element_by_css_selector("a").text != "vs":
            matches_dict["home_team_score"] = match.find_elements_by_css_selector("td")[4].find_element_by_css_selector("a").text.split(" : ")[0]
            matches_dict["away_team_score"] = match.find_elements_by_css_selector("td")[4].find_element_by_css_selector("a").text.split(" : ")[1]
        matches_df.loc[len(matches_df)] = matches_dict
        continue
print("last matches done!")


driver.close()
driver.quit()
matches_df = matches_df[matches_df.home_team_score.notnull()]
matches_df.to_csv("../CSV/Lists/"+str(league)+" "+str(year.replace("/","-"))+" Matches.csv")
