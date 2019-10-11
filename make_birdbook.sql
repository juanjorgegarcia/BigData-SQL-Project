DROP SCHEMA IF EXISTS birdbook;
CREATE SCHEMA birdbook;
USE birdbook;


--
-- Table structure for table `person`
--


CREATE TABLE person (
  person_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  username VARCHAR(45) NOT NULL,
  first_name VARCHAR(45) NOT NULL,
  last_name VARCHAR(45) NOT NULL,
  email VARCHAR(255) NOT NULL,
  city VARCHAR(45) NOT NULL,
  PRIMARY KEY  (person_id),
  UNIQUE KEY(username),
  KEY idx_person_username (username)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

DELIMITER ;;
-- CREATE TRIGGER tr_person_del ON person
-- INSTEAD OF DELETE
-- AS
-- BEGIN
--     UPDATE person
--     SET deletedAt = GETDATE()
--     WHERE person_id IN (SELECT person_id FROM deleted)
-- END

-- CREATE TRIGGER tr_post_del ON post
-- INSTEAD OF DELETE
-- AS
-- BEGIN
--     UPDATE post
--     SET deletedAt = GETDATE()
--     WHERE post_id IN (SELECT post_id FROM deleted)
-- END

-- CREATE TRIGGER tr_person_del ON person
-- ON DELETE
-- AS BEGIN
-- 	UPDATE post
--     set deletedAt = "1900-01-01 00:00:00"
--     person INNER JOIN person_make_post USING (person_id)
--     INNER JOIN post USING (post_id)
--     WHERE person_id IN (SELECT person_id FROM deleted)
-- END
CREATE TRIGGER tr_person_del ON person
ON DELETE
AS BEGIN
	UPDATE post
    set deletedAt = "1900-01-01 00:00:00"
    WHERE title LIKE "titulo"
END

DELIMITER ;;

--
-- Table structure for table `bird`
--

CREATE TABLE bird (
  bird_name VARCHAR(45) NOT NULL,
  PRIMARY KEY  (bird_name)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

--
-- Table structure for table `person_favorites_bird`
--

CREATE TABLE person_favorites_bird (
  person_id SMALLINT UNSIGNED NOT NULL,
  bird_name VARCHAR(45) NOT NULL,
  PRIMARY KEY  (person_id,bird_name),
  CONSTRAINT fk_person_favorites_bird_birdname FOREIGN KEY (bird_name) REFERENCES bird (bird_name) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_person_favorites_bird_personid FOREIGN KEY (person_id) REFERENCES person (person_id) ON DELETE RESTRICT ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

--
-- Table structure for table `post`
--

CREATE TABLE post (
  post_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  title VARCHAR(45) NOT NULL,
  url VARCHAR(45) ,
  content VARCHAR(255) NOT NULL,
  deletedAt datetime NULL,
  PRIMARY KEY  (post_id),
  KEY idx_post_title (title)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE person_make_post (
  person_id SMALLINT UNSIGNED NOT NULL,
  post_id SMALLINT UNSIGNED NOT NULL,
  PRIMARY KEY  (person_id, post_id),
  CONSTRAINT fk_person_make_post_postid FOREIGN KEY (post_id) REFERENCES post (post_id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_person_make_post_personid FOREIGN KEY (person_id) REFERENCES person (person_id) ON DELETE CASCADE ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;




CREATE TABLE post_refere_person (
  post_id SMALLINT UNSIGNED NOT NULL,
  person_id SMALLINT UNSIGNED NOT NULL,
  PRIMARY KEY  (post_id, person_id),
  CONSTRAINT fk_post_refere_person_personid FOREIGN KEY (person_id) REFERENCES person (person_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_post_refere_person_postid FOREIGN KEY (post_id) REFERENCES post (post_id) ON DELETE RESTRICT ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE person_view_post (
  person_id SMALLINT UNSIGNED NOT NULL,
  post_id SMALLINT UNSIGNED NOT NULL,
  ip INT UNSIGNED NOT NULL,
  device VARCHAR(45) NOT NULL,
  browser VARCHAR(45) NOT NULL,
  instant TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY  (person_id, post_id),
  CONSTRAINT fk_person_view_post_postid FOREIGN KEY (post_id) REFERENCES post (post_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_person_view_post_personid FOREIGN KEY (person_id) REFERENCES person (person_id) ON DELETE RESTRICT ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE post_refere_bird (
  post_id SMALLINT UNSIGNED NOT NULL,
  bird_name VARCHAR(45) NOT NULL,
  PRIMARY KEY  (post_id, bird_name),
  CONSTRAINT fk_post_refere_bird_postid FOREIGN KEY (post_id) REFERENCES post (post_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_post_refere_bird_birdname FOREIGN KEY (bird_name) REFERENCES bird (bird_name) ON DELETE RESTRICT ON UPDATE CASCADE
  
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;