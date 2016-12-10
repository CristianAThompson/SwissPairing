-- If Players and Matches already present drop those tables then create
-- Players table and Matches table
DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS Matches;
CREATE TABLE Players(
                    player_id serial primary key,
                    name text,
                    wins integer,
                    matches integer
                    );
CREATE TABLE Matches(
                    first_player_id integer references Players(player_id),
                    second_player_id integer references Players(player_id),
                    winner integer
                    );
