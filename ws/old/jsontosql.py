import pandas as pd
import json
import pickle
import os
import time
import sqlite3


def matchtosql(conn,path,tournament,year,status):
	print(time.strftime("%Y-%m-%d %H:%M:%S")," starting")
	pathfiles = path+"/"+"JSON/"+tournament+"/"+year+"/"
	files = os.listdir(pathfiles)

	matcheslist = pd.read_sql("Select * from matches",conn)["wsmatchid"].values.tolist()

	fileslist=[]

	for match in matcheslist:
	    match=str(match)+".json"
	    fileslist.append(match)

	filesfinal=[]

	for file in files:
	    if file not in fileslist:
	        filesfinal.append(file)
				
	totalcount = len(filesfinal)
	count = 0
	        
	for file in filesfinal:
	        match_list = []
	        f = open(str(pathfiles)+file,"r",encoding="utf-8")
	        match = json.load(f,encoding="utf-8")
	        matchid = f.name.split("/")[10].replace(".json","")
	        f.close()

	        matches_dict = {
	        "wsmatchid":None,
	        "league":None,
	        "season":None,
	        "date":None,
	        "hometeamid":None,
	        "awayteamid":None,
	        "hometeamname":None,
	        "awayteamname":None,
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
	            matches_dict["hometeamname"] = match["home"]["name"]
	        except KeyError:
	            matches_dict["hometeamname"] = None
	        try:
	            matches_dict["awayteamname"] = match["away"]["name"]
	        except KeyError:
	            matches_dict["awayteamname"] = None
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
	        match_list.append(matches_dict)
	        matches_df = pd.DataFrame(match_list)
	        matches_df = matches_df[["wsmatchid","league","season","date","hometeamid","awayteamid","hometeamname","awayteamname","homescore","awayscore",
	                            "homepkscore","awaypkscore","referee","managerhome","manageraway","attendance","venuename"]]
	        matches_df.to_sql("matches",conn,if_exists=status,index=False)
	        
	        events = match["events"]
	        event_list=[]
	        qual_list=[]
	        for event in events:
	            events_dict = {"keyid":None,
	                            "wsmatchid":None,
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
	                             "x":None,
	                             "y":None,}
	            try:
	                events_dict["keyid"] = str(matchid)+str(event["id"])
	            except KeyError:
	                events_dict["keyid"] = None
	            try:
	                events_dict["wsmatchid"] = matchid
	            except KeyError:
	                events_dict["wsmatchid"] = None
	            try:
	                events_dict["wseventid"] = str(event["id"])
	            except KeyError:
	                events_dict["wseventid"] = None
	            try:
	                events_dict["matcheventid"] = event["eventId"]
	            except KeyError:
	                events_dict["matcheventid"] = None
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
	                events_dict["x"] = event["x"]
	            except KeyError:
	                events_dict["x"] = None
	            try:
	                events_dict["y"] = event["y"]
	            except KeyError:
	                events_dict["y"] = None

	            event_list.append(events_dict)
	            
	            qualifiers = event["qualifiers"]
	            for qualifier in qualifiers:
	                    qual_dict = {"keyid":None,
	                                 "wsmatchid":None,
	                                 "wseventid":None,
	                                 "matcheventid":None,
	                                 "qualid":None,
	                                 "qualname":None,
	                                 "qualvalue":None,
	                                }
	                    try:
	                        qual_dict["keyid"] = str(matchid)+str(event["id"])
	                    except KeyError:
	                        qual_dict["keyid"] = None
	                    try:
	                        qual_dict["wsmatchid"] = matchid
	                    except KeyError:
	                        qual_dict["wsmatchid"] = None
	                    try:
	                        qual_dict["wseventid"] = str(event["id"])
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
	                        qual_dict["qualvalue"] = 1
	                    qual_list.append(qual_dict)

	        qual_df = pd.DataFrame(qual_list)
	        qual_df = qual_df[["keyid","wsmatchid","wseventid","matcheventid","qualid","qualname","qualvalue"]] 
	        qual_df = qual_df.drop_duplicates(["keyid","qualname"])
	        qual_df.to_sql("qualifiers",conn,if_exists=status,index=False)
	        
	            
	        events_df = pd.DataFrame(event_list)
	        events_df = events_df[["keyid","wsmatchid","wseventid","matcheventid","minute","second","expandedminute","teamid",
	                               "playerid","period","typeid","type","outcometype","x","y"]]
	        events_df.to_sql("events",conn,if_exists=status,index=False)
	        
	        teams = ["home","away"]
	        team_list = []
	        players_list = []
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
	            team_list.append(teams_dict)
	        
	            players = range(0,len(match[team]["players"]))
	            for number in players:
	                players_dict = {
	                        "playerid":None,
	                        "playername":None,
	                                }
	                try:
	                    players_dict["playerid"] = match[team]["players"][number]["playerId"]
	                except KeyError:
	                    players_dict["playerid"] = None
	                try:
	                    players_dict["playername"] = match[team]["players"][number]["name"]
	                except KeyError:
	                    players_dict["playername"] = None
	                
	                players_list.append(players_dict)
	        
	        players_sql = pd.read_sql("SELECT * FROM players",conn)
	        players_df = pd.DataFrame(players_list)
	        players_df = players_df[["playerid","playername"]]
	        players_df = players_df.append([players_sql,players_sql]).drop_duplicates("playerid",keep=False)
	        players_df.to_sql("players",conn,if_exists=status,index=False)
	        
	        teams_sql = pd.read_sql("SELECT * FROM teams",conn)
	        teams_df = pd.DataFrame(team_list)
	        teams_df = teams_df[["teamid","teamname"]]
	        teams_df = teams_df.append([teams_sql,teams_sql]).drop_duplicates("teamid",keep=False)
	        teams_df.to_sql("teams",conn,if_exists=status,index=False)
	        
	        count = count + 1
	        
	        print(time.strftime("%Y-%m-%d %H:%M:%S"),count,"files done of",totalcount)
	print(time.strftime("%Y-%m-%d %H:%M:%S"),"finished",totalcount,"matches of",tournament,year)
	        