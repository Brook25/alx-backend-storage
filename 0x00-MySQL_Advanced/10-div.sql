-- Creates a Function that divides and
-- returns 1st number by second number
-- or 0 if denominator is 0
DELIMITER //
CREATE FUNCTION safeDiv (a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
	IF b != 0 THEN
	RETURN a / b;
	END IF;
	RETURN 0;
END//
DELIMITER ;
