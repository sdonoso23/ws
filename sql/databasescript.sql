drop table matches, referees, teams, players, qualifiers, events, satisfiedevents, formations;

CREATE TABLE teams
(dbteamid serial NOT NULL,
 teamid int PRIMARY KEY,
 teamname varchar
 );


CREATE TABLE matches
(
    dbmatchid serial,
    wsmatchid integer PRIMARY KEY,
    league character varying NOT NULL,
    season character varying NOT NULL,
    date timestamp NOT NULL,
    hometeamid integer NOT NULL,
    awayteamid integer NOT NULL,
    hometeamname character varying NOT NULL,
    awayteamname character varying NOT NULL,
    homescore integer NOT NULL,
    awayscore integer NOT NULL,
    homepkscore integer,
    awaypkscore integer,
    referee character varying,
    managerhome character varying,
    manageraway character varying,
    attendance integer,
    venuename character varying,
	FOREIGN KEY (hometeamid) references teams (teamid),
	FOREIGN KEY (awayteamid) references teams (teamid)		
);

CREATE TABLE players
(dbplayerid serial NOT NULL,
 playerid int NOT NULL PRIMARY KEY,
 playername varchar
 );
 

CREATE TABLE referees
(dbrefereeid serial NOT NULL,
 refereeid int PRIMARY KEY,
 refereename varchar
 );

 CREATE TABLE formations
 (formid SERIAL,
 uniqueformationid varchar PRIMARY KEY,
 wsmatchid int,
 teamid int,
 formationid int,
 formationname varchar,
 captainplayerid int,
 formperiod int,
 startminute int,
 endminute int,
 subonplayerid int,
 suboffplayerid int,
 player1 int,
 player2 int,
 player3 int,
 player4 int,
 player5 int,
 player6 int,
 player7 int,
 player8 int,
 player9 int,
 player10 int,
 player11 int,
 FOREIGN KEY (wsmatchid) references matches (wsmatchid),
 FOREIGN KEY (teamid) references teams (teamid),
 FOREIGN KEY (captainplayerid) references players (playerid),
 FOREIGN KEY (subonplayerid) references players (playerid),
 FOREIGN KEY (suboffplayerid) references players (playerid),
 FOREIGN KEY (player1) references players (playerid),
 FOREIGN KEY (player2) references players (playerid),
 FOREIGN KEY (player3) references players (playerid),
 FOREIGN KEY (player4) references players (playerid),
 FOREIGN KEY (player5) references players (playerid),
 FOREIGN KEY (player6) references players (playerid),
 FOREIGN KEY (player7) references players (playerid),
 FOREIGN KEY (player8) references players (playerid),
 FOREIGN KEY (player9) references players (playerid),
 FOREIGN KEY (player10) references players (playerid),
 FOREIGN KEY (player11) references players (playerid)
 );
 
 
CREATE table events
(dbeventid SERIAL,
 wsmatchid int,
 wseventid varchar,
 matcheventid int,
 minute int,
 second int,
 expandedminute int,
 teamid int,
 playerid int,
 period varchar,
 typeid int,
 type varchar,
 outcometype varchar,
 x numeric,
 y numeric,
 endx numeric,
 endy numeric,
 relatedeventid int,
 relatedplayerid int,
 blockedx numeric,
 blockedy numeric,
 goalmouthz numeric,
 goalmouthy numeric,
 cardtype varchar,
 shot boolean,
 touch boolean,
 goal boolean,
 angle numeric,
 captainplayerid int,
 formationslot int,
 foul int,
 involvedplayers varchar,
 jerseynumber varchar,
 length numeric,
 oppositerelatedevent int,
 passendx numeric,
 passendy numeric,
 playercaughtoffside int,
 playerposition varchar,
 teamformation varchar,
 teamplayerformation varchar,
 zone varchar,
 PRIMARY KEY (wsmatchid,wseventid),
 FOREIGN KEY (wsmatchid) references matches (wsmatchid),
 FOREIGN KEY (teamid) references teams (teamid),
 FOREIGN KEY (playerid) references players (playerid)
 );

CREATE table qualifiers
(dbqualid SERIAL NOT NULL,
wsmatchid int,
wseventid varchar,
matcheventid int,
qualid int,
qualname varchar,
qualvalue varchar,
PRIMARY KEY (dbqualid),
FOREIGN KEY (wsmatchid,wseventid) references events (wsmatchid,wseventid)
);

CREATE table satisfiedevents
(dbseventid SERIAL,
 wsmatchid int,
 wseventid varchar,
 matcheventid int,
 satisfiedeventid int,
 satisfiedeventname varchar,
 satisfiedeventvalue int,
PRIMARY KEY (dbseventid),
FOREIGN KEY (wsmatchid,wseventid) references events (wsmatchid,wseventid)
);

INSERT INTO players (playerid,playername)
Values
(145414,NULL),
(135055,NULL),
(0,NULL),
(9463,NULL),
(278876,NULL),
(294162,NULL),
(294042,NULL),
(294147,NULL),
(74495,NULL),
(288893,NULL),
(291969,NULL),
(294020,NULL),
(294023,NULL),
(6582,NULL),
(259887,NULL),
(136675,NULL),
(134863,NULL),
(134862,NULL),
(141769,NULL),
(280664,NULL);




COPY teams (teamid, teamname) 
FROM 'C:\tmp\teams.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY matches (wsmatchid,league,season,date,hometeamid,awayteamid,hometeamname,awayteamname,homescore,awayscore,homepkscore,awaypkscore,referee,managerhome,manageraway,attendance,venuename) 
FROM 'C:\tmp\matches.csv' DELIMITER ',' NULL 'NA' CSV HEADER;
 
