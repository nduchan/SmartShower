CREATE TABLE users
(
	id INT AUTO_INCREMENT NOT NULL,
	fname VARCHAR(20),
	lname VARCHAR(20),
	email VARCHAR(42),
	password VARCHAR(64),
	phone CHAR(10),
	address VARCHAR(12),
	duration INT,
	buffer INT,
	morning BOOLEAN,
	event TIMESTAMP NULL,
	calendar_id VARCHAR(128),

	CONSTRAINT pk_id PRIMARY KEY (id)
);

CREATE TABLE times
(
	id INT,
	showertime TIMESTAMP,

	CONSTRAINT pk_id PRIMARY KEY (id),
	FOREIGN KEY (id) REFERENCES users(id)

);

CREATE TABLE address
(
	house_address VARCHAR(12) NOT NULL,
	calendar_id VARCHAR(128),

	CONSTRAINT pk_address PRIMARY KEY (house_address)

);

