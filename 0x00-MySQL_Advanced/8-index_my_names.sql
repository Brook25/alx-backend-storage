-- Creates an index based on the first letter of the name
-- from table names

CREATE INDEX idx_name_first ON names (name(1));
