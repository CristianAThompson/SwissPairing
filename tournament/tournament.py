#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")



def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * from Players;")
    rows = c.fetchall()
    for row in rows:
        c.execute("UPDATE Players SET wins = 0 WHERE player_id = %s;" % row[0])
        c.execute("UPDATE Players SET matches = 0 WHERE player_id = %s;" % row[0])
        conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS players CASCADE;")
    conn.commit()
    c.execute('CREATE TABLE players(player_id serial primary key, name text, \
                wins integer, matches integer);')
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * from players;")
    count = c.rowcount;
    print count
    conn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("insert into Players (name, wins, matches) values (%s, 0, 0)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    playerStanding = []
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * from Players;")
    rows = c.fetchall()
    for row in rows:
        eachPlayer = []
        if row[0] != None:
            eachPlayer.append(row[0])
        if row[1] != None:
            eachPlayer.append(row[1])
        if row[2] != None:
            eachPlayer.append(row[2])
        else:
            eachPlayer.append(0)
        if row[3] != None:
            eachPlayer.append(row[3])
        else:
            eachPlayer.append(0)
        playerStanding.append(eachPlayer)

    return playerStanding
    conn.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE Players SET wins = wins + 1 WHERE player_id = %s;" % winner)
    c.execute("UPDATE Players SET matches = matches + 1 WHERE player_id = %s;" % winner)
    c.execute("SELECT * from Players WHERE player_id = %s;" % winner)
    winner = c.fetchone()
    conn.commit()
    print winner
    # c.execute("UPDATE Players SET wins = wins - 1 WHERE player_id = %s;" % loser)
    c.execute("UPDATE Players SET matches = matches + 1 WHERE player_id = %s;" % loser)
    c.execute("SELECT * from Players WHERE player_id = %s;" % loser)
    loser = c.fetchone()
    conn.commit()
    print loser

    conn.close()



def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    c = conn.cursor()
    # c.execute("SELECT one.player_id, one.name, two.player_id, two.name \
    #             FROM Players AS one LEFT JOIN Players AS two ON \
    #             (one.player_id, one.name) != (two.player_id, two.name);")
    # pair = c.fetchall()
    # for row in pair:
    #     print row
    c.execute("SELECT player_id, name, wins FROM Players ORDER BY wins;")
    results = c.fetchall()
    matched = []
    total_length = len(results)
    for i in range(0, total_length - 1, 2):
        paired = (results[i][0], results[i][1],
                    results[i + 1][0], results[i + 1][1])
        matched.append(paired)
    conn.close()
    return matched







# registerPlayer("Mike")
# registerPlayer("Dave")
# registerPlayer("Tom")
# registerPlayer("Steve")
# print playerStandings()
# standings = playerStandings()
# [id1, id2, id3, id4] = [row[0] for row in standings]
# reportMatch(id1, id2)
# reportMatch(id3, id4)
# print playerStandings()
print swissPairings()
# deletePlayers()
# countPlayers()
