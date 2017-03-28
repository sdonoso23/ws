import pandas as pd
import json
import pickle
import os
import time

#set parameters name of tournament and season year

def teams(tournament,year):

    print(time.strftime("%Y-%m-%d %H:%M:%S")," starting teams table")
    savepath = "../CSV/"+tournament+"/"+year+"/"
    pathfiles = "../JSON/"+tournament+"/"+year+"/"
    files = os.listdir(pathfiles)
    if not os.path.exists(savepath):
                os.makedirs(savepath)

    teams = ["home","away"]
    aux_list=[]
    for file in files:
        try:
            f = open(str(pathfiles)+file,"r")
            match = json.load(f)
            matchid = f.name.split("/")[4].replace(".json","")
            f.close()
        except UnicodeDecodeError:
            f = open(str(pathfiles)+file,"r",encoding="utf-8")
            match = json.load(f,encoding="utf-8")
            matchid = f.name.split("/")[4].replace(".json","")
            f.close()
        for team in teams:
            teams_dict = {
            "teamid":None,
            "teamname":None,
                       }
            try:
                teams_dict["teamid"] = match[team]["teamId"]
            except KeyError:
                teams_dict["teamid"] = None
            try:
                teams_dict["teamname"] = match[team]["name"]
            except KeyError:
                teams_dict["teamname"] = None
            aux_list.append(teams_dict)
    print(time.strftime("%Y-%m-%d %H:%M:%S")," season done!")
    teams_df = pd.DataFrame(aux_list)
    teams_df = teams_df.drop_duplicates("teamid")
    teams_df = teams_df[["teamid","teamname"]]
    teams_df.index.name = "id"
    teams_df.to_csv(savepath+"teams.csv")
    print(time.strftime("%Y-%m-%d %H:%M:%S")," csv file done!")
