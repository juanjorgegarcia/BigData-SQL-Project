use birdbook;

CREATE TABLE person_vote_post (
  person_id SMALLINT UNSIGNED NOT NULL,
  post_id SMALLINT UNSIGNED NOT NULL,
  liked SMALLINT SIGNED NOT NULL,
  deletedAt datetime NULL,
  PRIMARY KEY  (person_id, post_id),
  CONSTRAINT fk_person_vote_post_postid FOREIGN KEY (post_id) REFERENCES post (post_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_person_vote_post_personid FOREIGN KEY (person_id) REFERENCES person (person_id) ON DELETE RESTRICT ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE person_comment_post (
  person_id SMALLINT UNSIGNED NOT NULL,
  post_id SMALLINT UNSIGNED NOT NULL,
  comment VARCHAR(255) NOT NULL,
  deletedAt datetime NULL,
  PRIMARY KEY  (person_id, post_id),
  CONSTRAINT fk_person_comment_post_postid FOREIGN KEY (post_id) REFERENCES post (post_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_person_comment_post_personid FOREIGN KEY (person_id) REFERENCES person (person_id) ON DELETE RESTRICT ON UPDATE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;
