from ws.constants import *
import json
import os
import pandas as pd
import numpy as np


class JSONLeague():

    jsonpath = JSONPATH

    def __init__(self, league):
        self.league = league
        self.leaguename = self.league.lower().replace(" ", "_")
        self.leaguepath = self.jsonpath + self.leaguename + "/"
        self.seasons = list(filter(lambda x: "2" in x, os.listdir(self.leaguepath)))
        self.matcheslists = {
        s: list(map(lambda x: int(x.split(".")[0]), list(filter(lambda x: ".json" in x, os.listdir(self.leaguepath + s)))))
        for s in self.seasons}
        self.season = self.seasons[-1]

    def matchesList(self):
        return self.matcheslists[self.season]

    def numberMatches(self):
        return pd.Series({k: len(v) for k, v in self.matcheslists.items()}, name="numberofmatches")

    def setSeason(self, season):

        self.season = season

        return self

    def importMatch(self, number):
        return JSONMatch(number, self.league, self.season, JSONPATH)


class JSONMatch():

    def __init__(self, matchid, league, season, jsonpath=JSONPATH):
        self.league = league
        self.season = season
        self.leaguename = self.league.lower().replace(" ", "_")
        self.matchid = matchid
        self.jsonpath = jsonpath
        self.matchpath = jsonpath + self.leaguename + "/" + self.season + "/" + str(self.matchid) + ".json"
        self.match = json.load(open(self.matchpath, "r", encoding="utf-8"), encoding="utf-8")
        self.home = self.match["home"]["name"]
        self.away = self.match["away"]["name"]
        self.date = self.match["startTime"]

    def matchInfo(self):

       data = {"League":self.league,
               "Season":self.season,
               "Home":self.home,
               "Away":self.away,
               "Date":pd.to_datetime(self.date)}

       return pd.Series(data)


class MatchLoader():

    def __init__(self,db,match):

        self.db = db

        if not isinstance(match, JSONMatch):
            raise(TypeError,"match must be of JSONMatch type")

        self.match = match
        self.match_data = match.match
        self.collections = self.db.collection_names()

    def teams(self):

        self.db["teams"].update_one({'teamId': self.match_data['home']['teamId']},
                         {'$setOnInsert': {'teamName': self.match_data['home']['name']}}, upsert=True)
        self.db["teams"].update_one({'teamId': self.match_data['away']['teamId']},
                         {'$setOnInsert': {'teamName': self.match_data['away']['name']}}, upsert=True)

        return self

    def players(self):

        for k, v in self.match_data["playerIdNameDictionary"].items():

            self.db["players"].update_one({"playerId": int(k)},
                                     {'$setOnInsert': {'playerName': v}}, upsert=True)

        return self

    def matches(self):


        data = {}

        data["league"] = self.match.league
        data["season"] = self.match.season
        data["date"] = self.match.date
        data["homeName"] = self.match.home
        try:
            data["homeId"] = self.match_data["home"]["teamId"]
        except KeyError:
            data["homeId"] = None
        try:
            data["homeManager"] = self.match_data["home"]["managerName"]
        except KeyError:
            data["homeManager"] = None
        data["awayName"] = self.match.away
        try:
            data["awayId"] = self.match_data["away"]["teamId"]
        except KeyError:
            data["awayId"] = None
        try:
            data["awayManager"] =  self.match_data["away"]["managerName"]
        except KeyError:
            data["awayManager"] = None
        try:
            data["referee"] = self.match_data["referee"]["name"]
        except KeyError:
            data["referee"] = None
        try:
            data["venue"] = self.match_data["venueName"]
        except KeyError:
            data["venue"] = None


        self.db["matches"].update_one({"wsMatchId":self.match.matchid},
                                      {'$setOnInsert': data}, upsert=True)

        return self

    def events(self):

        events = self.match_data["events"]


        for event in events:

            event["wsMatchId"] = self.match.matchid
            event["wsEventId"] = str(self.match.matchid)+str(event["id"])

        self.db["events"].insert_many(events)

        return self







