-- If Players and Matches already present drop those tables then create
-- Players table and Matches table
DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS Matches;
CREATE TABLE Players(
                    player_id serial primary key,
                    name text
                    );
CREATE TABLE Matches(
                    match_id serial primary key,
                    winner integer references Players(player_id),
                    loser integer references Players(player_id)
                    );
