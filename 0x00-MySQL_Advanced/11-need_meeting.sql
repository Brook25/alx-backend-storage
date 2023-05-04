-- Creates a view need_meeting that lists
-- all students with score under 80 and
-- had no meeting for more than a month

-- DROP VIEW need_meeting;
CREATE VIEW need_meeting AS SELECT name FROM students WHERE score < 80 AND 
	(last_meeting IS NULL OR DATEDIFF(CURDATE(), last_meeting) > 30);
