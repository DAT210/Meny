DROP DATABASE IF EXISTS dat210_menu;

CREATE DATABASE dat210_menu;

USE dat210_menu;

CREATE TABLE ingredient (
	i_id INT(6) AUTO_INCREMENT,
    i_name VARCHAR(64) NOT NULL UNIQUE,
    available BOOLEAN,
    PRIMARY KEY (i_id)
);


CREATE TABLE allergene (
	a_id INT(5) AUTO_INCREMENT,
    a_name VARCHAR(64) NOT NULL UNIQUE,
    PRIMARY KEY (a_id)
);

CREATE TABLE category (
	ca_id INT(3) AUTO_INCREMENT,
    ca_name VARCHAR(64) NOT NULL UNIQUE,
    PRIMARY KEY (ca_id)
);


CREATE TABLE course (
	c_id INT(5) AUTO_INCREMENT,
    c_name VARCHAR(64) NOT NULL UNIQUE,
    ca_id INT(3),
    price DECIMAL(6, 2),
    PRIMARY KEY (c_id),
    FOREIGN KEY (ca_id) REFERENCES category(ca_id)
);


CREATE TABLE course_ingredient (
	c_id INT(5),
    i_id INT(6),
    PRIMARY KEY (c_id, i_id),
    FOREIGN KEY (c_id) REFERENCES course(c_id),
	FOREIGN KEY (i_id) REFERENCES ingredient(i_id)
);


CREATE TABLE ingredient_allergene (
	i_id INT(6),
	a_id INT(5),
    PRIMARY KEY (i_id, a_id),
    FOREIGN KEY (i_id) REFERENCES ingredient(i_id),
    FOREIGN KEY (a_id) REFERENCES allergene(a_id)
);

/* Add dummy values to the database */

INSERT INTO ingredient (i_name, available) VALUES
	("ingredient alpha", true),
    ("ingredient bravo", true),
    ("ingredient charlie", true),
    ("ingredient delta", true),
    ("ingredient echo", true);
    
    
INSERT INTO allergene (a_name) VALUES
	("allergene alpha"),
    ("allergene bravo"),
    ("allergene charlie"),
    ("allergene delta"),
    ("allergene echo");
    
    
INSERT INTO course (c_name, price) VALUES 
	("course alpha", "5.20"),
    ("course bravo", "4.20"),
    ("course charlie", "3.75"),
    ("course delta", "2.10"),
    ("course echo", "7.40");
  
  
INSERT INTO category (ca_name) VALUES 
	("category alpha"),
    ("category bravo"),
    ("category charlie"),
    ("category delta");
    
    
INSERT INTO course_ingredient (c_id, i_id) VALUES
	(1, 1),
    (1, 3),
    (2, 2),
    (2, 5),
    (2, 1),
    (3, 1),
    (3, 3),
    (4, 5),
    (4, 1),
    (5, 1),
    (5, 2),
    (5, 3);
    
INSERT INTO ingredient_allergene (i_id, a_id) VALUES
	(1, 2),
    (2, 3),
    (1, 3);