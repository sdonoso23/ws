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



print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())," start time")

aux_list = []

for file in files:
    try:
        f = open(str(path)+file,"r")
        match = json.load(f)
        matchid = f.name.split("/")[4].replace(".json","")
        f.close()
        events = match["events"]
    except UnicodeDecodeError:
        f = open(str(path)+file,"r",encoding="utf-8")
        match = json.load(f,encoding="utf-8")
        matchid = f.name.split("/")[4].replace(".json","")
        f.close()
        events = match["events"]
    for event in events:
        sevents = event["satisfiedEventsTypes"]
        for sevent in sevents:
                sevents_dict = {"wsmatchid":None,
                             "wseventid":None,
                             "matcheventid":None,
                             "satisfiedeventid":None,
                             "satisfiedeventname":None,
                             "satisfiedeventvalue":1,
                            }
                try:
                    sevents_dict["wsmatchid"] = matchid
                except KeyError:
                    sevents_dict["wsmatchid"] = None
                try:
                    sevents_dict["wseventid"] = event["id"]
                except KeyError:
                    sevents_dict["wseventid"] = None
                try:
                    sevents_dict["matcheventid"] = event["eventId"]
                except KeyError:
                    sevents_dict["matcheventid"] = None
                try:
                    sevents_dict["satisfiedeventid"] = sevent
                except KeyError:
                    sevents_dict["satisfiedeventid"] = None
                try:
                    sevents_dict["satisfiedeventname"] = eventsindex[sevent]
                except KeyError:
                    sevents_dict["satisfiedeventname"] = None
                aux_list.append(qual_dict)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())," match done!")

sevents_df = pd.DataFrame(aux_list)
sevents_df = sevents_df[["wsmatchid","wseventid","matcheventid","satisfiedeventid","satisfiedeventname","satisfiedeventvalue"]]
sevents_df.to_csv(savepath+"satisfiedevents.csv")
