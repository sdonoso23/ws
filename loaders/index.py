import pandas as pd
import sqlite3

conn = sqlite3.connect('../CSV/Total/test2.sqlite')
cursor = conn.cursor()

cursor.execute('CREATE INDEX events_key on events (keyid)')
cursor.execute('CREATE INDEX events_match on events (wsmatchid)')
cursor.execute('CREATE INDEX events_player on events (playerid)')
cursor.execute('CREATE INDEX events_team on events (teamid)')
cursor.execute('CREATE INDEX events_type on events (type)')
cursor.execute('CREATE INDEX qual_key on qualifiers (keyid)')
cursor.execute('CREATE INDEX qual_match on qualifiers (wsmatchid)')
cursor.execute('CREATE INDEX qual_name on qualifiers (qualname)')
cursor.execute('CREATE INDEX matches_match on matches (wsmatchid)')
cursor.execute('CREATE INDEX players_player on players (playerid)')
cursor.execute('CREATE INDEX teams_team on teams (teamid)')