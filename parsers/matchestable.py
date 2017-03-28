import pandas as pd
import json
import pickle
import os
import time

#set parameters name of tournament and season year

def matches(tournament,year):
    print(time.strftime("%Y-%m-%d %H:%M:%S")," starting matches table")
    savepath = "../CSV/"+tournament+"/"+year+"/"
    pathfiles = "../JSON/"+tournament+"/"+year+"/"
    files = os.listdir(pathfiles)
    if not os.path.exists(savepath):
                os.makedirs(savepath)

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
        matches_dict = {
        "wsmatchid":None,
        "league":None,
        "season":None,
        "date":None,
        "hometeamid":None,
        "awayteamid":None,
        "homescore":None,
        "awayscore":None,
        "homepkscore":None,
        "awaypkscore":None,
        "referee":None,
        "managerhome":None,
        "manageraway":None,
        "attendance":None,
        "venuename":None,
                   }
        if match["pkScore"] == '':
            matches_dict["homepkscore"] = None
            matches_dict["awaypkscore"] = None
        try:
            matches_dict["wsmatchid"] = matchid
        except KeyError:
            matches_dict["wsmatchid"] = None
        try:
            matches_dict["league"] = tournament
        except KeyError:
            matches_dict["league"] = None
        try:
            matches_dict["season"] = year
        except KeyError:
            matches_dict["season"] = None
        try:
            matches_dict["date"] = match["startTime"].replace("T"," ")
        except KeyError:
            matches_dict["date"] = None
        try:
            matches_dict["hometeamid"] = match["home"]["teamId"]
        except KeyError:
            matches_dict["hometeamid"] = None
        try:
            matches_dict["awayteamid"] = match["away"]["teamId"]
        except KeyError:
            matches_dict["awayteamid"] = None
        try:
            matches_dict["homescore"] = match["score"].split(" : ")[0]
        except KeyError:
            matches_dict["homescore"] = None
        try:
            matches_dict["awayscore"] = match["score"].split(" : ")[1]
        except KeyError:
            matches_dict["awayscore"] = None
        try:
            if match["pkScore"] == '':
                matches_dict["homepkscore"] = None
                matches_dict["awaypkscore"] = None
            else:
                matches_dict["homepkscore"] = match["pkScore"].split(" : ")[0]
                matches_dict["awaypkscore"] = match["pkScore"].split(" : ")[1]
        except KeyError:
            matches_dict["homepkscore"] = None
            matches_dict["awaypkscore"] = None
        try:
            matches_dict["referee"] = match["referee"]["name"]
        except KeyError:
            matches_dict["referee"] = None
        try:
            matches_dict["managerhome"] = match["home"]["managerName"]
        except KeyError:
            matches_dict["managerhome"] = None
        try:
            matches_dict["manageraway"] = match["away"]["managerName"]
        except KeyError:
            matches_dict["manageraway"] = None
        try:
            matches_dict["attendance"] = match["attendance"]
        except KeyError:
            matches_dict["attendance"] = None
        try:
            matches_dict["venuename"] = match["venueName"]
        except KeyError:
            matches_dict["venuename"] = None
        aux_list.append(matches_dict)
    print(time.strftime("%Y-%m-%d %H:%M:%S")," season done!")

    matches_df = pd.DataFrame(aux_list)
    matches_df = matches_df[["wsmatchid","league","season","date","hometeamid","awayteamid","homescore","awayscore",
                            "homepkscore","awaypkscore","referee","managerhome","manageraway","attendance","venuename"]]
    matches_df.index.name = "id"
    matches_df.to_csv(savepath+"matches.csv")
