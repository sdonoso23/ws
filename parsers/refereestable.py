import pandas as pd
import json
import pickle
import os
import time

#set parameters name of tournament and season year

def referees(tournament,year):
    print(time.strftime("%Y-%m-%d %H:%M:%S")," starting referees table")
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
        referees_dict = {"refereeid":None,
                        "refereename":None,
                           }
        try:
            referees_dict["refereeid"] = match["referee"]["officialId"]
        except KeyError:
            referees_dict["refereeid"] = None
        try:
            referees_dict["refereename"] = match["referee"]["name"]
        except KeyError:
            referees_dict["refereename"] = None
        aux_list.append(referees_dict)
    print(time.strftime("%Y-%m-%d %H:%M:%S")," season done!")
    referees_df = pd.DataFrame(aux_list)
    referees_df = referees_df.drop_duplicates("refereeid")
    referees_df = referees_df[["refereeid","refereename"]]
    referees_df.index.name = "id"
    referees_df.to_csv(savepath+"referees.csv")
    print(time.strftime("%Y-%m-%d %H:%M:%S")," csv file done!")
