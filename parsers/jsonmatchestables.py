import pandas as pd
import json
import pickle
import os
import time

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
    print(time.strftime("%Y-%m-%d %H:%M:%S")," csv file done!")


def satisfiedevents(tournament,year):
    print(time.strftime("%Y-%m-%d %H:%M:%S")," starting satisfied events table")
    savepath = "../CSV/"+tournament+"/"+year+"/"
    pathfiles = "../JSON/"+tournament+"/"+year+"/"
    files = os.listdir(pathfiles)
    if not os.path.exists(savepath):
                os.makedirs(savepath)

    #load satisfiedevents dictionary
    e = open("../JSON/Other/events.json","r")
    eventsindex = json.load(e)
    e.close()
    eventsindex = {v: k for k, v in eventsindex.items()}

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
                    aux_list.append(sevents_dict)
    print(time.strftime("%Y-%m-%d %H:%M:%S")," season done!")

    sevents_df = pd.DataFrame(aux_list)
    sevents_df = sevents_df[["wsmatchid","wseventid","matcheventid","satisfiedeventid","satisfiedeventname","satisfiedeventvalue"]]
    sevents_df.index.name = "id"
    sevents_df.to_csv(savepath+"satisfiedevents.csv")
    print(time.strftime("%Y-%m-%d %H:%M:%S")," csv file done!")

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

def qualifiers(tournament,year):

    print(time.strftime("%Y-%m-%d %H:%M:%S")," starting qualifiers table")
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

    print(time.strftime("%Y-%m-%d %H:%M:%S")," season done!")
    qual_df = pd.DataFrame(aux_list)
    qual_df = qual_df[["wsmatchid","wseventid","matcheventid","qualid","qualname","qualvalue"]]
    qual_df.index.name = "id"
    qual_df.to_csv(savepath+"qualifiers.csv")
    print(time.strftime("%Y-%m-%d %H:%M:%S")," csv file done!")

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


def alltables(tournament,year):
    print(time.strftime("%Y-%m-%d %H:%M:%S"),"starting ",tournament," ",year)
    matches(tournament,year)
    satisfiedevents(tournament,year)
    formations(tournament,year)
    events(tournament,year)
    qualifiers(tournament,year)
    teams(tournament,year)
    referees(tournament,year)
    players(tournament,year)
    print(time.strftime("%Y-%m-%d %H:%M:%S"),"finished ",tournament," ",year)
