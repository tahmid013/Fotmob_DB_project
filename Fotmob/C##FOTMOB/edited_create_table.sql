

CREATE TABLE Referee	(
Referee_id NUMBER GENERATED BY DEFAULT AS IDENTITY,
Referee_name VARCHAR2(25) NOT NULL,
Match_controlled NUMBER,
 CONSTRAINT Referee_pk PRIMARY KEY(Referee_id)
);

CREATE TABLE Stadium	(
Stadium_id NUMBER GENERATED BY DEFAULT AS IDENTITY,
Stadium_name VARCHAR2(25) NOT NULL,
Capacity NUMBER NOT NULL,
 CONSTRAINT Stadium_pk PRIMARY KEY(Stadium_id)
);


CREATE TABLE Team	(
Team_id NUMBER GENERATED BY DEFAULT AS IDENTITY,
Team_name VARCHAR2(25) NOT NULL,
Short_name VARCHAR2(25) NOT NULL,
 CONSTRAINT Team_pk PRIMARY KEY(Team_id)
);


CREATE TABLE Coach	(
Coach_id NUMBER GENERATED BY DEFAULT AS IDENTITY,
Coach_name VARCHAR2(25) NOT NULL,
Leagues_won NUMBER NOT NULL,
Team_id NUMBER(12),
 CONSTRAINT Coach_pk PRIMARY KEY(Coach_id),
CONSTRAINT Team_fk FOREIGN KEY(Team_id) REFERENCES Team(Team_id)
);


CREATE TABLE Player	(
Player_id NUMBER GENERATED BY DEFAULT AS IDENTITY,
First_name VARCHAR2(25) NOT NULL,
Last_name VARCHAR2(25) NOT NULL,
Position VARCHAR2(25) NOT NULL,
Minutes_played NUMBER NOT NULL,
Red_card NUMBER NOT NULL,
Yellow_card NUMBER NOT NULL,
Country  VARCHAR2(25) NOT NULL,
Team_id NUMBER(12),
 CONSTRAINT Player_pk PRIMARY KEY(Player_id),
CONSTRAINT Team_fk2 FOREIGN KEY(Team_id) REFERENCES Team(Team_id)
);


CREATE TABLE Match	(
Match_id NUMBER GENERATED BY DEFAULT AS IDENTITY,
Date_ DATE NOT NULL ,
Attendance NUMBER(20) NOT NULL,
Referee_id NUMBER(12),
Stadium_id NUMBER(12),
Home_id NUMBER(12),
Away_id NUMBER(12),
 CONSTRAINT Match_pk PRIMARY KEY(Match_id),
 CONSTRAINT Referee_fk FOREIGN KEY(Referee_id) REFERENCES Referee(Referee_id),
 CONSTRAINT Stadium_fk FOREIGN KEY(Stadium_id) REFERENCES Stadium(Stadium_id),
 CONSTRAINT Home_fk FOREIGN KEY(Home_id) REFERENCES Team(Team_id) , 
 CONSTRAINT Away_fk FOREIGN KEY(Away_id) REFERENCES  Team(Team_id)   
);


CREATE TABLE Scores 	(
Score_id NUMBER GENERATED BY DEFAULT AS IDENTITY,
Goals NUMBER NOT NULL,
Assist NUMBER,
Scoring_id NUMBER(12),
Assist_id NUMBER(12),
Team_id NUMBER(12),
Match_id NUMBER(12),
 CONSTRAINT Score_pk PRIMARY KEY(Score_id),
 CONSTRAINT Match_fk2 FOREIGN KEY(Match_id) REFERENCES Match(Match_id),
 CONSTRAINT Team_fk3 FOREIGN KEY(Team_id) REFERENCES Team(Team_id),
 CONSTRAINT Scoring_fk FOREIGN KEY(Scoring_id) REFERENCES Player(Player_id) ,   
 CONSTRAINT Assist_fk FOREIGN KEY(Assist_id) REFERENCES Player(Player_id) 
);

CREATE TABLE Plays	(
Player_id NUMBER ,
Match_id NUMBER(12),
 CONSTRAINT Player_rel_pk PRIMARY KEY(Player_id,Match_id),
 CONSTRAINT player_play_fk2 FOREIGN KEY(Player_id) REFERENCES Player(Player_id) ,   
 CONSTRAINT match_played_fk2 FOREIGN KEY(Match_id) REFERENCES Match(Match_id) 
);

