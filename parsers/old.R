library(tidyverse)
library(ggplot2)
library(data.table)

####OLD FUNCTIONS####

csvlist<-function(league,year,tables){
    lista<-list()
    for (i in 1:length(tables)){
        lista[[i]]<-read_csv(paste("../CSV/",league,"/",year,"/",tables[i],".csv",sep=""))
    }
    names(lista)<-tables
    return(lista)
}

yearcsvlist<-function(leagues,year){
    datalist<-list()
    for (i in 1:length(leagues)){
        datalist[[i]]<-csvlist(leagues[i],year)
    }
    names(datalist)<-leagues
    return(datalist)
}


eventsdf<-function(dataframes){
    qualifiers<-dataframes$qualifiers %>%
        select(wseventid,qualname,qualvalue) %>%
        distinct(wseventid,qualname,.keep_all=TRUE) %>%
        spread(qualname,qualvalue)
    
    satisfiedevents<-dataframes$satisfiedevents %>%
        select(wseventid,satisfiedeventname,satisfiedeventvalue) %>%
        distinct(wseventid,satisfiedeventname,.keep_all=TRUE) %>%
        spread(satisfiedeventname,satisfiedeventvalue)
    
    eventscomplete<-dataframes$events %>%
        left_join(dataframes$playerslist,by=c("playerid")) %>%
        left_join(dataframes$playerslist,by=c("relatedplayerid"="playerid")) %>%
        rename(playername=playername.x) %>%
        rename(relatedplayername=playername.y) %>%
        left_join(dataframes$teams,by=c("teamid")) %>%
        left_join(qualifiers,by=c("wseventid")) %>%
        left_join(satisfiedevents,by=c("wseventid")) %>%
        select(-starts_with("id"))
    
    return(eventscomplete)
}


multieventsdf<-function(leaguesdf){
    eventslist<-list()
    for (i in 1:length(leaguesdf)){
        eventslist[[i]]<-eventsdf(leaguesdf[[i]])
    }
    return(eventslist)
}

savequalifiers<-function(leagues,years){
    aux<-function(leagues,years){
        lista<-list()
        for (i in 1:length(leagues)){
            lista[[i]]<-qualifiersdf(leagues[i],years)
        }
        fwrite(map_df(lista,bind_rows),paste("../CSV/Total/qualifiers",years,".csv",sep=""),sep=",",na=NA) 
    }
    for (i in 1:length(years)){
        aux(leagues,years[i])
    }
}

saveevents<-function(leagues,years){
    aux<-function(leagues,years){
        lista<-list()
        for (i in 1:length(leagues)){
            lista[[i]]<-eventsdf(leagues[i],years)
        }
        fwrite(map_df(lista,bind_rows),paste("../CSV/Total/events",years,".csv",sep=""),sep=",",na = NA) 
    }
    for (i in 1:length(years)){
        aux(leagues,years[i])
    }
}

savesevents<-function(leagues,years){
    aux<-function(leagues,years){
        lista<-list()
        for (i in 1:length(leagues)){
            lista[[i]]<-satisfieddf(leagues[i],years)
        }
        fwrite(map_df(lista,bind_rows),paste("../CSV/Total/sevents",years,".csv",sep=""),sep=",",na = NA) 
    }
    for (i in 1:length(years)){
        aux(leagues,years[i])
    }
}

qualifiersdf<-function(leagues,years){
    lista<-unlist(map(leagues,~paste("../CSV/",.x,"/",years,"/qualifiers.csv",sep="")))
    df<-map_df(lista,read_csv) %>%
        select(wsmatchid,wseventid,qualname,qualvalue) %>%
        distinct(wsmatchid,wseventid,qualname,.keep_all=TRUE) %>%
        spread(qualname,qualvalue,fill=0,convert=TRUE) %>%
        rename(crosss=Cross)
    colnames(df)<-tolower(names(df))
    df$wseventid<-parse_character(df$wseventid)
    return(df)
}

qualifiersdf2<-function(leagues,years){
    lista<-unlist(map(leagues,~paste("../CSV/",.x,"/",years,"/qualifiers.csv",sep="")))
    df<-map_df(lista,read_csv) %>%
        select(wsmatchid,wseventid,qualname,qualvalue) %>%
        distinct(wsmatchid,wseventid,qualname,.keep_all=TRUE) %>%
        spread(qualname,qualvalue,convert=TRUE) %>%
        rename(crosss=Cross)
    colnames(df)<-tolower(names(df))
    df$wseventid<-parse_character(df$wseventid)
    return(df)
}

