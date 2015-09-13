DELIMITER //
CREATE PROCEDURE sp_createUser(
	IN u_fname VARCHAR(20),
	IN u_lname VARCHAR(20),
	IN u_email VARCHAR(42),
	IN u_password VARCHAR(64),
	OUT success INT
)
BEGIN
	if (SELECT EXISTS(
			SELECT 1 
			FROM users
			WHERE email = u_email)
		) 
		THEN SELECT 0 INTO success;
	ELSE
		INSERT INTO users(
			fname,
			lname,
			email,
			password
		)
		values(
			u_fname,
			u_lname,
			u_email,
			u_password
		);
		SELECT 1 INTO success;
	END IF;
END//
DELIMITER ;
