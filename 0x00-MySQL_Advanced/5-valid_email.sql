-- Create trigger that changes valid_email at update
-- of email value.

DELIMITER //
CREATE TRIGGER email_val BEFORE UPDATE ON users
	FOR EACH ROW 
	BEGIN
	IF STRCMP(NEW.email, OLD.email) != 0 THEN
		SET NEW.valid_email = 0;
	END IF;
	END;//
DELIMITER ;