satisfieddf<-function(leagues,years){
    lista<-unlist(map(leagues,~paste("../CSV/",.x,"/",years,"/satisfiedevents.csv",sep="")))
    df<-map_df(lista,read_csv) %>%
        select(wsmatchid,wseventid,satisfiedeventname,satisfiedeventvalue) %>%
        distinct(wsmatchid,wseventid,satisfiedeventname,.keep_all=TRUE) %>%
        spread(satisfiedeventname,satisfiedeventvalue,fill=0)
    colnames(df)<-tolower(names(df))
    df$wseventid<-parse_character(df$wseventid)
    return(df)
    
}

satisfieddf2<-function(leagues,years){
    lista<-unlist(map(leagues,~paste("../CSV/",.x,"/",years,"/satisfiedevents.csv",sep="")))
    df<-map_df(lista,read_csv) %>%
        select(wsmatchid,wseventid,satisfiedeventname,satisfiedeventvalue) %>%
        distinct(wsmatchid,wseventid,satisfiedeventname,.keep_all=TRUE) %>%
        spread(satisfiedeventname,satisfiedeventvalue)
    colnames(df)<-tolower(names(df))
    df$wseventid<-parse_character(df$wseventid)
    return(df)
    
}

eventstotaldf<-function(leagues,years){
    qualifiers<-qualifiersdf(leagues,years)
    satisfied<-satisfieddf(leagues,years)
    events<-eventsdf(leagues,years)
    teams<-teamsdf(leagues,years)
    players<-playersdf(leagues,years)
    matches<-matchesdf(leagues,years)
    
    eventscomplete<-events %>%
        left_join(players,by=c("playerid")) %>%
        left_join(players,by=c("relatedplayerid"="playerid")) %>%
        rename(playername=playername.x) %>%
        rename(relatedplayername=playername.y) %>%
        left_join(matches,by=c("wsmatchid")) %>%
        left_join(teams,by=c("teamid")) %>%
        left_join(qualifiers,by=c("wseventid")) %>%
        left_join(satisfied,by=c("wseventid")) %>%
        select(-starts_with("id"))
    
    return(eventscomplete)
}

eventstotaldf2<-function(leagues,years){
    qualifiers<-qualifiersdf2(leagues,years)
    satisfied<-satisfieddf2(leagues,years)
    events<-eventsdf(leagues,years)
    teams<-teamsdf(leagues,years)
    players<-playersdf(leagues,years)
    matches<-matchesdf(leagues,years)
    
    eventscomplete<-events %>%
        left_join(players,by=c("playerid")) %>%
        left_join(players,by=c("relatedplayerid"="playerid")) %>%
        rename(playername=playername.x) %>%
        rename(relatedplayername=playername.y) %>%
        left_join(matches,by=c("wsmatchid")) %>%
        left_join(teams,by=c("teamid")) %>%
        left_join(qualifiers,by=c("wseventid")) %>%
        left_join(satisfied,by=c("wseventid")) %>%
        select(-starts_with("id"))
    
    return(eventscomplete)
}



shotsdf<-function(leagues,years){
    shotsdfaux2<-function(leagues,years){
        eventscomplete<-eventstotaldf2(leagues,years)
        return(events2shotsdf(eventscomplete))
    }
    lista<-list()
    for (i in 1:length(years)){
        lista[[i]]<-map(leagues,~shotsdfaux2(.x,years[i]))    
    }
    return(map_df(lista,bind_rows))
    
}



passdf<-function(leagues,years){
    passdfaux2<-function(leagues,years){
        eventscomplete<-read_csv(paste("../CSV/",leagues,"/",years,"/eventsfull.csv",sep=""))
        return(events2passdf(eventscomplete))
    }
    lista<-list()
    for (i in 1:length(years)){
        lista[[i]]<-map(leagues,~passdfaux2(.x,years[i]))    
    }
    return(map_df(lista,bind_rows))
    
}

