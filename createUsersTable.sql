CREATE TABLE users
(
	id INT AUTO_INCREMENT PRIMARY KEY,
	fname VARCHAR(20),
	lname VARCHAR(20),
	email VARCHAR(42),
	password VARCHAR(64),
	phone CHAR(10),
	address VARCHAR(12),
	duration INT,
	buffer INT,
	morning BOOLEAN,
	event TIMESTAMP
);

