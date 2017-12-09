import pandas as pd
from selenium import webdriver
import os
import time
import random as rn
import pickle
import copy


class Scraper:

	def __init__(self,leagues,jsonpath,listpath,driverpath):

		self.leagues = leagues
		self.path = jsonpath
		self.listpath = listpath
		self.driverpath = driverpath

	def __setLeague__(self,league):

	    self.league = league
	    self.countryid = self.leagues[self.league]["countryid"]
	    self.leagueid = self.leagues[self.league]["leagueid"]

	def __seasonsList__(self):
        
		if os.path.isfile(self.listpath+self.league+" Seasons.pkl"):
			with open(self.listpath+self.league+" Seasons.pkl","rb") as pkl: 
 				self.seasons = pickle.load(pkl)
		else:
			self.updateSeasons()
			with open(self.listpath+self.league+" Seasons.pkl","rb") as pkl: 
				self.seasons = pickle.load(pkl)

	def __matchesList__(self):
        
		if os.path.isfile(self.listpath+self.league+" "+self.season+" Matches.pkl"):
			with open(self.listpath+self.league+" "+self.season+" Matches.pkl","rb") as pkl: 
 				self.matches = pickle.load(pkl)
		else:
			self.updateMatchesList()
			with open(self.listpath+self.league+" "+self.season+" Matches.pkl","rb") as pkl: 
				self.matches = pickle.load(pkl)

	def __setSeason__(self,season):

		self.season = season
		self.seasonid = self.seasons[season]

	def setParams(self,league,season):	

		self.__setLeague__(league)
		self.__seasonsList__()
		self.__setSeason__(season)
		self.__matchesList__()

	def __openDriver__(self):

		self.driver = webdriver.Chrome(executable_path=self.driverpath)

	def __closeDriver__(self):	
		
		self.driver.close()
		self.driver.quit()

	def updateSeasons(self):

		self.__openDriver__()

		url = "https://www.whoscored.com/Regions/"+str(self.countryid)+"/Tournaments/"+str(self.leagueid) 
		
		self.driver.get(url)

		# Gets seasons list	
		seasons = self.driver.find_element_by_css_selector("#seasons").find_elements_by_css_selector("option")

		seasons_dict = {season.text.replace("/","-") : season.get_attribute("value").split("/")[6] for season in seasons}

		self.__closeDriver__()

		with open(self.listpath+self.league+" Seasons.pkl","wb") as f: 
			pickle.dump(seasons_dict,f)

	def updateMatchesList(self):

		self.__openDriver__()

		url = "https://www.whoscored.com/Regions/"+str(self.countryid)+"/Tournaments/"+str(self.leagueid)+"/Seasons/"+str(self.seasonid)
		
		self.driver.get(url)

		time.sleep(15)

		#try:
		#	self.driver.find_element_by_css_selector("#sub-navigation").find_elements_by_css_selector("a")[1].click()
		#except:
		#	time.sleep(10)
		#	self.driver.find_element_by_css_selector("#sub-navigation").find_elements_by_css_selector("a")[1].click()

		matches = self.driver.find_element_by_id("tournament-fixture").find_elements_by_css_selector("tr")

		agg = []

		while self.driver.find_element_by_id("date-controller").find_elements_by_css_selector("a")[0].get_attribute("title") == "View previous week":

			agg.append(self.__scrapeMatchesList__(matches))
			
			time.sleep(3)
			self.driver.find_element_by_id("date-controller").find_elements_by_css_selector("a")[0].click()
			time.sleep(5)
			matches = self.driver.find_element_by_id("tournament-fixture").find_elements_by_css_selector("tr")

		agg.append(self.__scrapeMatchesList__(matches))

		print ("last matches done!")

		self.__closeDriver__()

		matches_df = pd.concat(agg)
		matches_list = matches_df[matches_df.home_team_score.notnull()].drop_duplicates("matchid")["matchid"].tolist()

		with open(self.listpath+self.league+" "+self.season+" Matches.pkl","wb") as f: 
			pickle.dump(matches_list,f)

	def __scrapeMatchesList__(self,matches):

		matchcount = 0
		matches_df = pd.DataFrame(columns=["matchid","home_team_score","away_team_score"])

		
		for match in matches:
			if match.get_attribute("data-id") != None:
		            matches_dict = {
		                    "matchid": match.find_elements_by_css_selector("td")[4].find_element_by_css_selector("a").get_attribute("href").split("/")[4],
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
		    if os.path.exists(str(self.path)+str(self.league)+"/"+str(self.season)+"/"+str(match)+".json"):
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

	def __getMatches__(self,matches):
		

		count = 0

		for matchid in matches:
		    
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
		    if not os.path.exists(str(self.path)+"/"+str(self.league)+"/"+str(self.season)):
		        os.makedirs(str(self.path)+"/"+str(self.league)+"/"+str(self.season))
		    f = open(str(self.path)+"/"+str(self.league)+"/"+str(self.season)+"/"+str(matchid)+".json", 'w',encoding="utf-8")
		    count = count + 1
		    print(time.strftime("%Y-%m-%d %H:%M:%S")," ",count, "matches done " ,source_code[0],source_code[1],source_code[-1])
		    try:
		        f.write(source_code)
		    except UnicodeEncodeError:
		        pass
		        print("Unicode error")
		    f.close()
		    time.sleep(rn.randint(20,25))
	