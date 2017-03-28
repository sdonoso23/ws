import pandas as pd
import json
import pickle
import os
import time

#set parameters name of tournament and season year

def players(tournament,year):
    print(time.strftime("%Y-%m-%d %H:%M:%S")," starting players table")
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
        teams = ["home","away"]
        players = range(0,len(match["home"]["players"])-1)
        for team in teams:
            for number in players:
                players_dict = {"wsmatchid":None,
                        "playerid":None,
                        "playername":None,
                        "position":None,
                        "shirtno":None,
                        "manofthematch":None,
                        "matchrating":None,
                        "height":None,
                        "weight":None,
                        "age":None,
                                }
                try:
                    players_dict["wsmatchid"] = matchid
                except KeyError:
                    players_dict["wsmatchid"] = None
                try:
                    players_dict["playerid"] = match[team]["players"][number]["playerId"]
                except KeyError:
                    players_dict["playerid"] = None
                try:
                    players_dict["playername"] = match[team]["players"][number]["name"]
                except KeyError:
                    players_dict["playername"] = None
                try:
                    players_dict["position"] = match[team]["players"][number]["position"]
                except KeyError:
                    players_dict["position"] = None
                try:
                    players_dict["shirtno"] = match[team]["players"][number]["shirtNo"]
                except KeyError:
                    players_dict["shirtno"] = None
                try:
                    players_dict["manofthematch"] = match[team]["players"][number]["isManOfTheMatch"]
                except KeyError:
                    players_dict["manofthematch"] = None
                try:
                    ratings = match[team]["players"][number]["stats"]["ratings"]
                    for rating in ratings:
                        dictratings = {"ratings":rating}
                    players_dict["matchrating"] = match[team]["players"][number]["stats"]["ratings"][dictratings["ratings"]]
                except KeyError:
                    players_dict["matchrating"] = None
                try:
                    players_dict["height"] = match[team]["players"][number]["height"]
                except KeyError:
                    players_dict["height"] = None
                try:
                    players_dict["weight"] = match[team]["players"][number]["weight"]
                except KeyError:
                    players_dict["weight"] = None
                try:
                    players_dict["age"] = match[team]["players"][number]["age"]
                except KeyError:
                    players_dict["age"] = None
                aux_list.append(players_dict)
    print(time.strftime("%Y-%m-%d %H:%M:%S")," season done!")
    players_df = pd.DataFrame(aux_list)
    players_df = players_df[["wsmatchid","playerid","playername","position","shirtno","manofthematch",
                                              "matchrating","height","weight","age"]]
    players_list = players_df.drop(["wsmatchid","position","shirtno","manofthematch","matchrating"],1)
    players_list = players_list.drop_duplicates("playerid")
    players_list = players_list[["playerid","playername"]]
    players_df.index.name = "id"
    players_list.index.name = "id"
    players_df.to_csv(savepath+"players.csv")
    players_list.to_csv(savepath+"playerslist.csv")
    print(time.strftime("%Y-%m-%d %H:%M:%S")," csv file done!")
