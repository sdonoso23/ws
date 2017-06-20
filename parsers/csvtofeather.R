library(tidyverse)
library(ggplot2)
library(data.table)
library(feather)
library(RSQLite)

####PREPARING CSV FILES####

matchesdf<-function(leagues,years){
    lista<-unlist(map(leagues,~paste("../CSV/",.x,"/",years,"/matches.csv",sep="")))
    return(map_df(lista,read_csv) %>%
               select(-id))
}

eventsdf<-function(leagues,years){
    lista<-unlist(map(leagues,~paste("../CSV/",.x,"/",years,"/events.csv",sep="")))
    df<-map_df(lista,read_csv)
    colnames(df)<-tolower(names(df))
    df$wseventid<-parse_character(df$wseventid)
    df<-df %>%
        mutate(keyid=paste(wsmatchid,wseventid,sep="")) %>%
        select(-id)
    
    return(df)
}

teamsdf<-function(leagues,years){
    lista<-unlist(map(leagues,~paste("../CSV/",.x,"/",years,"/teams.csv",sep="")))
    return(map_df(lista,read_csv) %>%
               distinct(teamid,.keep_all=TRUE) %>%
               select(-id))
}

playersdf<-function(leagues,years){
    lista<-unlist(map(leagues,~paste("../CSV/",.x,"/",years,"/playerslist.csv",sep="")))
    return(map_df(lista,read_csv) %>%
               distinct(playerid,.keep_all=TRUE) %>%
               select(-id))
}

refereedf<-function(leagues,years){
    lista<-unlist(map(leagues,~paste("../CSV/",.x,"/",years,"/referees.csv",sep="")))
    return(map_df(lista,read_csv) %>%
               distinct(refereeid,.keep_all=TRUE) %>%
               select(-id)) %>%
        na.omit()
}

qualifiersdf<-function(leagues,years){
    lista<-unlist(map(leagues,~paste("../CSV/",.x,"/",years,"/qualifiers.csv",sep="")))
    df<-map_df(lista,read_csv) %>%
        distinct(wsmatchid,wseventid,qualname,.keep_all=TRUE) %>%
        select(-id) 
    colnames(df)<-tolower(names(df))
    df$wseventid<-parse_character(df$wseventid)
    df<-mutate(df,keyid=paste(wsmatchid,wseventid,sep=""))
    return(df)
}

satisfieddf<-function(leagues,years){
    lista<-unlist(map(leagues,~paste("../CSV/",.x,"/",years,"/satisfiedevents.csv",sep="")))
    df<-map_df(lista,read_csv) %>%
        distinct(wsmatchid,wseventid,satisfiedeventname,.keep_all=TRUE) %>%
        select(-id)
    colnames(df)<-tolower(names(df))
    df$wseventid<-parse_character(df$wseventid)
    df<-mutate(df,keyid=paste(wsmatchid,wseventid,sep=""))
    return(df)
    
}

formationsdf<-function(leagues,years){
    lista<-unlist(map(leagues,~paste("../CSV/",.x,"/",years,"/formations.csv",sep="")))
    
    df<-map_df(lista,~read_csv(.,col_types = cols(formationname=col_character())) %>%
                   select(-id,-xposition,-yposition) %>%
                   spread(slotnumber,playerid) %>%
                   select(c(1:12,15:22,13,14))       ) 
    df$subonplayerid<-parse_integer(df$subonplayerid)
    df$suboffplayerid<-parse_integer(df$suboffplayerid)
    
    return(df)
}

datadf<-function(leagues,years,table){
    lista<-map(flatten(map(leagues,~paste("../CSV/",.x,"/",years,"/",sep=""))),~paste(.x,table,".csv",sep=""))
    return(map_df(lista,read_csv))
}

####SAVE CSV BY YEAR####

savematches<-function(leagues,years){
    write_feather(matchesdf(leagues,years),"../CSV/Total/matches.feather")
}

saveplayers<-function(leagues,years){
    write_feather(playersdf(leagues,years),"../CSV/Total/players.feather")
}

savereferees<-function(leagues,years){
    write_feather(refereedf(leagues,years),"../CSV/Total/referees.feather")
}

saveteams<-function(leagues,years){
    write_feather(teamsdf(leagues,years),"../CSV/Total/teams.feather")
}

saveformations<-function(leagues,years){
    write_feather(formationsdf(leagues,years),"../CSV/Total/formations.feather")
}

saveevents<-function(leagues,years){
    aux<-function(leagues,years){
        lista<-list()
        for (i in 1:length(leagues)){
            lista[[i]]<-eventsdf(leagues[i],years)
        }
        write_feather(map_df(lista,bind_rows),paste("../CSV/Total/events",years,".feather",sep="")) 
    }
    for (i in 1:length(years)){
        aux(leagues,years[i])
    }
}

savequalifiers<-function(leagues,years){
    aux<-function(leagues,years){
        lista<-list()
        for (i in 1:length(leagues)){
            lista[[i]]<-qualifiersdf(leagues[i],years)
        }
        write_feather(map_df(lista,bind_rows),paste("../CSV/Total/qualifiers",years,".feather",sep="")) 
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
        write_feather(map_df(lista,bind_rows),paste("../CSV/Total/sevents",years,".feather",sep="")) 
    }
    for (i in 1:length(years)){
        aux(leagues,years[i])
    }
}