matchevents<-function(matchid){
    leagues<-c("La Liga","Bundesliga","Premier League","Serie A","Ligue 1")
    years<-c("2016-2017","2015-2016","2014-2015","2013-2014")
    matches<-matchesdf(leagues,years)
    league<-select(filter(matches,wsmatchid==matchid),league)[[1]]
    year<-select(filter(matches,wsmatchid==matchid),season)[[1]]
    eventsdf<-eventstotaldf(league,year) %>%
        filter(wsmatchid==matchid)
    return(eventsdf)
}

events2shotsdf<-function(events){
    shots<-events %>%
        filter(shot==TRUE) %>%
        select(-contains(".y"))
    shots<-shots[,colSums(is.na(shots))<nrow(shots)]
    return(shots)
}

events2passdf<-function(events){
    pass<-events %>%
        filter(type=="Pass") 
    pass<-pass[,colSums(is.na(pass))<nrow(pass)]
    return(pass)
}

writefullevents<-function(leagues,years){
    aux1<-function(leagues,years){
        write_csv(eventstotaldf(leagues,years),paste("../CSV/",leagues,"/",years,"/eventsfull.csv",sep=""))
    }
    for (i in 1:length(years)){
        walk(leagues,~aux1(.,years[i]))
    }
}

loadevents<-function(years){
    lista<-unlist(map(years,~paste("C:/tmp/events",.,".csv",sep="")))
    aux<-function(file){
        return(read_csv(file) %>%
                   select(wsmatchid,wseventid,playerid))
    }
    return(map_df(lista,aux))
}

loadsevents<-function(years){
    lista<-unlist(map(years,~paste("C:/tmp/sevents",.,".csv",sep="")))
    aux<-function(file){
        return(read_csv(file) %>%
                   select(wsmatchid,wseventid))
    }
    return(map_df(lista,aux))
}

distinctqualifiers<-function(leagues,years){
    lista<-unlist(map(leagues,~paste("../CSV/",.x,"/",years,"/qualifiers.csv",sep="")))
    aux<-function(file){
        return(read_csv(file) %>%
                   distinct(qualname))
    }
    lista2<-map(lista,aux)
    return(map_df(lista2,bind_rows)%>%
               distinct(qualname) %>%
               arrange(qualname))
}

distinctsevents<-function(leagues,years){
    lista<-unlist(map(leagues,~paste("../CSV/",.x,"/",years,"/satisfiedevents.csv",sep="")))
    aux<-function(file){
        return(read_csv(file) %>%
                   distinct(satisfiedeventname))
    }
    lista2<-map(lista,aux)
    return(map_df(lista2,bind_rows)%>%
               distinct(satisfiedeventname) %>%
               arrange(satisfiedeventname))
}

loadquals<-function(years){
    lista<-unlist(map(years,~paste("C:/tmp/qualifiers",.,".csv",sep="")))
    aux<-function(file){
        return(read_csv(file) %>%
                   select(wsmatchid,wseventid))
    }
    return(map_df(lista,aux))
}

shotsdf<-function(years){
    lista<-list()
    dist<-c("Length", "PassEndX", "Zone", 
            "PassEndY", "Angle", "OppositeRelatedEvent", 
            "RelatedEventId", "GoalMouthY", "GoalMouthZ", 
            "BlockedX", "BlockedY", "Foul", "PlayerPosition", 
            "JerseyNumber", "FormationSlot", "TeamFormation", 
            "TeamPlayerFormation", "InvolvedPlayers", "CaptainPlayerId", 
            "PlayerCaughtOffside")
    for (i in 1:length(years)){
        shots<-loadevents(years[i]) %>%
            filter(shot==TRUE) %>%
            .[,colSums(is.na(.))<nrow(.)]
        
        distinct<-shots %>%
            distinct(keyid)
        
        shotsquals<-loadquals(years[i]) %>%
            filter(keyid %in% distinct$keyid) %>%
            filter(!qualname %in% dist) %>%
            select(keyid,qualname,qualvalue) %>%
            spread(qualname,qualvalue,convert=TRUE,fill = 0)
        
        shotssevents<-loadsevents(years[i]) %>%
            filter(keyid %in% distinct$keyid) %>%
            select(keyid,satisfiedeventname,satisfiedeventvalue) %>%
            spread(satisfiedeventname,satisfiedeventvalue,convert=TRUE,fill = 0)
        
        shots<-shots %>%
            left_join(shotsquals,by=("keyid"="keyid")) %>%
            left_join(shotssevents,by=("keyid"="keyid")) 
        
        lista[[i]]<-shots
    }       
    matches<-read_csv("../CSV/Total/matches.csv") %>%
        select(wsmatchid,date,league,season,hometeamname,awayteamname)
    teams<-read_csv("../CSV/Total/teams.csv")
    players<-read_csv("../CSV/Total/players.csv")
    
    return(map_df(lista,bind_rows) %>%
               left_join(matches,by="wsmatchid") %>%
               left_join(teams,by="teamid") %>%
               left_join(players,by="playerid") %>%
               left_join(players,by=c("relatedplayerid"="playerid")) %>%
               rename(playername=playername.x) %>%
               rename(relatedplayername=playername.y)
    )
}


