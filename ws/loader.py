from ws.constants import *
import json
import os
import pandas as pd
import numpy as np


class League():

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

    def matchesList(self, season=None):
        return self.matcheslists[self.season]

    def numberMatches(self):
        return pd.Series({k: len(v) for k, v in self.matcheslists.items()}, name="numberofmatches")

    def setSeason(self, season):

        self.season = season

        return self

    def importMatch(self, number):
        return Match(number, self.league, self.season, JSONPATH)


class Match():

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

        print("%s - %s Season" % (self.league, self.season))
        print("%s" % self.date)
        print("%s - %s" % (self.home,self.away))


class MatchLoader():

    def __init__(self,db,match):

        self.db = db

        if not isinstance(match, Match):
            raise(TypeError,"match must be of Match type")

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


        data = {
                "league": self.match.league,
                "season": self.match.season,
                "date": self.match.date,
                "homeName" : self.match.home,
                "homeId": self.match_data["home"]["teamId"],
                "homeManager": self.match_data["home"]["managerName"],
                "awayName" : self.match.away,
                "awayId": self.match_data["away"]["teamId"],
                "awayManager": self.match_data["away"]["managerName"],
                "referee": self.match_data["referee"]["name"],
                "venue": self.match_data["venueName"],
                }

        self.db["matches"].update_one({"wsMatchId":self.match.matchid},
                                      {'$setOnInsert': data}, upsert=True)

        return self

    def events(self):

        events = self.match_data["events"]

        if len(events) == self.db["events"].count({"wsMatchId":self.match.matchid}):
            return self

        else:
            for event in events:

                event["wsMatchId"] = self.match.matchid

                self.db["events"].update_one({"wsEventId": str(self.match.matchid)+str(event["id"])},
                                            {'$setOnInsert': event}, upsert=True)


        return self








