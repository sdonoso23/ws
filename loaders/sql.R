library(RSQLite)
library(tidyverse)

setwd("C:/Users/Administrador.000/Desktop/Sebastian/Code/Whoscored/R")
con<-dbConnect(drv=SQLite(), dbname="../CSV/Total/football.sqlite")

walk(years,~dbWriteTable(conn=con,
                         name="events",
                         value = read_feather(paste("../CSV/Total/events",.,".feather",sep="")),
                         row.names=FALSE,append=TRUE))

walk(years,~dbWriteTable(conn=con,
                         name="qualifiers",
                         value = read_feather(paste("../CSV/Total/qualifiers",.,".feather",sep="")),
                         row.names=FALSE,append=TRUE))
dbWriteTable(conn=con,
             name="teams",
             value = read_feather("../CSV/Total/teams.feather"),
             row.names=FALSE,append=TRUE)

dbWriteTable(conn=con,
             name="players",
             value = read_feather("../CSV/Total/players.feather"),
             row.names=FALSE,append=TRUE)

dbWriteTable(conn=con,
             name="matches",
             value = read_feather("../CSV/Total/matches.feather"),
             row.names=FALSE,append=TRUE)

dbSendQuery(con,"CREATE INDEX events_key on events (keyid)")
dbSendQuery(con,"CREATE INDEX events_match on events (wsmatchid)")
dbSendQuery(con,"CREATE INDEX events_player on events (playerid)")
dbSendQuery(con,"CREATE INDEX events_team on events (teamid)")
dbSendQuery(con,"CREATE INDEX events_type on events (type)")
dbSendQuery(con,"CREATE INDEX qual_key on qualifiers (keyid)")
dbSendQuery(con,"CREATE INDEX qual_match on qualifiers (wsmatchid)")
dbSendQuery(con,"CREATE INDEX matches_match on matches (wsmatchid)")
dbSendQuery(con,"CREATE INDEX players_player on players (playerid)")
dbSendQuery(con,"CREATE INDEX teams_team on team (teamid)")

dbDisconnect(con)



