import pandas as pd
from selenium import webdriver
import os
import time
import pickle
import random as rn

driver = webdriver.Firefox(executable_path="C:/Users/Administrador.000/Downloads/geckodriver-v0.15.0-win64/geckodriver.exe")

url = "https://www.whoscored.com/Regions/250/Tournaments/12/Seasons/1868"

driver.get(url)
league = driver.find_element_by_css_selector("#breadcrumb-nav").find_element_by_css_selector("#tournaments").find_element_by_css_selector("[selected]").text
year = driver.find_element_by_css_selector("#breadcrumb-nav").find_element_by_css_selector("#seasons").find_element_by_css_selector("[selected]").text

print("page got")
driver.find_element_by_css_selector("#sub-navigation").find_elements_by_css_selector("a")[1].click()
time.sleep(5)
matches_df = pd.DataFrame(columns=["league","year","matchid","home_team","away_team","home_team_score","away_team_score"])
matches = driver.find_element_by_id("tournament-fixture").find_elements_by_css_selector("tr")
matchcount = 0

print("starting first page")
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

driver.find_element_by_css_selector("#breadcrumb-nav").find_element_by_css_selector("#stages").find_elements_by_css_selector("option")[0].click()

time.sleep(5)
print("going to pages")

driver.find_element_by_css_selector("#sub-navigation").find_elements_by_css_selector("a")[1].click()

time.sleep(5)

print("going to fixture")

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