passdf<-function(years){
    lista<-list()
    dist<-c("Length", "PassEndX", "Zone", 
            "PassEndY", "Angle", "OppositeRelatedEvent", 
            "RelatedEventId", "GoalMouthY", "GoalMouthZ", 
            "BlockedX", "BlockedY", "Foul", "PlayerPosition", 
            "JerseyNumber", "FormationSlot", "TeamFormation", 
            "TeamPlayerFormation", "InvolvedPlayers", "CaptainPlayerId", 
            "PlayerCaughtOffside")
    for (i in 1:length(years)){
        ass<-loadevents(years[1]) %>%
            filter(type=="Pass") %>%
            .[,colSums(is.na(.))<nrow(.)]
        
        distinct<-pass$keyid
        
        passquals<-loadquals(years[1]) %>%
            filter(keyid %in% distinct) %>%
            select(keyid,qualname,qualvalue) %>%
            spread(qualname,qualvalue,convert=TRUE,fill = 0)
        
        passsevents<-loadsevents(years[1]) %>%
            filter(keyid %in% distinct) %>%
            select(keyid,satisfiedeventname,satisfiedeventvalue) %>%
            spread(satisfiedeventname,satisfiedeventvalue,convert=TRUE,fill = 0)
        
        pass<-pass %>%
            left_join(passquals,by=("keyid"="keyid")) %>%
            left_join(passsevents,by=("keyid"="keyid")) 
        
        lista[[i]]<-pass
    }       
    matches<-read_csv("../CSV/Total/matches.csv") %>%
        select(wsmatchid,date,league,season,hometeamname,awayteamname)
    teams<-read_csv("../CSV/Total/teams.csv")
    players<-read_csv("../CSV/Total/players.csv")
    
    return(map_df(lista,bind_rows) %>%
               left_join(matches,by="wsmatchid") %>%
               left_join(teams,by="teamid") %>%
               left_join(players,by="playerid") %>%
               left_join(players,by=c("relatedplayerid"="playerid")) %>%
               rename(playername=playername.x) %>%
               rename(relatedplayername=playername.y)
    )
}

eventsdffinal<-function(leagues,years){
    qualifiers<-qualifiersdf(leagues,years)
    events<-eventsdf(leagues,years)
    dist<-c("Length", "PassEndX", "Zone", "PassEndY", "Angle", "OppositeRelatedEvent", "RelatedEventId", "GoalMouthY", "GoalMouthZ", "BlockedX", "BlockedY", "Foul", "PlayerPosition", "JerseyNumber", "FormationSlot", "TeamFormation", "TeamPlayerFormation", "InvolvedPlayers", "CaptainPlayerId", "PlayerCaughtOffside")
    quals<-qualifiers %>%
        filter(qualname %in% dist) %>%
        select(-qualid) %>%
        spread(qualname,qualvalue,convert=TRUE)
    
    colnames(quals)<-tolower(names(quals))
    
    
    eventscomplete<-events %>%
        left_join(quals,by=c("wsmatchid","wseventid")) %>%
        select(-contains(".y")) %>%
        rename(matcheventid=matcheventid.x) %>%
        rename(relatedeventid=relatedeventid.x) %>%
        rename(blockedx=blockedx.x) %>%
        rename(blockedy=blockedy.x) %>%
        rename(goalmouthy=goalmouthy.x) %>%
        rename(goalmouthz=goalmouthz.x) 
    
    
    return(eventscomplete %>% 
               mutate(keyid=paste(wsmatchid,wseventid,sep="")))
}

