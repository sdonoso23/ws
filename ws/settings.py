import json 


tourn = open("../data/tournaments.json","r",encoding="UTF-8")
b = json.load(tourn)
tournaments = { b[i]["name"] : {"countryid": b[i]["id"], 
                        "tournaments": {b[i]["tournaments"][k]["name"] : {"leagueid": b[i]["tournaments"][k]["id"]} \
                                        for k in range(len(b[i]["tournaments"]))}} for i in range(len(b))}



leagues = {"La Liga":{"countryid":206,"leagueid":4},
        "Bundesliga":{"countryid":81,"leagueid":3},
    	"Serie A":{"countryid":108,"leagueid":5},
    	"Premier League":{"countryid":252,"leagueid":2},
    	"Ligue 1":{"countryid":74,"leagueid":22}}

listpath = "../data/Lists/"
path = "../data/JSON/"
driverpath = "C:/Users/Administrador.000/Downloads/chromedriver_win32/chromedriver.exe"