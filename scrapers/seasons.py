import pandas as pd
from selenium import webdriver
import os
import time
import pickle
import random as rn

driver = webdriver.Firefox(executable_path="C:/Users/Administrador.000/Downloads/geckodriver-v0.15.0-win64/geckodriver.exe")


#set seasons url

url = "https://www.whoscored.com/Regions/250/Tournaments/12/Europe-UEFA-Champions-League"
driver.get(url)

league = driver.find_element_by_css_selector("#breadcrumb-nav").find_element_by_css_selector("#tournaments").find_element_by_css_selector("[selected]").text
year = driver.find_element_by_css_selector("#breadcrumb-nav").find_element_by_css_selector("#seasons").find_element_by_css_selector("[selected]").text

seasons_df = pd.DataFrame(columns=["league","link","seasonid","season"])
seasons = driver.find_element_by_css_selector("#seasons").find_elements_by_css_selector("option")

for season in seasons:
    seasons_dict = {
        "league": league,
        "link": season.get_attribute("value"),
        "seasonid": season.get_attribute("value").split("/")[6],
        "season": season.text.replace("/","-"),
         }
    print(seasons_dict)
    seasons_df.loc[len(seasons_df)] = seasons_dict

driver.close()
driver.quit()
seasons_df.to_csv("../CSV/Lists/"+str(league)+" "+"Seasons"+".csv")
