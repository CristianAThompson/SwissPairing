-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
create database tournament;
DROP TABLE IF EXISTS Players;
CREATE TABLE players(player_id serial primary key, name text, wins integer, matches integer);
DROP TABLE IF EXISTS Matches;
CREATE TABLE matches(first_player_id integer references Players(player_id),
                    second_player_id integer references Players(player_id),
                    winner integer);
