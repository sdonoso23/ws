import pandas as pd
import json
import pickle
import os
import time

#set parameters name of tournament and season year

def formations(tournament,year):

    print(time.strftime("%Y-%m-%d %H:%M:%S")," starting formations table")
    savepath = "../CSV/"+tournament+"/"+year+"/"
    pathfiles = "../JSON/"+tournament+"/"+year+"/"
    files = os.listdir(pathfiles)
    if not os.path.exists(savepath):
                os.makedirs(savepath)

    aux_list = []

    for file in files:
        try:
            f = open(str(pathfiles)+file,"r")
            match = json.load(f)
            matchid = f.name.split("/")[4].replace(".json","")
            f.close()
            teams = ["home","away"]
        except UnicodeDecodeError:
            f = open(str(pathfiles)+file,"r",encoding="utf-8")
            match = json.load(f,encoding="utf-8")
            matchid = f.name.split("/")[4].replace(".json","")
            f.close()
            teams = ["home","away"]
        for team in teams:
            formations = match[team]["formations"]
            for formation in formations:
                numbers = [0,1,2,3,4,5,6,7,8,9,10]
                for number in numbers:
                    formations_dict = {"wsmatchid":None,
                                 "teamid":None,
                                 "formationid":None,
                                 "formationname":None,
                                 "captainplayerid":None,
                                 "period":None,
                                 "startminute":None,
                                 "endminute":None,
                                 "playerid":None,
                                 "slotnumber":"player"+str(number+1),
                                 "xposition":None,
                                 "yposition":None,
                                 "subonplayerid":None,
                                 "suboffplayerid":None,
                                }
                    try:
                        formations_dict["wsmatchid"] = matchid
                    except KeyError:
                        formations_dict["wsmatchid"] = None
                    try:
                        formations_dict["teamid"] = match[team]["teamId"]
                    except KeyError:
                        formations_dict["teamid"] = None
                    try:
                        formations_dict["formationid"] = formation["formationId"]
                    except KeyError:
                        formations_dict["formationid"] = None
                    try:
                        formations_dict["formationname"] = formation["formationName"]
                    except KeyError:
                        formations_dict["formationname"] = None
                    try:
                        formations_dict["captainplayerid"] = formation["captainPlayerId"]
                    except KeyError:
                        formations_dict["captainplayerid"] = None
                    try:
                        formations_dict["period"] = formation["period"]
                    except KeyError:
                        formations_dict["period"] = None
                    try:
                        formations_dict["startminute"] = formation["startMinuteExpanded"]
                    except KeyError:
                        formations_dict["startminute"] = None
                    try:
                        formations_dict["endminute"] = formation["endMinuteExpanded"]
                    except KeyError:
                        formations_dict["endminute"] = None
                    try:
                        formations_dict["playerid"] = formation["playerIds"][number]
                    except KeyError:
                        formations_dict["playerid"] = None
                    try:
                        formations_dict["xposition"] = formation["formationPositions"][number]["vertical"]
                    except KeyError:
                        formations_dict["xpoisiton"] = None
                    try:
                        formations_dict["yposition"] = formation["formationPositions"][number]["horizontal"]
                    except KeyError:
                        formations_dict["yposition"] = None
                    try:
                        formations_dict["subonplayerid"] = formation["subOnPlayerId"]
                    except KeyError:
                        formations_dict["subonplayerid"] = None
                    try:
                        formations_dict["suboffplayerid"] = formation["subOffPlayerId"]
                    except KeyError:
                        formations_dict["suboffplayerid"] = None
                    aux_list.append(formations_dict)
    print(time.strftime("%Y-%m-%d %H:%M:%S")," season done!")

    formations_df = pd.DataFrame(aux_list)
    formations_df = formations_df[["wsmatchid","teamid","formationid","formationname","captainplayerid","period","startminute",
                                  "endminute","playerid","slotnumber","xposition","yposition","subonplayerid","suboffplayerid"]]
    formations_df.index.name = "id"
    formations_df.to_csv(savepath+"formations.csv")
    print(time.strftime("%Y-%m-%d %H:%M:%S")," csv file done!")
