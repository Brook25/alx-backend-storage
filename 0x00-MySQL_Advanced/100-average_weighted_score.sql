-- Creates a procedure that
-- calculates weighted avarage of scores

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
DELIMITER ;
