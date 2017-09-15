import pandas as pd
from selenium import webdriver
import os
import time
import random as rn
import pickle


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

	def __setSeason__(self,season):

		self.season = season
		self.seasonid = self.seasons[season]

	def setParams(self,league,season):	

		self.__setLeague__(league)
		self.__seasonsList__()
		self.__setSeason__(season)

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

	

