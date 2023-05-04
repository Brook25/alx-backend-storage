-- Creates a procedure that does
-- weighted avarage for every user in  a table\

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (IN usr_id INT)
BEGIN
	DECLARE wgt_tot INT;
        SET wgt_tot = (SELECT SUM(weight) FROM projects);
        UPDATE users SET average_score = ((SELECT SUM(weight * score)
	FROM projects INNER JOIN corrections ON projects.id = corrections.project_id 
	WHERE user_id = usr_id) / wgt_tot) WHERE id = usr_id;
END//


DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers//
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	DECLARE max_id INT;
	DECLARE x INT;
	SET max_id = (SELECT MAX(id) FROM users);
	SET x = 1;
	WHILE x <= max_id
	DO CALL ComputeAverageWeightedScoreForUser(x);
	SET x = x + 1;
	END WHILE;
END//
DELIMITER ;