loadevents<-function(years){
    lista<-unlist(map(years,~paste("../CSV/Total/events",.,".csv",sep="")))
    aux<-function(file){
        df<-read_csv(file,col_types = cols(
            wsmatchid = col_integer(),
            wseventid = col_character(),
            matcheventid = col_integer(),
            minute = col_integer(),
            second = col_integer(),
            expandedminute = col_integer(),
            teamid = col_integer(),
            playerid = col_integer(),
            period = col_character(),
            typeid = col_integer(),
            type = col_character(),
            outcometype = col_character(),
            x = col_double(),
            y = col_double(),
            endx = col_double(),
            endy = col_double(),
            relatedeventid = col_integer(),
            relatedplayerid = col_integer(),
            blockedx = col_double(),
            blockedy = col_double(),
            goalmouthz = col_double(),
            goalmouthy = col_double(),
            cardtype = col_character(),
            shot = col_logical(),
            touch = col_logical(),
            goal = col_logical(),
            keyid = col_character(),
            angle = col_double(),
            captainplayerid = col_integer(),
            formationslot = col_character(),
            foul = col_integer(),
            involvedplayers = col_character(),
            jerseynumber = col_character(),
            length = col_double(),
            oppositerelatedevent = col_integer(),
            passendx = col_double(),
            passendy = col_double(),
            playercaughtoffside = col_integer(),
            playerposition = col_character(),
            teamformation = col_character(),
            teamplayerformation = col_character(),
            zone = col_character()))
        return(df)
    }
    return(map_df(lista,aux))
}

loadsevents<-function(years){
    lista<-unlist(map(years,~paste("../CSV/Total/sevents",.,".csv",sep="")))
    aux<-function(file){
        df<-read_csv(file,col_types=cols(
            wsmatchid = col_integer(),
            wseventid = col_character(),
            matcheventid = col_integer(),
            satisfiedeventid = col_integer(),
            satisfiedeventname = col_character(),
            satisfiedeventvalue = col_integer(),
            keyid = col_character()
        ))
        df$wseventid<-parse_character(df$wseventid)
        return(df)
    }
    return(map_df(lista,aux))
}

loadquals<-function(years){
    lista<-unlist(map(years,~paste("../CSV/Total/qualifiers",.,".csv",sep="")))
    aux<-function(file){
        df<-read_csv(file,col_types = cols(
            wsmatchid = col_integer(),
            wseventid = col_character(),
            matcheventid = col_integer(),
            qualid = col_integer(),
            qualname = col_character(),
            qualvalue = col_character(),
            keyid = col_character()
        ))
        df$wseventid<-parse_character(df$wseventid)
        return(df)
    }
    return(map_df(lista,aux))
}

shotsdf<-function(years){
    lista<-list()
    dist<-c("Length", "PassEndX", "Zone", 
            "PassEndY", "Angle", "OppositeRelatedEvent", 
            "RelatedEventId", "GoalMouthY", "GoalMouthZ", 
            "BlockedX", "BlockedY", "Foul", "PlayerPosition", 
            "JerseyNumber", "FormationSlot", "TeamFormation", 
            "TeamPlayerFormation", "InvolvedPlayers", "CaptainPlayerId", 
            "PlayerCaughtOffside")
    for (i in 1:length(years)){
        shots<-loadevents(years[i]) %>%
            filter(shot==TRUE) %>%
            .[,colSums(is.na(.))<nrow(.)]
        
        distinct<-shots %>%
            distinct(keyid)
        
        shotsquals<-loadquals(years[i]) %>%
            filter(keyid %in% distinct$keyid) %>%
            filter(!qualname %in% dist) %>%
            select(keyid,qualname,qualvalue) %>%
            spread(qualname,qualvalue,convert=TRUE,fill = 0)
        
        
        shots<-shots %>%
            left_join(shotsquals,by=("keyid"="keyid")) 
        
        
        lista[[i]]<-shots
    }       
    matches<-read_csv("../CSV/Total/matches.csv") %>%
        select(wsmatchid,date,league,season,hometeamname,awayteamname)
    teams<-read_csv("../CSV/Total/teams.csv")
    players<-read_csv("../CSV/Total/players.csv")
    
    return(map_df(lista,bind_rows) %>%
               left_join(matches,by="wsmatchid") %>%
               left_join(teams,by="teamid") %>%
               left_join(players,by="playerid") %>%
               left_join(players,by=c("relatedplayerid"="playerid")) %>%
               rename(playername=playername.x) %>%
               rename(relatedplayername=playername.y)
    )
}

