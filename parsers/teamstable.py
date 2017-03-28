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




teams = ["home","away"]
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
    for team in teams:
        teams_dict = {
        "teamid":match[team]["teamId"],
        "teamname":match[team]["name"],
                   }
        aux_list.append(teams_dict)

teams_df = pd.DataFrame(aux_list)
teams_df = teams_df.drop_duplicates()
teams_df = teams_df[["teamid","teamname"]]
teams_df.to_csv(savepath+"teams.csv")
