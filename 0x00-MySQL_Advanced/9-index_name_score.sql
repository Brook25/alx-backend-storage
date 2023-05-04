-- Creates index with two columns from
-- table names with first letter of name and score

CREATE INDEX idx_name_first_score ON names (name(1), score);
