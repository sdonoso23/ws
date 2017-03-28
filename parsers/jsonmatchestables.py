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



# Players Table:


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
    teams = ["home","away"]
    players = range(0,len(match["home"]["players"])-1)
    for team in teams:
        for number in players:
            players_dict = {"wsmatchid":matchid,
                    "playerid":match[team]["players"][number]["playerId"],
                    "playername":match[team]["players"][number]["name"],
                    "position":match[team]["players"][number]["position"],
                    "shirtno":match[team]["players"][number]["shirtNo"],
                    "manofthematch":match[team]["players"][number]["isManOfTheMatch"],
                    "matchrating":None,
                    "height":match[team]["players"][number]["height"],
                    "weight":match[team]["players"][number]["weight"],
                    "age":match[team]["players"][number]["age"],
                            }
            try:
                ratings = match[team]["players"][number]["stats"]["ratings"]
                for rating in ratings:
                    dictratings = {"ratings":rating}
                players_dict["matchrating"] = match[team]["players"][number]["stats"]["ratings"][dictratings["ratings"]]
            except KeyError:
                players_dict["matchrating"] = None
            aux_list.append(players_dict)
    print(file," done")
players_df = pd.DataFrame(aux_list)
players_df = players_df[["wsmatchid","playerid","playername","position","shirtno","manofthematch",
                                          "matchrating","height","weight","age"]]
players_list = players_df.drop(["wsmatchid","position","shirtno","manofthematch","matchrating"],1)
players_list = players_list.drop_duplicates()
players_list = players_list[["playerid","playername"]]
players_df.to_csv(savepath+"players.csv")
players_list.to_csv(savepath+"playerslist.csv")


# Matches Table

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
    matches_dict = {
    "wsmatchid":f.name.split("/")[4].replace(".json",""),
    "league":f.name.split("/")[2],
    "season":f.name.split("/")[3],
    "date":match["startTime"],
    "hometeamid":match["home"]["teamId"],
    "awayteamid":match["away"]["teamId"],
    "homescore":match["score"].split(" : ")[0],
    "awayscore":match["score"].split(" : ")[1],
    "homepkscore":None,
    "awaypkscore":None,
    "referee":match["referee"]["name"],
    "managerhome":match["home"]["managerName"],
    "manageraway":match["away"]["managerName"],
    "attendance":match["attendance"],
    "venuename":match["venueName"],
               }
    if match["pkScore"] == '':
        matches_dict["homepkscore"] = None
        matches_dict["awaypkscore"] = None
    aux_list.append(matches_dict)

matches_df = pd.DataFrame(aux_list)
matches_df = matches_df[["wsmatchid","league","season","date","hometeamid","awayteamid","homescore","awayscore",
                         "homepkscore","awaypkscore","referee","managerhome","manageraway","attendance","venuename"]]
matches_df.to_csv(savepath+"matches.csv")


# Referees Table

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


# Team Table


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


# Qualifiers Table

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
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),matchid," match done!")


events_df = pd.DataFrame(aux_list)
events_df = events_df[["wsmatchid","wseventid","minute","second","expandedminute","teamid","playerid","period","typeid",
                      "type","outcometype","istouch","x","y","endX","endY"]]
events_df.to_csv(savepath+"events.csv")


# Satisfied Events Table

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
                qual_dict = {"wsmatchid":None,
                             "wseventid":None,
                             "matcheventid":None,
                             "satisfiedeventid":None,
                             "satisfiedeventname":None,
                             "satisfiedeventvalue":1,
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
                    qual_dict["satisfiedeventid"] = sevent
                except KeyError:
                    qual_dict["satisfiedeventid"] = None
                try:
                    qual_dict["satisfiedeventname"] = eventsindex[sevent]
                except KeyError:
                    qual_dict["satisfiedeventname"] = None
                aux_list.append(qual_dict)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())," match done!")

sevents_df = pd.DataFrame(aux_list)
sevents_df = sevents_df[["wsmatchid","wseventid","matcheventid","satisfiedeventid","satisfiedeventname","satisfiedeventvalue"]]
sevents_df.to_csv(savepath+"satisfiedevents.csv")


# Formations Table:

print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())," start time")

aux_list = []

for file in files:
    try:
        f = open(str(path)+file,"r")
        match = json.load(f)
        matchid = f.name.split("/")[4].replace(".json","")
        f.close()
        teams = ["home","away"]
    except UnicodeDecodeError:
        f = open(str(path)+file,"r",encoding="utf-8")
        match = json.load(f,encoding="utf-8")
        matchid = f.name.split("/")[4].replace(".json","")
        f.close()
        teams = ["home","away"]
    for team in teams:
        formations = match[team]["formations"]
        for formation in formations:
            numbers = [0,1,2,3,4,5,6,7,8,9,10]
            for number in numbers:
                formations_dict = {"wsmatchid":matchid,
                             "teamid":match[team]["teamId"],
                             "formationid":formation["formationId"],
                             "formationname":formation["formationName"]  ,
                             "captainplayerid":formation["captainPlayerId"],
                             "period":formation["period"],
                             "startminute":formation["startMinuteExpanded"],
                             "endminute":formation["endMinuteExpanded"],
                             "playerid":formation["playerIds"][number],
                             "slotnumber":"player "+str(number+1),
                             "xposition":formation["formationPositions"][number]["vertical"],
                             "yposition":formation["formationPositions"][number]["horizontal"],
                             "subonplayerid":None,
                             "suboffplayerid":None,

                            }
                try:
                    formations_dict["subonplayerid"] = formation["subOnPlayerId"]
                except KeyError:
                    formations_dict["subonplayerid"] = None
                try:
                    formations_dict["suboffplayerid"] = formation["subOffPlayerId"]
                except KeyError:
                    formations_dict["suboffplayerid"] = None
                aux_list.append(formations_dict)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())," match done!")

formations_df = pd.DataFrame(aux_list)
formations_df = formations_df[["wsmatchid","teamid","formationid","formationname","captainplayerid","period","startminute",
                              "endminute","playerid","slotnumber","xposition","yposition","subonplayerid","suboffplayerid"]]
formations_df.to_csv(savepath+"formations.csv")
