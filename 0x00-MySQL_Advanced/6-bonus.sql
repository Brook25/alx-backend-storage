-- Creates a procedure that adds corrections to
-- a table based on rows from two other tables

DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER //
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name varchar(255), IN score INT)
BEGIN
        DECLARE pr_id INT;
        SELECT id FROM projects WHERE name = project_name INTO pr_id;
        IF pr_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, (SELECT id FROM projects WHERE name = project_name), score);
        ELSE
        INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, pr_id, score);
        END IF;
END//
DELIMITER ;