COPY players (playerid, playername) 
FROM 'C:\tmp\players.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY referees (refereeid, refereename) 
FROM 'C:\tmp\referees.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY formations (uniqueformationid,wsmatchid,teamid,formationid,formationname,captainplayerid,formperiod,startminute,endminute,subonplayerid,suboffplayerid,player1,player2,player3,player4,player5,player6,player7,player8,player9,player10,player11)
FROM 'C:\tmp\formations.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY events (wsmatchid,wseventid,matcheventid,minute,second,expandedminute,teamid,playerid,period,typeid,type,outcometype,x,y,endx,endy,relatedeventid,relatedplayerid,blockedx,blockedy,goalmouthz,goalmouthy,cardtype,shot,touch,goal,angle,captainplayerid,formationslot,foul,involvedplayers,jerseynumber,length,oppositerelatedevent,passendx,passendy,playercaughtoffside,playerposition,teamformation,teamplayerformation,zone)
FROM 'C:\tmp\events2012-2013.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY events (wsmatchid,wseventid,matcheventid,minute,second,expandedminute,teamid,playerid,period,typeid,type,outcometype,x,y,endx,endy,relatedeventid,relatedplayerid,blockedx,blockedy,goalmouthz,goalmouthy,cardtype,shot,touch,goal,angle,captainplayerid,formationslot,foul,involvedplayers,jerseynumber,length,oppositerelatedevent,passendx,passendy,playercaughtoffside,playerposition,teamformation,teamplayerformation,zone)
FROM 'C:\tmp\events2013-2014.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY events (wsmatchid,wseventid,matcheventid,minute,second,expandedminute,teamid,playerid,period,typeid,type,outcometype,x,y,endx,endy,relatedeventid,relatedplayerid,blockedx,blockedy,goalmouthz,goalmouthy,cardtype,shot,touch,goal,angle,captainplayerid,formationslot,foul,involvedplayers,jerseynumber,length,oppositerelatedevent,passendx,passendy,playercaughtoffside,playerposition,teamformation,teamplayerformation,zone)
FROM 'C:\tmp\events2014-2015.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY events (wsmatchid,wseventid,matcheventid,minute,second,expandedminute,teamid,playerid,period,typeid,type,outcometype,x,y,endx,endy,relatedeventid,relatedplayerid,blockedx,blockedy,goalmouthz,goalmouthy,cardtype,shot,touch,goal,angle,captainplayerid,formationslot,foul,involvedplayers,jerseynumber,length,oppositerelatedevent,passendx,passendy,playercaughtoffside,playerposition,teamformation,teamplayerformation,zone)
FROM 'C:\tmp\events2015-2016.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY events (wsmatchid,wseventid,matcheventid,minute,second,expandedminute,teamid,playerid,period,typeid,type,outcometype,x,y,endx,endy,relatedeventid,relatedplayerid,blockedx,blockedy,goalmouthz,goalmouthy,cardtype,shot,touch,goal,angle,captainplayerid,formationslot,foul,involvedplayers,jerseynumber,length,oppositerelatedevent,passendx,passendy,playercaughtoffside,playerposition,teamformation,teamplayerformation,zone)
FROM 'C:\tmp\events2016-2017.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY qualifiers (wsmatchid,wseventid,matcheventid,qualid,qualname,qualvalue)
FROM 'C:\tmp\qualifiers2012-2013.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY qualifiers (wsmatchid,wseventid,matcheventid,qualid,qualname,qualvalue)
FROM 'C:\tmp\qualifiers2013-2014.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY qualifiers (wsmatchid,wseventid,matcheventid,qualid,qualname,qualvalue)
FROM 'C:\tmp\qualifiers2014-2015.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY qualifiers (wsmatchid,wseventid,matcheventid,qualid,qualname,qualvalue)
FROM 'C:\tmp\qualifiers2015-2016.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY qualifiers (wsmatchid,wseventid,matcheventid,qualid,qualname,qualvalue)
FROM 'C:\tmp\qualifiers2016-2017.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY satisfiedevents (wsmatchid,wseventid,matcheventid,satisfiedeventid,satisfiedeventname,satisfiedeventvalue)
FROM 'C:\tmp\sevents2012-2013.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY satisfiedevents (wsmatchid,wseventid,matcheventid,satisfiedeventid,satisfiedeventname,satisfiedeventvalue)
FROM 'C:\tmp\sevents2013-2014.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY satisfiedevents (wsmatchid,wseventid,matcheventid,satisfiedeventid,satisfiedeventname,satisfiedeventvalue)
FROM 'C:\tmp\sevents2014-2015.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY satisfiedevents (wsmatchid,wseventid,matcheventid,satisfiedeventid,satisfiedeventname,satisfiedeventvalue)
FROM 'C:\tmp\sevents2015-2016.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY satisfiedevents (wsmatchid,wseventid,matcheventid,satisfiedeventid,satisfiedeventname,satisfiedeventvalue)
FROM 'C:\tmp\sevents2016-2017.csv' DELIMITER ',' NULL 'NA' CSV HEADER;


CREATE INDEX events_player on events (playerid);
CREATE INDEX events_teams on events (teamid);
CREATE INDEX events_shots on events (shot);
CREATE INDEX qualifiers_events on qualifiers (wsmatchid,wseventid);
CREATE INDEX satisfiedevents_events on satisfiedevents (wsmatchid,wseventid);

COPY (SELECT DISTINCT playerid FROM events ORDER BY playerid) TO '/tmp/events.csv' DELIMITER ',' CSV HEADER;


