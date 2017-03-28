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
        referees_dict = {"refereeid":match["referee"]["officialId"],
                    "referee":match["referee"]["name"],
                       }
        aux_list.append(referees_dict)
    print(file," done")
referees_df = pd.DataFrame(aux_list)
referees_df = referees_df.drop_duplicates()
referees_df = referees_df[["refereeid","referee"]]
referees_df.to_csv(savepath+"referees.csv")
