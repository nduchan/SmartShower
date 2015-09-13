DELIMITER //
CREATE FUNCTION sf_createUser(
	u_fname VARCHAR(20),
	u_lname VARCHAR(20),
	u_email VARCHAR(42),
	u_password VARCHAR(64)
) RETURNS INT 
BEGIN
	DECLARE success INT;
	IF (SELECT EXISTS(
			SELECT 1 
			FROM users
			WHERE email = u_email)
		) 
		THEN return 0;
	ELSE
		INSERT INTO users(
			fname,
			lname,
			email,
			password
		)
		VALUES(
			u_fname,
			u_lname,
			u_email,
			u_password
		);
		return 1;	
	END IF;
END//
DELIMITER ;
