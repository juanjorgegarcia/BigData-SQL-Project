use birdbook;

DELIMITER //
CREATE TRIGGER del_per_post
BEFORE UPDATE ON person
FOR EACH ROW
BEGIN
	IF NEW.is_deleted = 1 THEN
		UPDATE post 
		SET post.deletedAt =  CURDATE()
		WHERE post.person_id =NEW.person_id;
        
		UPDATE person_view_post
		SET person_view_post.deletedAt =  CURDATE()
		WHERE person_view_post.person_id =NEW.person_id;
        
		UPDATE person_comment_post
		SET person_comment_post.deletedAt =  CURDATE()
		WHERE person_comment_post.person_id =NEW.person_id;
        
		UPDATE person_vote_post
		SET person_vote_post.deletedAt =  CURDATE()
		WHERE person_vote_post.person_id =NEW.person_id;
        
	END IF;
        
END//

DELIMITER ;


DELIMITER //
CREATE TRIGGER del_per_refere_per
BEFORE UPDATE ON person
FOR EACH ROW
BEGIN
	IF NEW.is_deleted = 1 THEN
		UPDATE post_refere_person
		SET post_refere_person.deletedAt =  CURDATE()
		WHERE post_refere_person.person_id =NEW.person_id;
	END IF;
        
END//

DELIMITER ;




DELIMITER //
CREATE TRIGGER del_per_view_post
BEFORE UPDATE ON person
FOR EACH ROW
BEGIN
	IF NEW.is_deleted = 1 THEN
		UPDATE person_view_post
		SET person_view_post.deletedAt =  CURDATE()
		WHERE person_view_post.person_id =NEW.person_id;
	END IF;
        
END//


DELIMITER ;

DELIMITER //
CREATE TRIGGER del_post_references
BEFORE UPDATE ON post
FOR EACH ROW
BEGIN
	IF NEW.deletedAt IS NOT NULL THEN
		UPDATE post_refere_bird
		SET post_refere_bird.deletedAt =  CURDATE()
		WHERE post_refere_bird.post_id=NEW.post_id;
        
		UPDATE post_refere_person
		SET post_refere_person.deletedAt =  CURDATE()
		WHERE post_refere_person.post_id=NEW.post_id;
	END IF;
        
END//

DELIMITER ;




