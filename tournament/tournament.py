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
    c.execute("DELETE FROM Matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM Players;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered.

            Select all player rows and retun the count of the total
            number rows"""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT count(*) as num from Players;")
    count = c.fetchone()[0]
    conn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

        Inserts a new row into the Players table with name passed in and
        player_id is automatically generated as a  serial"""
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO Players (name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

        Creates a playerStanding list object and then fetches all player rows
        and select the count of wins from matches and the count of total
        number of matches where a player is either winner or loser and
        append the result to a blank list object called eachPlayer

        Append that list object to the playerStanding list as a tuple
        containing player_id, name, wins, matches"""
    playerStanding = []
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT Players.player_id, Players.name, \
    (SELECT count(Matches.winner) FROM Matches \
    WHERE Players.player_id = Matches.winner) AS wins, \
    (SELECT count(Matches.match_id) FROM Matches \
    WHERE Players.player_id = Matches.winner OR \
    Players.player_id = Matches.loser) AS matches FROM Players;")
    rows = c.fetchall()
    for row in rows:
        playerStanding.append(row)
    return playerStanding
    conn.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

        Update the value of winner to be the passed in winner, then update the
        value of loser to be the passed in loser both of these values are
        stored inside the Matches table"""

    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO Matches (winner, loser) \
                VALUES (%s, %s)" % (winner, loser))
    conn.commit()
    c.execute("SELECT * FROM Matches;")
    matches = c.fetchall()
    return matches
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

        First retrieves all the player_id, name, and wins from Players and
        Matches tables then get the length of the returned results and create
        an empty list matched, then for each result from the length 0 to the
        end of the returned results - 1 step each iteration by 2.
        Assign the First result index 0(player_id) and first result index
        1(name) and second result index 0(player_id) and second result
        index 1(name) to paired and append paired to the matched list object
        then increment by 2 and return the results index i index 0 and so
        on until the length of the passed in Players query is reached.

        return the matched list of (player_id, name, player_id, name) objects
    """
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT Players.player_id, Players.name, \
    (SELECT count(Matches.winner) FROM Matches \
    WHERE Players.player_id = Matches.winner) AS wins FROM Players \
    ORDER BY wins DESC;")
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
# print countPlayers()
