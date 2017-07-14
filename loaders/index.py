import pandas as pd
import sqlite3


def createindex(conn):

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

def dropindex(conn):

	cursor = conn.cursor()

	cursor.execute('DROP INDEX events_key')
	cursor.execute('DROP INDEX events_match')
	cursor.execute('DROP INDEX events_player')
	cursor.execute('DROP INDEX events_team')
	cursor.execute('DROP INDEX events_type')
	cursor.execute('DROP INDEX qual_key')
	cursor.execute('DROP INDEX qual_match')
	cursor.execute('DROP INDEX qual_name')
	cursor.execute('DROP INDEX matches_match')
	cursor.execute('DROP INDEX players_player')
	cursor.execute('DROP INDEX teams_team')