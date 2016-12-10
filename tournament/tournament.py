#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")



def deleteMatches():
    """Remove all the match records from the database.

        Select all players then for each player row update the quantity of win
        and match records to 0."""
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
    """Remove all the player records from the database.

        First Remove the current Players table then recreate the empty
        Players table with id, name, wins, and matches defined"""
    conn = connect()
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS Players CASCADE;")
    conn.commit()
    c.execute('CREATE TABLE Players(player_id serial primary key, name text, \
                wins integer, matches integer);')
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered.

            Select all player rows and retun the count of the total
            number rows"""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * from Players;")
    count = c.rowcount;
    conn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

        Inserts a new row into the Players table with name passed in and
        0 wins and 0 matches, player_id is automatically generated as a
        serial"""
    conn = connect()
    c = conn.cursor()
    c.execute("insert into Players (name, wins, matches) values (%s, 0, 0)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

        Creates a playerStanding list object and then fetches all player rows
        for each player row if the index is present append the value to
        a blank list object called eachPlayer, for index 2 wins and index 3
        matches, if it returns No Value or None append the integer 0 instead

        After each index has been appended to eachPlayer append that list
        list object to the playerStanding list as a tuple"""
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

        Update the value of wins to be current wins + 1 and increment matches
        by 1 as well for the passed in winner, then update the value of
        wins to be current wins - 1 and increment matches by 1 for the passed
        in loser"""

    conn = connect()
    c = conn.cursor()
    c.execute("UPDATE Players SET wins = wins + 1 WHERE player_id = %s;" % winner)
    c.execute("UPDATE Players SET matches = matches + 1 WHERE player_id = %s;" % winner)
    c.execute("SELECT * from Players WHERE player_id = %s;" % winner)
    winner = c.fetchone()
    conn.commit()
    print winner
    c.execute("UPDATE Players SET matches = matches + 1 WHERE player_id = %s;" % loser)
    c.execute("SELECT * from Players WHERE player_id = %s;" % loser)
    loser = c.fetchone()
    conn.commit()
    print loser

    conn.close()



def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

        First retrieves all the player_id, name, and wins from Players table
        then get the length of the returned results and create an empty list
        matched, then for each result from the length 0 to the end of the
        returned results - 1 step each iteration by 2.
        Assign the First result index 0(player_id) and first result index
        1(name) and second result index 0(player_id) and second result
        index 1(name) to paired and append paired to the matched list object
        then increment by 2 and return the results index i index 0 and so
        on until the length of the passed in Players query is reached.

        return the matched list of (player_id, name, player_id, name) objects
    """
    conn = connect()
    c = conn.cursor()
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
# print swissPairings()
# deletePlayers()
# countPlayers()
