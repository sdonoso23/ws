import json 
from pymongo import MongoClient

tourn = open("../data/tournaments.json","r",encoding="UTF-8")
b = json.load(tourn)
TOURNAMENTS = { b[i]["name"] : {"countryid": b[i]["id"], 
                        "tournaments": {b[i]["tournaments"][k]["name"] : {"leagueid": b[i]["tournaments"][k]["id"]} \
                                        for k in range(len(b[i]["tournaments"]))}} for i in range(len(b))}



LEAGUES = {"La Liga":{"countryid":206,"leagueid":4},
        "Bundesliga":{"countryid":81,"leagueid":3},
    	"Serie A":{"countryid":108,"leagueid":5},
    	"Premier League":{"countryid":252,"leagueid":2},
    	"Ligue 1":{"countryid":74,"leagueid":22},
    	"Brasileirao":{"countryid":31,"leagueid":95},
    	"Eredivisie":{"countryid":155,"leagueid":13},
    	"Russian Premier League":{"countryid":182,"leagueid":77},
    	"Chinese Super League":{"countryid":45,"leagueid":162},
    	"Liga NOS":{"countryid":177,"leagueid":21},
    	"Super Lig":{"countryid":225,"leagueid":17},
    	"Primera Argentina":{"countryid":11,"leagueid":68},
    	"UEFA Champions League":{"countryid":250,"leagueid":12},
    	"UEFA Europa League":{"countryid":250,"leagueid":30},
        "FIFA World Cup":{"countryid":247,"leagueid":36},
        "Major League Soccer":{"countryid":233,"leagueid":85}}


LISTPATH = "../data/lists/"
JSONPATH = "../data/json/"
DRIVERPATH = "../../software/chromedriver/chromedriver"
SEASON_DEPTH = 10


CLIENT = MongoClient()
DB = CLIENT["football"]
