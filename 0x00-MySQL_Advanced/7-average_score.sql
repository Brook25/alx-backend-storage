-- Creates a procedure that computes and
-- stores the average score of a student

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN usr_id INT)
BEGIN
        UPDATE users SET average_score = (SELECT AVG(score) FROM corrections WHERE user_id = usr_id) WHERE id = usr_id;
END//
DELIMITER ;
