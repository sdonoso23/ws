import pandas as pd
import json
import pickle
import os
import time

#set parameters name of tournament and season year

def events(tournament,year):

    print(time.strftime("%Y-%m-%d %H:%M:%S")," starting events table")
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
            events = match["events"]
        except UnicodeDecodeError:
            f = open(str(pathfiles)+file,"r",encoding="utf-8")
            match = json.load(f,encoding="utf-8")
            matchid = f.name.split("/")[4].replace(".json","")
            f.close()
            events = match["events"]
        for event in events:
            events_dict = {"wsmatchid":None,
                             "wseventid":None,
                             "matcheventid":None,
                             "minute":None,
                             "second":None,
                             "expandedminute":None,
                             "teamid":None,
                             "playerid":None,
                             "period":None,
                             "typeid":None,
                             "type":None,
                             "outcometype":None,
                             "istouch":None,
                             "x":None,
                             "y":None,
                             "endX":None,
                             "endY":None,}

            try:
                events_dict["wsmatchid"] = matchid
            except KeyError:
                events_dict["wsmatchid"] = None
            try:
                events_dict["wseventid"] = event["id"]
            except KeyError:
                events_dict["wseventid"] = None
            try:
                events_dict["minute"] = event["minute"]
            except KeyError:
                events_dict["minute"] = None
            try:
                events_dict["second"] = event["second"]
            except KeyError:
                events_dict["second"] = None
            try:
                events_dict["expandedminute"] = event["expandedMinute"]
            except KeyError:
                events_dict["expandedminute"] = None
            try:
                events_dict["teamid"] = event["teamId"]
            except KeyError:
                events_dict["teamid"] = None
            try:
                events_dict["playerid"] = event["playerId"]
            except KeyError:
                events_dict["playerid"] = None
            try:
                events_dict["period"] = event["period"]["displayName"]
            except KeyError:
                events_dict["period"] = None
            try:
                events_dict["typeid"] = event["type"]["value"]
            except KeyError:
                events_dict["typeid"] = None
            try:
                events_dict["type"] = event["type"]["displayName"]
            except KeyError:
                events_dict["type"] = None
            try:
                events_dict["outcometype"] = event["outcomeType"]["displayName"]
            except KeyError:
                events_dict["outcometype"] = None
            try:
                events_dict["istouch"] = event["isTouch"]
            except KeyError:
                events_dict["istouch"] = None
            try:
                events_dict["x"] = event["x"]
            except KeyError:
                events_dict["x"] = None
            try:
                events_dict["y"] = event["y"]
            except KeyError:
                events_dict["y"] = None
            try:
                events_dict["endX"] = event["endX"]
            except KeyError:
                events_dict["endX"] = None
            try:
                events_dict["endY"] = event["endY"]
            except KeyError:
                events_dict["endY"] = None

            aux_list.append(events_dict)


    print(time.strftime("%Y-%m-%d %H:%M:%S")," season done!")
    events_df = pd.DataFrame(aux_list)
    events_df = events_df[["wsmatchid","wseventid","minute","second","expandedminute","teamid","playerid","period","typeid",
                          "type","outcometype","istouch","x","y","endX","endY"]]
    events_df.index.name = "id"
    events_df.to_csv(savepath+"events.csv")
    print(time.strftime("%Y-%m-%d %H:%M:%S")," csv file done!")
