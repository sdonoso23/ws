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
        qualifiers = event["qualifiers"]
        for qualifier in qualifiers:
                qual_dict = {"wsmatchid":None,
                             "wseventid":None,
                             "matcheventid":None,
                             "qualid":None,
                             "qualname":None,
                             "qualvalue":None,
                            }
                try:
                    qual_dict["wsmatchid"] = matchid
                except KeyError:
                    qual_dict["wsmatchid"] = None
                try:
                    qual_dict["wseventid"] = event["id"]
                except KeyError:
                    qual_dict["wseventid"] = None
                try:
                    qual_dict["matcheventid"] = event["eventId"]
                except KeyError:
                    qual_dict["matcheventid"] = None
                try:
                    qual_dict["qualid"] = qualifier["type"]["value"]
                except KeyError:
                    qual_dict["qualid"] = None
                try:
                    qual_dict["qualname"] = qualifier["type"]["displayName"]
                except KeyError:
                    qual_dict["qualname"] = None
                try:
                    qual_dict["qualvalue"] = qualifier["value"]
                except KeyError:
                    qual_dict["qualvalue"] = None
                aux_list.append(qual_dict)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())," match done!")

qual_df = pd.DataFrame(aux_list)
qual_df = qual_df[["wsmatchid","wseventid","matcheventid","qualid","qualname","qualvalue"]]
qual_df.to_csv(savepath+"qualifiers.csv")
