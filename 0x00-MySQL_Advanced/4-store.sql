-- Creates a trigger that updates another table
-- based on the changes on the current table

CREATE TRIGGER upd_items AFTER INSERT ON orders FOR EACH ROW
	UPDATE items SET quantity = quantity - NEW.number WHERE name = NEW.item_name; 
