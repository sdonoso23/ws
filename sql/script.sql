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
 PRIMARY KEY (wsmatchid,wseventid),
 FOREIGN KEY (wsmatchid) references matches (wsmatchid),
 FOREIGN KEY (teamid) references teams (teamid),
 FOREIGN KEY (playerid) references players (playerid)
 );

CREATE table qualifiers
(dbqualid SERIAL NOT NULL,
 wsmatchid int,
wseventid varchar,
aerialfoul int,
angle numeric,
assisted int,
bigchance int,
bigchancecreated int,
blocked int,
blockedcross int,
blockedx numeric,
blockedy numeric,
boxcentre int,
boxleft int,
boxright int,
captainplayerid int,
chipped int,
collected int,
cornertaken int,
crosss int,
deepboxleft int,
deepboxright int,
defensive int,
directfreekick int,
divingsave int,
fastbreak int,
feet int,
formationslot int,
foul int,
freekicktaken int,
fromcorner int,
fromshotofftarget int,
goaldisallowed int,
goalkick int,
goalmouthy numeric,
goalmouthz numeric,
hands int,
head int,
headpass int,
highcentre int,
highclaim int,
highleft int,
highright int,
indirectfreekicktaken int,
intentionalassist int,
intentionalgoalassist int,
involvedplayers varchar,
jerseynumber varchar,
keepermissed int,
keepersaved int,
keepersaveinsixyard int,
keepersaveinthebox int,
keepersaveobox int,
keeperthrow int,
keeperwentwide int,
keypass int,
lastman int,
layoff int,
leadingtoattempt int,
leadingtogoal int,
leftfoot int,
length numeric,
longball int,
lowcentre int,
lowleft int,
lowright int,
misshigh int,
missleft int,
missright int,
obstruction int,
offensive int,
oppositerelatedevent int,
otherbodypart int,
outfielderblock int,
outofboxcentre int,
outofboxdeepleft int,
outofboxdeepright int,
outofboxleft int,
outofboxright int,
overrun int,
owngoal int,
parrieddanger int,
parriedsafe int,
passendx numeric,
passendy numeric,
penalty int,
playercaughtoffside int,
playerposition varchar,
red int,
regularplay int,
relatedeventid int,
rightfoot int,
savedoffline int,
secondyellow int,
setpiece int,
shotassist int,
sixyardblock int,
smallboxcentre int,
smallboxleft int,
smallboxright int,
standingsave int,
teamformation int,
teamplayerformation varchar,
thirtyfivepluscentre int,
thirtyfiveplusleft int,
thirtyfiveplusright int,
throughball int,
throwin int,
throwinsetpiece int,
voidyellowcard int,
yellow int,
zone varchar,
PRIMARY KEY (dbqualid),
FOREIGN KEY (wsmatchid,wseventid) references events (wsmatchid,wseventid)
);

