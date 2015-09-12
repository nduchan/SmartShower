CREATE TABLE users
(
	id INT AUTO_INCREMENT PRIMARY KEY,
	fname VARCHAR(20),
	lname VARCHAR(20),
	phone CHAR(10),
	email VARCHAR(42),
	address VARCHAR(12),
	credentials VARCHAR(1024),
	morning INT
);

