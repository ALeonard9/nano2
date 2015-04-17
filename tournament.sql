DROP TABLE match;
DROP TABLE round;
DROP TABLE player;
DROP TABLE tournament;

CREATE TABLE tournament
(
tourney_id serial,
tourney_name varchar(255),
PRIMARY KEY (tourney_id)
);

CREATE TABLE player
(
player_id serial,
player_name varchar(255),
PRIMARY KEY (player_id)
);

CREATE TABLE round
(
round_id serial,
tourney_id int,
round int,
PRIMARY KEY (round_id),
FOREIGN KEY (tourney_id) REFERENCES tournament(tourney_id)
);

CREATE TABLE match
(
match_id serial,
round_id int,
player_id int,
result int,
PRIMARY KEY (match_id),
FOREIGN KEY (round_id) REFERENCES round(round_id),
FOREIGN KEY (player_id) REFERENCES player(player_id)
);

INSERT INTO tournament (tourney_name) VALUES ('default');

INSERT INTO round (tourney_id, round) VALUES (1 , 1),(1, 2), (1, 3), (1, 4);
