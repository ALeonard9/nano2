#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("delete from match")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("delete from player")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("select count(*) from player")
    a = cursor.fetchone()[0]
    DB.commit()
    DB.close()
    return a

def registerPlayer(name):
    """Adds a player to the tournament database."""
    
    name = bleach.clean(name)
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("INSERT INTO player (player_name) VALUES (%s)", (name,))
    DB.commit()
    DB.close()

"""    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie."""


    DB = connect()
    cursor = DB.cursor()
    cursor.execute("select p.player_id, player_name, coalesce(sum(result), 0)::int as wins, count(result)::int as matches from player p left join match m on p.player_id = m.player_id group by p.player_id order by wins DESC")
    a = cursor.fetchall()
    DB.commit()
    DB.close()
    return a

"""    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players."""
    
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("INSERT INTO match (round_id, player_id, result) VALUES (1, (%s), 1)", (winner,))
    cursor.execute("INSERT INTO match (round_id, player_id, result) VALUES (1, (%s), 0)", (loser,))
    DB.commit()
    DB.close()

 
def swissPairings():
    DB = connect()
    cursor = DB.cursor()
    cursor.execute("select r.player_id, r.player_name, e.player_id, e.player_name from (select a.player_id, a.player_name, sum(m.result)::int as wins from player a, match m where a.player_id = m.player_id group by a.player_id order by wins desc) r inner join (select a.player_id, a.player_name, sum(m.result)::int as wins from player a, match m where a.player_id = m.player_id group by a.player_id order by wins desc) e on r.player_id <> e.player_id and r.wins = e.wins where r.player_id < e.player_id")
    a = cursor.fetchall()
    DB.commit()
    DB.close()
    return a 
