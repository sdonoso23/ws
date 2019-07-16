import pandas as pd
import numpy as np

from ws.constants import *


class BaseQuery():

    def __init__(self, db):
        self.db = db
        self.player_dict = {i["playerId"]: i["playerName"] for i in list(self.db["players"].find())}
        self.team_dict = {i["teamId"]: i["teamName"] for i in list(self.db["teams"].find())}
        self.matches_dict = {i["wsMatchId"]: i for i in list(self.db["matches"].find())}

    def query(self, collection, condition):
        return self.db[collection].find(condition)

    def getMatch(self,matchid):
        return Match(self, matchid)

    def getLeagueMatchesInfo(self, league, season):
        return pd.DataFrame(list(self.query("matches", {"$and": [{"league": league}, {"season": season}]})))

    def eventsDataFrame(self,condition, columns=["_id", "wsMatchId", "expandedMinute", "second", "teamId", "playerId", "type.displayName",
                   "outcomeType.displayName", "x", "y"]):

        events = []
        columns = columns

        for i in self.query("events",condition):

            row = {}
            for col in columns:
                if "." in col:
                    splt = col.split(".")
                    row[col] = i[splt[0]][splt[1]]
                else:
                    row[col] = i.get(col, None)

            row["teamName"] = self.team_dict.get(i["teamId"], None)
            row["playerName"] = self.player_dict.get(i.get("playerId", None), None)

            events.append(row)

        return pd.DataFrame(events)[columns + ["teamName", "playerName"]].set_index("_id")

    def getQualifiers(self,condition,columns=None):

        a = {}
        for i in self.query("events",condition):

            d = {q.get("type", None).get("displayName", None): q.get("value", 1) for q in i["qualifiers"]}

            a[i["_id"]] = d


        return pd.DataFrame(a).T if columns == None else pd.DataFrame(a).T[columns]

    def allShotsData(self):

        df_shots = self.eventsDataFrame({"isShot": True})

        y = (df_shots["type.displayName"] == "Goal").apply(int).sort_index()

        quals_shots = self.getQualifiers(condition={"_id": {"$in": df_shots.index.tolist()}})

        quals_shots = quals_shots[(quals_shots["Penalty"] != 1) | (quals_shots["OwnGoal"] != 1)]

        SHOT_QUALS = ["Assisted", "DirectFreekick", "RegularPlay",
                      "FromCorner", "RightFoot", "LeftFoot", "Head",
                      "SetPiece", "ThrowinSetPiece", "OtherBodyPart"]

        dataset = df_shots[["x", "y"]].merge(quals_shots[SHOT_QUALS], right_index=True, left_index=True).fillna(
            0).sort_index()


        return dataset, y.loc[dataset.index]




class Match():

    def __init__(self, bq, matchid):


        self.bq = bq
        self.matchid = matchid
        self.info = pd.Series(self.bq.matches_dict[self.matchid])
        self.cursor = self.bq.query("events", {"wsMatchId": self.matchid})

    def calculateMinutes(self):

        maxMinute = np.max([i["expandedMinute"] for i in self.cursor.clone()])

        starters = []
        subs = {}
        for i in self.cursor.clone():

            try:
                if (i["type"]["displayName"] == "FormationSet"):

                    for q in i["qualifiers"]:
                        if q["type"]["displayName"] == "InvolvedPlayers":
                            starters.extend(list(map(int, q["value"].split(",")))[0:11])
                elif (i["type"]["displayName"] == "SubstitutionOn"):
                    subs[i["playerId"]] = maxMinute - i["expandedMinute"]
                    subs[i["relatedPlayerId"]] = i["expandedMinute"]

                else:
                    continue
            except:
                print("error")
                continue

        players = {k: maxMinute for k in starters}
        players.update(subs)

        players = {k: {"playerName": self.bq.player_dict[k],
                       "minutes": v} for k, v in players.items()}

        return pd.DataFrame(players).T[["playerName", "minutes"]]


    def events(self):

        return self.bq.eventsDataFrame({"wsMatchId":self.matchid})

    def qualifiers(self):

       return self.bq.getQualifiers({"wsMatchId":self.matchid})

    def shots(self):

        df = self.events()

        shots_types = ["ShotOnPost", "SavedShot", "MissedShots", "Goal"]

        df_shots = df[list(map(lambda x: x in shots_types, df["type.displayName"]))]

        y = (df_shots["type.displayName"] == "Goal").apply(int).sort_index()

        quals_shots = self.bq.getQualifiers(condition={"_id": {"$in": df_shots.index.tolist()}})

        if "Penalty" in quals_shots.columns:

            quals_shots = quals_shots[(quals_shots["Penalty"] != 1)]

        if "OwnGoal" in quals_shots.columns:

            quals_shots = quals_shots[quals_shots["OwnGoal"] != 1]

        SHOT_QUALS = ["Assisted", "DirectFreekick", "RegularPlay",
                      "FromCorner", "RightFoot", "LeftFoot", "Head",
                      "SetPiece", "ThrowinSetPiece", "OtherBodyPart"]

        inter = quals_shots.columns.intersection(SHOT_QUALS)

        dif = set(SHOT_QUALS).difference(quals_shots.columns)

        dataset = df_shots[["x", "y"]].merge(quals_shots[inter], right_index=True, left_index=True).fillna(
            0).sort_index()

        dataset = pd.concat([dataset, pd.DataFrame(0, index=dataset.index, columns=dif)], axis=1)[["x", "y"] + SHOT_QUALS]

        return dataset, y.loc[dataset.index]


