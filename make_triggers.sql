use birdbook;



DELIMITER //
CREATE TRIGGER del_per
BEFORE UPDATE ON person
FOR EACH ROW
BEGIN
	IF NEW.is_deleted = 1 THEN
		UPDATE post 
		SET post.deletedAt =  CURDATE()
		WHERE post.person_id =NEW.person_id;
	END IF;
        
END//

DELIMITER ;