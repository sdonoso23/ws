import pandas as pd
from selenium import webdriver
import os
import time
import random as rn
import pickle
import copy
from ws.constants import LEAGUES, LISTPATH, JSONPATH, DRIVERPATH, SEASON_DEPTH

class Scraper:

    def __init__(self,league,jsonpath=JSONPATH,listpath=LISTPATH,driverpath=DRIVERPATH,season_depth = SEASON_DEPTH):

        self.league = league
        self.leaguename = self.league.lower().replace(" ","_")
        self.countryid = LEAGUES[self.league]["countryid"]
        self.leagueid = LEAGUES[self.league]["leagueid"]
        self.season_depth = season_depth

        self.path = jsonpath
        self.listpath = listpath
        self.driverpath = driverpath

        self.__seasonsList__()
        self.season = sorted(self.seasons.keys(),reverse=True)[0]
        self.seasonid = self.seasons[self.season].get("id", None)
        self.stages = self.seasons[self.season].get("stages", None)
        self.stage = None
        self.broken = False

        self.seasonpath = self.__createPath__()
        try:
            self.savedmatches = list(map(lambda x: x.split(".")[0], list(filter(lambda x: ".json" in x, os.listdir(self.seasonpath)))))
        except:
            self.savedmatches = []

        self.__matchesList__()

    def __createPath__(self):

        path = str(self.path) + "/" + str(self.leaguename) + "/" + str(self.season)+"/"
        if not os.path.exists(path):
            os.makedirs(path)

        return str(self.path) + "/" + str(self.leaguename) + "/" + str(self.season)+"/"

    def setSeason(self,season):

        self.season = season
        self.seasonid = self.seasons[self.season]["id"]
        self.stages = self.seasons[self.season].get("stages", None)
        self.seasonpath = self.__createPath__()
        self.savedmatches = list(map(lambda x: x.split(".")[0],
                                     list(filter(lambda x: ".json" in x, os.listdir(self.seasonpath)))))
        self.__matchesList__()

        return self

    def setStage(self,stage):

        try:
            self.stageid = self.seasons[self.season]["stages"][stage]
            self.stage = stage
        except KeyError:
            print("Warning: Season without stages")

        return self

    def getInfo(self):

        print("League: %s" % self.league)
        print("Season: %s" % self.season)
        print("Stage: %s" % self.stage)
        print("Available matches: %i" % len(self.matches))
        print("Saved Matches: %i" % len(self.savedmatches))
        print("Save path: %s" % self.path)
        print("List path: %s" % self.listpath)
        print("Driver path: %s" % self.driverpath)


    def __seasonsList__(self):
        
        if os.path.isfile(self.listpath+self.leaguename+"_seasons.pkl"):
            with open(self.listpath+self.leaguename+"_seasons.pkl","rb") as pkl:
                self.seasons = pickle.load(pkl)
        else:
            self.updateSeasons()
            with open(self.listpath+self.leaguename+"_seasons.pkl","rb") as pkl:
                self.seasons = pickle.load(pkl)

        return self.seasons

    def __matchesList__(self):
        
        if os.path.isfile(self.listpath+self.leaguename+"_"+self.season+"_matches.pkl"):
            with open(self.listpath+self.leaguename+"_"+self.season+"_matches.pkl","rb") as pkl:
                self.matches = pickle.load(pkl)
        else:
            self.updateMatchesList()
            with open(self.listpath+self.leaguename+"_"+self.season+"_matches.pkl","rb") as pkl:
                self.matches = pickle.load(pkl)

        return self.matches

    def __openDriver__(self):

        self.driver = webdriver.Chrome(executable_path=self.driverpath)

        return self

    def __closeDriver__(self):

        self.driver.close()
        self.driver.quit()

        return self

    def updateSeasons(self):

        self.__openDriver__()

        url = "https://www.whoscored.com/Regions/"+str(self.countryid)+"/Tournaments/"+str(self.leagueid)

        self.driver.get(url)

        # Gets seasons list
        seasons = self.driver.find_element_by_css_selector("#seasons").find_elements_by_css_selector("option")

        length = self.season_depth if len(seasons) > self.season_depth else seasons

        d = {}
        for i in range(length):

            s = seasons[i]
            name = s.text.replace("/","-")
            ids = s.get_attribute("value").split("/")[6]
            s.click()

            try:
                stages = self.driver.find_element_by_css_selector("#stages").find_elements_by_css_selector("option")
                st_d = {stage.text: stage.get_attribute("value").split("/")[8] for stage in stages}
                d[name] = {"id": ids,
                           "stages": st_d}
            except:
                d[name] = {"id": ids}

            seasons = self.driver.find_element_by_css_selector("#seasons").find_elements_by_css_selector("option")

            time.sleep(5)


        self.__closeDriver__()

        with open(self.listpath+self.leaguename+"_seasons.pkl","wb") as f:
            pickle.dump(d,f)

        self.__seasonsList__()

        return self.seasons
        

    def updateMatchesList(self):

        self.__openDriver__()

        if self.stage is None:
            url = "https://www.whoscored.com/Regions/"+str(self.countryid)+"/Tournaments/"+str(self.leagueid)+"/Seasons/"+str(self.seasonid)
        else:
            url = "https://www.whoscored.com/Regions/"+str(self.countryid)+"/Tournaments/"+str(self.leagueid)+"/Seasons/"+str(self.seasonid)+"/Stages/"+str(self.stageid)

        self.driver.get(url)

        time.sleep(3)

        matches = self.driver.find_element_by_id("tournament-fixture").find_elements_by_css_selector("tr")
        agg = []

        el = self.driver.find_element_by_id("date-controller").find_elements_by_css_selector("a")[0]
        loc = el.location_once_scrolled_into_view
        self.driver.execute_script("window.scrollTo(%i, %i)" % (loc["x"],loc["y"]))


        while self.driver.find_element_by_id("date-controller").find_elements_by_css_selector("a")[0].get_attribute("title") == "View previous week":

            agg.append(self.__scrapeMatchesList__(matches))

            try:
                el.click()
                time.sleep(1)
                matches = self.driver.find_element_by_id("tournament-fixture").find_elements_by_css_selector("tr")
            except:
                print("scraping error")
                break


        agg.append(self.__scrapeMatchesList__(matches))

        print ("last matches done!")

        self.__closeDriver__()

        matches_df = pd.concat(agg)
        matches_list = matches_df[matches_df.home_team_score.notnull()].drop_duplicates("matchid")["matchid"].tolist()
        matches_list = list(set(self.savedmatches+matches_list))

        with open(self.listpath+self.leaguename+"_"+self.season+"_matches.pkl","wb") as f:
            pickle.dump(matches_list,f)

        self.__matchesList__()
        self.broken = False

        return self

    def __scrapeMatchesList__(self,matches):

        matchcount = 0
        matches_df = pd.DataFrame(columns=["matchid","home_team_score","away_team_score"])


        for match in matches:


            if match.get_attribute("data-id") != None:

                    matchid = match.find_elements_by_css_selector("td")[4].find_element_by_css_selector("a").get_attribute("href").split("/")[4]

                    matches_dict = {
                            "matchid": matchid,
                            "home_team_score": None,
                            "away_team_score": None,
                             }
                    if match.find_elements_by_css_selector("td")[4].find_element_by_css_selector("a").text != "vs":
                        matches_dict["home_team_score"] = match.find_elements_by_css_selector("td")[4].find_element_by_css_selector("a").text.split(" : ")[0]
                        matches_dict["away_team_score"] = match.find_elements_by_css_selector("td")[4].find_element_by_css_selector("a").text.split(" : ")[1]
                    matches_df.loc[len(matches_df)] = matches_dict
                    matchcount = matchcount+1

        print(matchcount, " matches done!")

        return matches_df


    def __checkMatches__(self):

        listofmatches = copy.copy(self.matches)
        deletematches = []

        for match in listofmatches:
            if os.path.exists(str(self.path)+str(self.leaguename)+"/"+str(self.season)+"/"+str(match)+".json"):
                deletematches.append(match)

        print("you already have ", len(deletematches)," matches")
        print("you are missing", len(listofmatches)-len(deletematches)," matches")

        if len(deletematches) > 0:
            for match in deletematches:
                listofmatches.remove(match)

        return listofmatches

    def getMatches(self,number):

        matches = self.__checkMatches__()[0:number]

        print("starting scraping of ",len(matches)," matches")

        self.__openDriver__()

        self.__getMatches__(matches)

        self.__closeDriver__()

        return self

    def __getMatches__(self,matches):

        path = self.__createPath__()

        count = 0

        for matchid in matches:

            count = count + 1
            url = "https://www.whoscored.com/Matches/" + str(matchid) + "/Live/"
            self.driver.get(url)
            source_code = self.driver.page_source

        #search for piece with data
            start = "var matchCentreData = "
            end = ";\n"

        #remove useless info
            try:
                source_code = source_code.split(start)[1].split(end)[0]
            except IndexError as e:
                print(matchid," Error")
                continue

            try:
                f = open(path + str(matchid) + ".json",
                    'w', encoding="utf-8")
                f.write(source_code)
                print(time.strftime("%Y-%m-%d %H:%M:%S"), " ", count, "matches done ", source_code[0], source_code[1],
                      source_code[-1])
            except UnicodeEncodeError:
                print(matchid,"Unicode error")

            f.close()
            time.sleep(rn.randint(20,25))

        self.savedmatches = list(
            map(lambda x: x.split(".")[0], list(filter(lambda x: ".json" in x, os.listdir(self.seasonpath)))))

        print ("Total count of saved matches with new: %i" % len(self.savedmatches))

        return self