import pandas as pd
from selenium import webdriver
import os
import time
import pickle
import random as rn


def databyid(matches,driver,path):

    
    for matchid in matches:
        url = "https://www.whoscored.com/Matches/" + str(matchid) + "/Live/"
        driver.get(url)
        text1 = driver.find_element_by_css_selector("#breadcrumb-nav").find_element_by_css_selector("a").text.split(" - ")
        league = text1[0]
        year = text1[1].replace("/","-")
        source_code = driver.page_source

    #search for piece with data
        start = "var matchCentreData = "
        end = ";\n"

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
        time.sleep(20)
    driver.close()
    driver.quit()

def databylist(league,year,number,driver,listpath,path):

    file = str(listpath)+str(league)+" "+str(year)+" Matches.csv"


    listofmatches = pd.read_csv(file,index_col=0)
    matches = listofmatches['matchid'].values.tolist()
    deletematches = []

    for match in matches:
        if os.path.exists(str(path)+str(league)+"/"+str(year)+"/"+str(match)+".json"):
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
        url = "https://www.whoscored.com/Matches/" + str(matchid) + "/Live/"
        driver.get(url)
        text1 = driver.find_element_by_css_selector("#breadcrumb-nav").find_element_by_css_selector("a").text.split(" - ")
        league = text1[0]
        year = text1[1].replace("/","-")
        source_code = driver.page_source

    #search for piece with data
        start = "var matchCentreData = "
        end = ";\n"

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
        time.sleep(rn.randint(20,25))

    driver.close()
    driver.quit()


def matcheslist(url,driver,listpath):


    driver.get(url)
    league = driver.find_element_by_css_selector("#breadcrumb-nav").find_element_by_css_selector("#tournaments").find_element_by_css_selector("[selected]").text
    year = driver.find_element_by_css_selector("#breadcrumb-nav").find_element_by_css_selector("#seasons").find_element_by_css_selector("[selected]").text
    time.sleep(20)
    try:
        driver.find_element_by_css_selector("#sub-navigation").find_elements_by_css_selector("a")[1].click()
    except:

        time.sleep(10)
        driver.find_element_by_css_selector("#sub-navigation").find_elements_by_css_selector("a")[1].click()

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
        time.sleep(10)
        driver.find_element_by_id("date-controller").find_elements_by_css_selector("a")[0].click()
        time.sleep(rn.randint(7,10))
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
    matches_df = matches_df.drop_duplicates("matchid")
    matches_df.to_csv(str(listpath)+str(league)+" "+str(year.replace("/","-"))+" Matches.csv")


def uclmatcheslist(url,driver,listpath):

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
    matches_df.to_csv(str(listpath)+str(league)+" "+str(year.replace("/","-"))+" Matches.csv")


def seasonslist(url,driver,listpath):
    
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
        seasons_df.loc[len(seasons_df)] = seasons_dict

    driver.close()
    driver.quit()
    seasons_df.to_csv(str(listpath)+str(league)+" "+"Seasons"+".csv")



def brasilmatcheslist(url,driver,listpath):


    driver.get(url)
    league = "Brasileirao"
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
    matches_df = matches_df.drop_duplicates("matchid")
    matches_df.to_csv(str(listpath)+str(league)+" "+str(year.replace("/","-"))+" Matches.csv")


def eredmatcheslist(url,driver,listpath):

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
    matches_df.to_csv(str(listpath)+str(league)+" "+str(year.replace("/","-"))+" Matches.csv")

def brasildatabylist(league,year,number,driver,listpath,path):

    file = str(listpath)+str(league)+" "+str(year)+" Matches.csv"


    listofmatches = pd.read_csv(file,index_col=0)
    matches = listofmatches['matchid'].values.tolist()
    deletematches = []

    for match in matches:
        if os.path.exists(str(path)+str(league)+"/"+str(year)+"/"+str(match)+".json"):
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
        url = "https://www.whoscored.com/Matches/" + str(matchid) + "/Live/"
        driver.get(url)
        text1 = driver.find_element_by_css_selector("#breadcrumb-nav").find_element_by_css_selector("a").text.split(" - ")
        source_code = driver.page_source

    #search for piece with data
        start = "var matchCentreData = "
        end = ";\n"

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
        time.sleep(rn.randint(20,25))

    driver.close()
    driver.quit()