shotsdf2<-function(years){
    lista<-list()
    dist<-c("Length", "PassEndX", "Zone", 
            "PassEndY", "Angle", "OppositeRelatedEvent", 
            "RelatedEventId", "GoalMouthY", "GoalMouthZ", 
            "BlockedX", "BlockedY", "Foul", "PlayerPosition", 
            "JerseyNumber", "FormationSlot", "TeamFormation", 
            "TeamPlayerFormation", "InvolvedPlayers", "CaptainPlayerId", 
            "PlayerCaughtOffside")
    for (i in 1:length(years)){
        shots<-loadevents(years[i]) %>%
            filter(shot==TRUE) %>%
            .[,colSums(is.na(.))<nrow(.)]
        
        distinct<-shots %>%
            distinct(keyid)
        
        qualtype<-read_csv2("../CSV/Total/uniquequals.csv")
        
        shotsquals<-loadquals(years[i]) %>%
            filter(keyid %in% distinct$keyid) %>%
            filter(!qualname %in% dist) %>%
            left_join(qualtype,by="qualid") %>% 
            select(keyid,qualname.x,qualvalue,qualtype) %>% 
            mutate(qualvalue2=ifelse(qualname.x==qualtype,1,qualname.x)) %>%
            select(keyid,qualtype,qualvalue2) %>%
            spread(qualtype,qualvalue2,convert=TRUE,fill = 0)
        
        shots<-shots %>%
            left_join(shotsquals,by=("keyid"="keyid")) 
        
        
        lista[[i]]<-shots
    }       
    matches<-read_csv("../CSV/Total/matches.csv") %>%
        select(wsmatchid,date,league,season,hometeamname,awayteamname)
    teams<-read_csv("../CSV/Total/teams.csv")
    players<-read_csv("../CSV/Total/players.csv")
    
    return(map_df(lista,bind_rows) %>%
               left_join(matches,by="wsmatchid") %>%
               left_join(teams,by="teamid") %>%
               left_join(players,by="playerid") %>%
               left_join(players,by=c("relatedplayerid"="playerid")) %>%
               rename(playername=playername.x) %>%
               rename(relatedplayername=playername.y)
    )
}


passdf<-function(years){
    lista<-list()
    dist<-c("Length", "PassEndX", "Zone", 
            "PassEndY", "Angle", "OppositeRelatedEvent", 
            "RelatedEventId", "GoalMouthY", "GoalMouthZ", 
            "BlockedX", "BlockedY", "Foul", "PlayerPosition", 
            "JerseyNumber", "FormationSlot", "TeamFormation", 
            "TeamPlayerFormation", "InvolvedPlayers", "CaptainPlayerId", 
            "PlayerCaughtOffside")
    for (i in 1:length(years)){
        pass<-loadevents(years[1]) %>%
            filter(type=="Pass")
        
        distinct<-pass$keyid
        
        passquals<-loadquals(years[1]) %>%
            filter(keyid %in% distinct) %>%
            select(keyid,qualname,qualvalue) %>%
            spread(qualname,qualvalue,convert=TRUE,fill = 0)
        
        pass<-pass %>%
            left_join(passquals,by=("keyid"="keyid"))
        lista[[i]]<-pass
    }       
    matches<-read_csv("../CSV/Total/matches.csv") %>%
        select(wsmatchid,date,league,season,hometeamname,awayteamname)
    teams<-read_csv("../CSV/Total/teams.csv")
    players<-read_csv("../CSV/Total/players.csv")
    
    return(map_df(lista,bind_rows) %>%
               left_join(matches,by="wsmatchid") %>%
               left_join(teams,by="teamid") %>%
               left_join(players,by="playerid") %>%
               left_join(players,by=c("relatedplayerid"="playerid")) %>%
               rename(playername=playername.x) %>%
               rename(relatedplayername=playername.y)
    )
}