CREATE table satisfiedevents
(dbseventid SERIAL,
 wsmatchid int,
 wseventid varchar,
assist int,
assistcorner int,
assistcross int,
assistfreekick int,
assistother int,
assistthroughball int,
assistthrowin int,
ballrecovery int,
bigchancecreated int,
bigchancemissed int,
bigchancescored int,
challengelost int,
clearanceeffective int,
clearancehead int,
clearanceofftheline int,
clearancetotal int,
closemisshigh int,
closemisshighleft int,
closemisshighright int,
closemissleft int,
closemissright int,
collected int,
cornerawarded int,
defensiveduel int,
defensivethird int,
dispossessed int,
dribblelost int,
dribblewon int,
duelaeriallost int,
duelaerialwon int,
errorleadstogoal int,
errorleadstoshot int,
finalthird int,
foulcommitted int,
foulgiven int,
goalcounter int,
goalhead int,
goalleftfoot int,
goalnormal int,
goalobox int,
goalobp int,
goalopenplay int,
goalown int,
goalpenaltyarea int,
goalrightfoot int,
goalsetpiece int,
goalsixyardbox int,
intentionalassist int,
interceptionall int,
interceptioninthebox int,
interceptionwon int,
keeperclaimhighlost int,
keeperclaimhighwon int,
keeperclaimlost int,
keeperclaimwon int,
keeperdivingsave int,
keepermissed int,
keeperpenaltysaved int,
keepersaveinthebox int,
keepersavetotal int,
keepersmother int,
keepersweeperlost int,
keypasscorner int,
keypasscross int,
keypassfreekick int,
keypasslong int,
keypassother int,
keypassshort int,
keypassthroughball int,
keypassthrowin int,
midthird int,
offensiveduel int,
offsidegiven int,
offsideprovoked int,
outfielderblock int,
outfielderblockedpass int,
overrun int,
parrieddanger int,
parriedsafe int,
passaccurate int,
passback int,
passbackzoneinaccurate int,
passchipped int,
passcorner int,
passcorneraccurate int,
passcornerinaccurate int,
passcrossaccurate int,
passcrossblockeddefensive int,
passcrossinaccurate int,
passforward int,
passforwardzoneaccurate int,
passfreekick int,
passfreekickaccurate int,
passfreekickinaccurate int,
passhead int,
passinaccurate int,
passkey int,
passleft int,
passlongballaccurate int,
passlongballinaccurate int,
passright int,
passthroughballaccurate int,
passthroughballinaccurate int,
passthroughballinacurate int,
penaltyconceded int,
penaltymissed int,
penaltyscored int,
penaltywon int,
pos int,
punches int,
redcard int,
savefeet int,
savehands int,
saveobox int,
saveobp int,
savepenaltyarea int,
savesixyardbox int,
secondyellow int,
shortpassaccurate int,
shortpassinaccurate int,
shotblocked int,
shotcounter int,
shothead int,
shotleftfoot int,
shotoboxtotal int,
shotobp int,
shotofftarget int,
shotofftargetinsidebox int,
shotonpost int,
shotontarget int,
shotopenplay int,
shotpenaltyarea int,
shotrightfoot int,
shotsetpiece int,
shotsixyardbox int,
shotstotal int,
sixyardblock int,
standingsave int,
suboff int,
subon int,
successfulfinalthirdpasses int,
tacklelastman int,
tacklelost int,
tacklewon int,
throwin int,
touches int,
turnover int,
voidyellowcard int,
yellowcard int,
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

COPY events (wsmatchid,wseventid,matcheventid,minute,second,expandedminute,teamid,playerid,period,typeid,type,outcometype,x,y,endx,endy,relatedeventid,relatedplayerid,blockedx,blockedy,goalmouthz,goalmouthy,cardtype,shot,touch,goal)
FROM 'C:\tmp\events2012-2013.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY events (wsmatchid,wseventid,matcheventid,minute,second,expandedminute,teamid,playerid,period,typeid,type,outcometype,x,y,endx,endy,relatedeventid,relatedplayerid,blockedx,blockedy,goalmouthz,goalmouthy,cardtype,shot,touch,goal)
FROM 'C:\tmp\events2013-2014.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY events (wsmatchid,wseventid,matcheventid,minute,second,expandedminute,teamid,playerid,period,typeid,type,outcometype,x,y,endx,endy,relatedeventid,relatedplayerid,blockedx,blockedy,goalmouthz,goalmouthy,cardtype,shot,touch,goal)
FROM 'C:\tmp\events2014-2015.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY events (wsmatchid,wseventid,matcheventid,minute,second,expandedminute,teamid,playerid,period,typeid,type,outcometype,x,y,endx,endy,relatedeventid,relatedplayerid,blockedx,blockedy,goalmouthz,goalmouthy,cardtype,shot,touch,goal)
FROM 'C:\tmp\events2015-2016.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY events (wsmatchid,wseventid,matcheventid,minute,second,expandedminute,teamid,playerid,period,typeid,type,outcometype,x,y,endx,endy,relatedeventid,relatedplayerid,blockedx,blockedy,goalmouthz,goalmouthy,cardtype,shot,touch,goal)
FROM 'C:\tmp\events2016-2017.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY qualifiers (wsmatchid,wseventid,angle,assisted,bigchance,bigchancecreated,blocked,blockedcross,blockedx,blockedy,boxcentre,boxleft,boxright,captainplayerid,chipped,collected,cornertaken,crosss,deepboxleft,deepboxright,defensive,directfreekick,divingsave,fastbreak,feet,formationslot,foul,freekicktaken,fromcorner,fromshotofftarget,goaldisallowed,goalkick,goalmouthy,goalmouthz,hands,head,headpass,highcentre,highclaim,highleft,highright,indirectfreekicktaken,intentionalassist,intentionalgoalassist,involvedplayers,jerseynumber,keepermissed,keepersaved,keepersaveinsixyard,keepersaveinthebox,keepersaveobox,keeperthrow,keeperwentwide,keypass,lastman,layoff,leadingtoattempt,leadingtogoal,leftfoot,length,longball,lowcentre,lowleft,lowright,misshigh,missleft,missright,offensive,oppositerelatedevent,otherbodypart,outfielderblock,outofboxcentre,outofboxdeepleft,outofboxdeepright,outofboxleft,outofboxright,overrun,owngoal,parrieddanger,parriedsafe,passendx,passendy,penalty,playercaughtoffside,playerposition,red,regularplay,relatedeventid,rightfoot,savedoffline,secondyellow,setpiece,shotassist,sixyardblock,smallboxcentre,smallboxleft,smallboxright,standingsave,teamformation,teamplayerformation,thirtyfivepluscentre,thirtyfiveplusleft,thirtyfiveplusright,throughball,throwin,throwinsetpiece,voidyellowcard,yellow,zone)
FROM 'C:\tmp\qualifiers2012-2013.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY qualifiers (wsmatchid,wseventid,aerialfoul,angle,assisted,bigchance,bigchancecreated,blocked,blockedcross,blockedx,blockedy,boxcentre,boxleft,boxright,captainplayerid,chipped,collected,cornertaken,crosss,deepboxleft,deepboxright,defensive,directfreekick,divingsave,fastbreak,feet,formationslot,foul,freekicktaken,fromcorner,fromshotofftarget,goaldisallowed,goalkick,goalmouthy,goalmouthz,head,headpass,highcentre,highclaim,highleft,highright,indirectfreekicktaken,intentionalassist,intentionalgoalassist,involvedplayers,jerseynumber,keepermissed,keepersaved,keepersaveinsixyard,keepersaveinthebox,keepersaveobox,keeperthrow,keeperwentwide,keypass,lastman,layoff,leadingtoattempt,leadingtogoal,leftfoot,length,longball,lowcentre,lowleft,lowright,misshigh,missleft,missright,obstruction,offensive,oppositerelatedevent,otherbodypart,outfielderblock,outofboxcentre,outofboxdeepleft,outofboxdeepright,outofboxleft,outofboxright,overrun,owngoal,parrieddanger,parriedsafe,passendx,passendy,penalty,playercaughtoffside,playerposition,red,regularplay,relatedeventid,rightfoot,savedoffline,secondyellow,setpiece,shotassist,sixyardblock,smallboxcentre,smallboxleft,smallboxright,standingsave,teamformation,teamplayerformation,thirtyfivepluscentre,thirtyfiveplusleft,thirtyfiveplusright,throughball,throwin,throwinsetpiece,voidyellowcard,yellow,zone,hands)
FROM 'C:\tmp\qualifiers2013-2014.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY qualifiers (wsmatchid,wseventid,aerialfoul,angle,assisted,bigchance,bigchancecreated,blocked,blockedcross,blockedx,blockedy,boxcentre,boxleft,boxright,captainplayerid,chipped,collected,cornertaken,crosss,deepboxleft,deepboxright,defensive,directfreekick,divingsave,fastbreak,feet,formationslot,foul,freekicktaken,fromcorner,fromshotofftarget,goaldisallowed,goalkick,goalmouthy,goalmouthz,hands,head,headpass,highcentre,highclaim,highleft,highright,indirectfreekicktaken,intentionalassist,intentionalgoalassist,involvedplayers,jerseynumber,keepermissed,keepersaved,keepersaveinsixyard,keepersaveinthebox,keepersaveobox,keeperthrow,keeperwentwide,keypass,lastman,layoff,leadingtoattempt,leadingtogoal,leftfoot,length,longball,lowcentre,lowleft,lowright,misshigh,missleft,missright,obstruction,offensive,oppositerelatedevent,otherbodypart,outfielderblock,outofboxcentre,outofboxdeepleft,outofboxdeepright,outofboxleft,outofboxright,overrun,owngoal,parrieddanger,parriedsafe,passendx,passendy,penalty,playercaughtoffside,playerposition,red,regularplay,relatedeventid,rightfoot,savedoffline,secondyellow,setpiece,shotassist,sixyardblock,smallboxcentre,smallboxleft,smallboxright,standingsave,teamformation,teamplayerformation,thirtyfivepluscentre,thirtyfiveplusleft,thirtyfiveplusright,throughball,throwin,throwinsetpiece,voidyellowcard,yellow,zone)
FROM 'C:\tmp\qualifiers2014-2015.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY qualifiers (wsmatchid,wseventid,aerialfoul,angle,assisted,bigchance,bigchancecreated,blocked,blockedcross,blockedx,blockedy,boxcentre,boxleft,boxright,captainplayerid,chipped,collected,cornertaken,crosss,deepboxleft,deepboxright,defensive,directfreekick,divingsave,fastbreak,feet,formationslot,foul,freekicktaken,fromcorner,fromshotofftarget,goaldisallowed,goalkick,goalmouthy,goalmouthz,hands,head,headpass,highcentre,highclaim,highleft,highright,indirectfreekicktaken,intentionalassist,intentionalgoalassist,involvedplayers,jerseynumber,keepermissed,keepersaved,keepersaveinsixyard,keepersaveinthebox,keepersaveobox,keeperthrow,keeperwentwide,keypass,lastman,layoff,leadingtoattempt,leadingtogoal,leftfoot,length,longball,lowcentre,lowleft,lowright,misshigh,missleft,missright,obstruction,offensive,oppositerelatedevent,otherbodypart,outfielderblock,outofboxcentre,outofboxdeepleft,outofboxdeepright,outofboxleft,outofboxright,overrun,owngoal,parrieddanger,parriedsafe,passendx,passendy,penalty,playercaughtoffside,playerposition,red,regularplay,relatedeventid,rightfoot,savedoffline,secondyellow,setpiece,shotassist,sixyardblock,smallboxcentre,smallboxleft,smallboxright,standingsave,teamformation,teamplayerformation,thirtyfivepluscentre,thirtyfiveplusleft,thirtyfiveplusright,throughball,throwin,throwinsetpiece,voidyellowcard,yellow,zone)
FROM 'C:\tmp\qualifiers2015-2016.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY qualifiers (wsmatchid,wseventid,aerialfoul,angle,assisted,bigchance,bigchancecreated,blocked,blockedcross,blockedx,blockedy,boxcentre,boxleft,boxright,captainplayerid,chipped,collected,cornertaken,crosss,deepboxleft,deepboxright,defensive,directfreekick,divingsave,fastbreak,feet,formationslot,foul,freekicktaken,fromcorner,fromshotofftarget,goaldisallowed,goalkick,goalmouthy,goalmouthz,hands,head,headpass,highcentre,highclaim,highleft,highright,indirectfreekicktaken,intentionalassist,intentionalgoalassist,involvedplayers,jerseynumber,keepermissed,keepersaved,keepersaveinsixyard,keepersaveinthebox,keepersaveobox,keeperthrow,keeperwentwide,keypass,lastman,layoff,leadingtoattempt,leadingtogoal,leftfoot,length,longball,lowcentre,lowleft,lowright,misshigh,missleft,missright,obstruction,offensive,oppositerelatedevent,otherbodypart,outfielderblock,outofboxcentre,outofboxdeepleft,outofboxdeepright,outofboxleft,outofboxright,overrun,owngoal,parrieddanger,parriedsafe,passendx,passendy,penalty,playercaughtoffside,playerposition,red,regularplay,relatedeventid,rightfoot,savedoffline,secondyellow,setpiece,shotassist,sixyardblock,smallboxcentre,smallboxleft,smallboxright,standingsave,teamformation,teamplayerformation,thirtyfivepluscentre,thirtyfiveplusleft,thirtyfiveplusright,throughball,throwin,throwinsetpiece,voidyellowcard,yellow,zone)
FROM 'C:\tmp\qualifiers2016-2017.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY satisfiedevents (wsmatchid,wseventid,assist,assistcorner,assistcross,assistfreekick,assistother,assistthroughball,assistthrowin,ballrecovery,bigchancecreated,bigchancemissed,bigchancescored,challengelost,clearanceeffective,clearancehead,clearanceofftheline,clearancetotal,closemisshigh,closemisshighleft,closemisshighright,closemissleft,closemissright,collected,cornerawarded,defensiveduel,defensivethird,dispossessed,dribblelost,dribblewon,duelaeriallost,duelaerialwon,errorleadstogoal,errorleadstoshot,finalthird,foulcommitted,foulgiven,goalcounter,goalhead,goalleftfoot,goalnormal,goalobox,goalobp,goalopenplay,goalown,goalpenaltyarea,goalrightfoot,goalsetpiece,goalsixyardbox,intentionalassist,interceptionall,interceptioninthebox,interceptionwon,keeperclaimhighwon,keeperdivingsave,keepermissed,keeperpenaltysaved,keepersaveinthebox,keepersavetotal,keepersmother,keepersweeperlost,keypasscorner,keypasscross,keypassfreekick,keypasslong,keypassother,keypassshort,keypassthroughball,keypassthrowin,midthird,offensiveduel,offsidegiven,offsideprovoked,outfielderblock,overrun,parrieddanger,parriedsafe,passaccurate,passback,passbackzoneinaccurate,passchipped,passcorner,passcorneraccurate,passcornerinaccurate,passcrossaccurate,passcrossblockeddefensive,passcrossinaccurate,passforward,passforwardzoneaccurate,passfreekick,passfreekickaccurate,passfreekickinaccurate,passhead,passinaccurate,passkey,passleft,passlongballaccurate,passlongballinaccurate,passright,passthroughballaccurate,passthroughballinaccurate,penaltyconceded,penaltymissed,penaltyscored,penaltywon,pos,punches,redcard,savefeet,savehands,saveobox,saveobp,savepenaltyarea,savesixyardbox,secondyellow,shortpassaccurate,shortpassinaccurate,shotblocked,shotcounter,shothead,shotleftfoot,shotoboxtotal,shotobp,shotofftarget,shotofftargetinsidebox,shotonpost,shotontarget,shotopenplay,shotpenaltyarea,shotrightfoot,shotsetpiece,shotsixyardbox,shotstotal,sixyardblock,standingsave,suboff,subon,successfulfinalthirdpasses,tacklelastman,tacklelost,tacklewon,throwin,touches,turnover,voidyellowcard,yellowcard,keeperclaimhighlost,keeperclaimlost,keeperclaimwon,passthroughballinacurate)
FROM 'C:\tmp\sevents2012-2013.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY satisfiedevents (wsmatchid,wseventid,assist,assistcorner,assistcross,assistfreekick,assistother,assistthroughball,ballrecovery,bigchancecreated,bigchancemissed,bigchancescored,challengelost,clearanceeffective,clearancehead,clearanceofftheline,clearancetotal,closemisshigh,closemisshighleft,closemisshighright,closemissleft,closemissright,collected,cornerawarded,defensiveduel,defensivethird,dispossessed,dribblelost,dribblewon,duelaeriallost,duelaerialwon,errorleadstogoal,errorleadstoshot,finalthird,foulcommitted,foulgiven,goalcounter,goalhead,goalleftfoot,goalnormal,goalobox,goalobp,goalopenplay,goalown,goalpenaltyarea,goalrightfoot,goalsetpiece,goalsixyardbox,intentionalassist,interceptionall,interceptioninthebox,interceptionwon,keeperclaimhighwon,keeperdivingsave,keepermissed,keeperpenaltysaved,keepersaveinthebox,keepersavetotal,keepersmother,keepersweeperlost,keypasscorner,keypasscross,keypassfreekick,keypasslong,keypassother,keypassshort,keypassthroughball,keypassthrowin,midthird,offensiveduel,offsidegiven,offsideprovoked,outfielderblock,outfielderblockedpass,overrun,parrieddanger,parriedsafe,passaccurate,passback,passbackzoneinaccurate,passchipped,passcorner,passcorneraccurate,passcornerinaccurate,passcrossaccurate,passcrossblockeddefensive,passcrossinaccurate,passforward,passforwardzoneaccurate,passfreekick,passfreekickaccurate,passfreekickinaccurate,passhead,passinaccurate,passkey,passleft,passlongballaccurate,passlongballinaccurate,passright,passthroughballaccurate,passthroughballinaccurate,penaltyconceded,penaltymissed,penaltyscored,penaltywon,pos,punches,redcard,savefeet,saveobox,saveobp,savepenaltyarea,savesixyardbox,secondyellow,shortpassaccurate,shortpassinaccurate,shotblocked,shotcounter,shothead,shotleftfoot,shotoboxtotal,shotobp,shotofftarget,shotofftargetinsidebox,shotonpost,shotontarget,shotopenplay,shotpenaltyarea,shotrightfoot,shotsetpiece,shotsixyardbox,shotstotal,sixyardblock,standingsave,suboff,subon,successfulfinalthirdpasses,tacklelastman,tacklelost,tacklewon,throwin,touches,turnover,voidyellowcard,yellowcard,assistthrowin,keeperclaimhighlost,keeperclaimlost,keeperclaimwon,passthroughballinacurate,savehands)
FROM 'C:\tmp\sevents2013-2014.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY satisfiedevents (wsmatchid,wseventid,assist,assistcorner,assistcross,assistfreekick,assistother,assistthroughball,assistthrowin,ballrecovery,bigchancecreated,bigchancemissed,bigchancescored,challengelost,clearanceeffective,clearancehead,clearanceofftheline,clearancetotal,closemisshigh,closemisshighleft,closemisshighright,closemissleft,closemissright,collected,cornerawarded,defensiveduel,defensivethird,dispossessed,dribblelost,dribblewon,duelaeriallost,duelaerialwon,errorleadstogoal,errorleadstoshot,finalthird,foulcommitted,foulgiven,goalcounter,goalhead,goalleftfoot,goalnormal,goalobox,goalobp,goalopenplay,goalown,goalpenaltyarea,goalrightfoot,goalsetpiece,goalsixyardbox,intentionalassist,interceptionall,interceptioninthebox,interceptionwon,keeperclaimhighwon,keeperdivingsave,keepermissed,keeperpenaltysaved,keepersaveinthebox,keepersavetotal,keepersmother,keepersweeperlost,keypasscorner,keypasscross,keypassfreekick,keypasslong,keypassother,keypassshort,keypassthroughball,keypassthrowin,midthird,offensiveduel,offsidegiven,offsideprovoked,outfielderblock,outfielderblockedpass,overrun,parrieddanger,parriedsafe,passaccurate,passback,passbackzoneinaccurate,passchipped,passcorner,passcorneraccurate,passcornerinaccurate,passcrossaccurate,passcrossblockeddefensive,passcrossinaccurate,passforward,passforwardzoneaccurate,passfreekick,passfreekickaccurate,passfreekickinaccurate,passhead,passinaccurate,passkey,passleft,passlongballaccurate,passlongballinaccurate,passright,passthroughballaccurate,passthroughballinaccurate,penaltyconceded,penaltymissed,penaltyscored,penaltywon,pos,punches,redcard,savefeet,savehands,saveobox,saveobp,savepenaltyarea,savesixyardbox,secondyellow,shortpassaccurate,shortpassinaccurate,shotblocked,shotcounter,shothead,shotleftfoot,shotoboxtotal,shotobp,shotofftarget,shotofftargetinsidebox,shotonpost,shotontarget,shotopenplay,shotpenaltyarea,shotrightfoot,shotsetpiece,shotsixyardbox,shotstotal,sixyardblock,standingsave,suboff,subon,successfulfinalthirdpasses,tacklelastman,tacklelost,tacklewon,throwin,touches,turnover,voidyellowcard,yellowcard)
FROM 'C:\tmp\sevents2014-2015.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY satisfiedevents (wsmatchid,wseventid,assist,assistcorner,assistcross,assistfreekick,assistother,assistthroughball,assistthrowin,ballrecovery,bigchancecreated,bigchancemissed,bigchancescored,challengelost,clearanceeffective,clearancehead,clearanceofftheline,clearancetotal,closemisshigh,closemisshighleft,closemisshighright,closemissleft,closemissright,collected,cornerawarded,defensiveduel,defensivethird,dispossessed,dribblelost,dribblewon,duelaeriallost,duelaerialwon,errorleadstogoal,errorleadstoshot,finalthird,foulcommitted,foulgiven,goalcounter,goalhead,goalleftfoot,goalnormal,goalobox,goalobp,goalopenplay,goalown,goalpenaltyarea,goalrightfoot,goalsetpiece,goalsixyardbox,intentionalassist,interceptionall,interceptioninthebox,interceptionwon,keeperclaimhighwon,keeperdivingsave,keepermissed,keeperpenaltysaved,keepersaveinthebox,keepersavetotal,keepersmother,keepersweeperlost,keypasscorner,keypasscross,keypassfreekick,keypasslong,keypassother,keypassshort,keypassthroughball,keypassthrowin,midthird,offensiveduel,offsidegiven,offsideprovoked,outfielderblock,outfielderblockedpass,overrun,parrieddanger,parriedsafe,passaccurate,passback,passbackzoneinaccurate,passchipped,passcorner,passcorneraccurate,passcornerinaccurate,passcrossaccurate,passcrossblockeddefensive,passcrossinaccurate,passforward,passforwardzoneaccurate,passfreekick,passfreekickaccurate,passfreekickinaccurate,passhead,passinaccurate,passkey,passleft,passlongballaccurate,passlongballinaccurate,passright,passthroughballaccurate,passthroughballinaccurate,penaltyconceded,penaltymissed,penaltyscored,penaltywon,pos,punches,redcard,savefeet,savehands,saveobox,saveobp,savepenaltyarea,savesixyardbox,secondyellow,shortpassaccurate,shortpassinaccurate,shotblocked,shotcounter,shothead,shotleftfoot,shotoboxtotal,shotobp,shotofftarget,shotofftargetinsidebox,shotonpost,shotontarget,shotopenplay,shotpenaltyarea,shotrightfoot,shotsetpiece,shotsixyardbox,shotstotal,sixyardblock,standingsave,suboff,subon,successfulfinalthirdpasses,tacklelastman,tacklelost,tacklewon,throwin,touches,turnover,voidyellowcard,yellowcard)
FROM 'C:\tmp\sevents2015-2016.csv' DELIMITER ',' NULL 'NA' CSV HEADER;

COPY satisfiedevents(wsmatchid,wseventid,assist,assistcorner,assistcross,assistfreekick,assistother,assistthroughball,assistthrowin,ballrecovery,bigchancecreated,bigchancemissed,bigchancescored,challengelost,clearanceeffective,clearancehead,clearanceofftheline,clearancetotal,closemisshigh,closemisshighleft,closemisshighright,closemissleft,closemissright,collected,cornerawarded,defensiveduel,defensivethird,dispossessed,dribblelost,dribblewon,duelaeriallost,duelaerialwon,errorleadstogoal,errorleadstoshot,finalthird,foulcommitted,foulgiven,goalcounter,goalhead,goalleftfoot,goalnormal,goalobox,goalobp,goalopenplay,goalown,goalpenaltyarea,goalrightfoot,goalsetpiece,goalsixyardbox,intentionalassist,interceptionall,interceptioninthebox,interceptionwon,keeperclaimhighwon,keeperdivingsave,keepermissed,keeperpenaltysaved,keepersaveinthebox,keepersavetotal,keepersmother,keepersweeperlost,keypasscorner,keypasscross,keypassfreekick,keypasslong,keypassother,keypassshort,keypassthroughball,keypassthrowin,midthird,offensiveduel,offsidegiven,offsideprovoked,outfielderblock,outfielderblockedpass,overrun,parrieddanger,parriedsafe,passaccurate,passback,passbackzoneinaccurate,passchipped,passcorner,passcorneraccurate,passcornerinaccurate,passcrossaccurate,passcrossblockeddefensive,passcrossinaccurate,passforward,passforwardzoneaccurate,passfreekick,passfreekickaccurate,passfreekickinaccurate,passhead,passinaccurate,passkey,passleft,passlongballaccurate,passlongballinaccurate,passright,passthroughballaccurate,passthroughballinaccurate,penaltyconceded,penaltymissed,penaltyscored,penaltywon,pos,punches,redcard,savefeet,savehands,saveobox,saveobp,savepenaltyarea,savesixyardbox,secondyellow,shortpassaccurate,shortpassinaccurate,shotblocked,shotcounter,shothead,shotleftfoot,shotoboxtotal,shotobp,shotofftarget,shotofftargetinsidebox,shotonpost,shotontarget,shotopenplay,shotpenaltyarea,shotrightfoot,shotsetpiece,shotsixyardbox,shotstotal,sixyardblock,standingsave,suboff,subon,successfulfinalthirdpasses,tacklelastman,tacklelost,tacklewon,throwin,touches,turnover,voidyellowcard,yellowcard)
FROM 'C:\tmp\sevents2016-2017.csv' DELIMITER ',' NULL 'NA' CSV HEADER;


COPY (SELECT DISTINCT playerid FROM events ORDER BY playerid) TO '/tmp/events.csv' DELIMITER ',' CSV HEADER;

drop index player_events
drop index team_events
drop index key_sevents

