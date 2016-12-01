use TEMP_MESSAGE;
show tables;

DROP TABLE IF EXISTS Tester;
CREATE TABLE TEMP_MESSAGE.tester 
(
	id BIGINT NOT NULL AUTO_INCREMENT,
	name VARCHAR(45) NULL,
	email VARCHAR(45) NULL,
	age integer,
	gender char(1),
    PRIMARY KEY (id)
);
    
DROP TABLE IF EXISTS message;
create table TEMP_MESSAGE.message 
(
	message VARCHAR(100) not null,
    message_id int primary key,
    from_tester_id int,
    to_tester_id int, 
FOREIGN KEY (from_tester_id) REFERENCES tester(tester_id),
FOREIGN KEY (to_tester_id) REFERENCES tester(tester_id)
);



INSERT INTO tester (name,email,age,gender)
VALUES ('Yuri Ahron', 'yuri@gmail.com', 32, 'm');

INSERT INTO tester (name,email,age,gender)
VALUES ('Michal Abu-ish', 'mich563@gmail.com', 23, 'f');

select * from tester;

drop table if exists TEMP_MESSAGE.player;
Create TABLE TEMP_MESSAGE.player
(
	nickname varchar(40) unique,
    player_id int primary key AUTO_INCREMENT
);

INSERT INTO player (nickname) values ('Johney');

select * from player;

DROP TABLE IF EXISTS message;
create table TEMP_MESSAGE.message 
(
	message VARCHAR(100) not null,
    message_id int primary key AUTO_INCREMENT ,
    from_player_id int,
    to_player_id int, 
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (from_player_id) REFERENCES player(player_id),
FOREIGN KEY (to_player_id) REFERENCES player(player_id)
);



INSERT INTO message (message, to_player_id, from_player_id) values ('Hi', 1, 4); 

select * from message;