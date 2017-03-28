import pandas as pd
import json
import pickle
import os
import time

#set parameters name of tournament and season year

tournament="La Liga"
year="2015-2016"


path = "../JSON/"+tournament+"/"+year+"/"
files = os.listdir(path)
savepath = "../CSV/"+tournament+"/"+year+"/"
if not os.path.exists(savepath):
            os.makedirs(savepath)

#load satisfiedevents dictionary
e = open("../JSON/Other/events.json","r")
eventsindex = json.load(e)
e.close()
eventsindex = {v: k for k, v in eventsindex.items()}

aux_list=[]

for file in files:
    try:
        f = open(str(path)+file,"r")
        match = json.load(f)
        matchid = f.name.split("/")[4].replace(".json","")
        f.close()
    except UnicodeDecodeError:
        f = open(str(path)+file,"r",encoding="utf-8")
        match = json.load(f,encoding="utf-8")
        matchid = f.name.split("/")[4].replace(".json","")
        f.close()
    teams = ["home","away"]
    players = range(0,len(match["home"]["players"])-1)
    for team in teams:
        for number in players:
            players_dict = {"wsmatchid":matchid,
                    "playerid":match[team]["players"][number]["playerId"],
                    "playername":match[team]["players"][number]["name"],
                    "position":match[team]["players"][number]["position"],
                    "shirtno":match[team]["players"][number]["shirtNo"],
                    "manofthematch":match[team]["players"][number]["isManOfTheMatch"],
                    "matchrating":None,
                    "height":match[team]["players"][number]["height"],
                    "weight":match[team]["players"][number]["weight"],
                    "age":match[team]["players"][number]["age"],
                            }
            try:
                ratings = match[team]["players"][number]["stats"]["ratings"]
                for rating in ratings:
                    dictratings = {"ratings":rating}
                players_dict["matchrating"] = match[team]["players"][number]["stats"]["ratings"][dictratings["ratings"]]
            except KeyError:
                players_dict["matchrating"] = None
            aux_list.append(players_dict)
    print(file," done")
players_df = pd.DataFrame(aux_list)
players_df = players_df[["wsmatchid","playerid","playername","position","shirtno","manofthematch",
                                          "matchrating","height","weight","age"]]
players_list = players_df.drop(["wsmatchid","position","shirtno","manofthematch","matchrating"],1)
players_list = players_list.drop_duplicates()
players_list = players_list[["playerid","playername"]]
players_df.to_csv(savepath+"players.csv")
players_list.to_csv(savepath+"playerslist.csv")
