CREATE DATABASE `PhotoShare`;
USE `PhotoShare`;

DROP TABLE IF EXISTS `Friendship` CASCADE;
DROP TABLE IF EXISTS `Photo_Tag` CASCADE;
DROP TABLE IF EXISTS `Comments` CASCADE;
DROP TABLE IF EXISTS `Likes` CASCADE;
DROP TABLE IF EXISTS `Tag` CASCADE;
DROP TABLE IF EXISTS `Photo` CASCADE;
DROP TABLE IF EXISTS `Album` CASCADE;
DROP TABLE IF EXISTS `Users` CASCADE;

CREATE TABLE `Users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `date_of_birth` date NOT NULL,
  `email` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `gender` char(1) DEFAULT NULL,
  `hometown` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
);

INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Anonymous', '', '1900-01-01', '0000@Photoshare.com', 'Anonymous', NULL, NULL);
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Ang', 'Li', '1993-02-07', 'angli@gmail.com', 'password', 'M', 'BOS');
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Jim', 'Hunt', '1989-01-11', 'jh@gmail.com', 'password', 'M', NULL);
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Ryan', 'Peterson', '1991-02-20', 'rpet@gmail.com', 'password', NULL, 'Boston');
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Yisong', 'Yue', '1989-01-11', 'yyue@gmail.com', 'password', 'F', 'Seoul');
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Kristel', 'Keegan', '1993-03-15', 'kkeegan@gmail.com', 'password', 'F', 'Charles Town');
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Scott', 'Tucker', '1989-04-08', 'stucker@gmail.com', 'password', 'M', NULL);
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Paris', 'Hilton', '1991-04-10', 'philton@gmail.com', 'password', NULL, NULL);
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Bob', 'Saget', '1989-04-30', 'bsa@gmail.com', 'password', 'M', 'Pittsburgh');
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Albert', 'Weinstein', '1993-06-07', 'aws@gmail.com', 'password', 'M', 'Rockport');
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Freddy', 'Mercury', '1992-07-26', 'fmer@gmail.com', 'password', 'F', NULL);
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Edward', 'Scissorhands', '1991-08-22', 'ecissor@gmail.com', 'password', NULL, NULL);
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Ezra', 'Cornell', '1993-08-23', 'ecornell@gmail.com', 'password', 'M', NULL);
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Britney', 'Spears', '1992-10-18', 'bs@gmail.com', 'password', NULL, NULL);
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Michael', 'Luo', '1987-10-30', 'mluo@gmail.com', 'password', NULL, NULL);
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Regan', 'Morris', '1988-11-07', 'rmo@gmail.com', 'password', NULL, NULL);
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Lisa', 'Woods', '1989-10-07', 'lwoods@gmail.com', 'password', 'M', NULL);
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Michelle', 'Faul', '1990-11-08', 'mfaul@gmail.com', 'password', NULL, NULL);
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('David', 'Johnston', '1989-12-19', 'djson@gmail.com', 'password', NULL, NULL);
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Laura', 'Holson', '1993-12-24', 'lhol@gmail.com', 'password', NULL, NULL);
INSERT INTO `PhotoShare`.`Users`(`first_name`,`last_name`,`date_of_birth`,`email`,`password`,`gender`,`hometown`) VALUES ('Kim', 'Dixon', '1990-11-17', 'kdixon@gmail.com', 'password', 'M', NULL);

CREATE TABLE `Friendship` (
  `from_user_id` int(11) NOT NULL,
  `to_user_id` int(11) NOT NULL,
  PRIMARY KEY (`from_user_id`,`to_user_id`),
  CONSTRAINT `from_user_id` FOREIGN KEY (`from_user_id`) REFERENCES `Users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `to_user_id` FOREIGN KEY (`to_user_id`) REFERENCES `Users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('2','3');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('2','4');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('2','5');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('2','6');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('2','7');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('2','8');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('3','5');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('3','17');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('3','7');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('3','12');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('3','15');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('3','10');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('4','12');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('5','8');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('5','2');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('5','4');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('5','18');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('5','13');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('6','5');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('7','6');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('7','13');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('7','18');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('8','2');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('8','9');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('9','7');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('9','12');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('10','11');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('10','14');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('10','12');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('11','8');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('11','2');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('12','4');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('13','18');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('13','13');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('14','15');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('15','16');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('14','17');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('14','18');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('14','3');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('14','2');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('15','7');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('16','8');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('16','9');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('17','20');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('17','16');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('18','4');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('18','3');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('19','14');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('20','21');
INSERT INTO `PhotoShare`.`Friendship`(`from_user_id`,`to_user_id`) VALUES ('21','3');

CREATE TABLE `Album` (
  `album_id` int(11) NOT NULL AUTO_INCREMENT,
  `album_name` varchar(45) DEFAULT 'Unknown',
  `owner_id` int(11) NOT NULL,
  `date_created` date DEFAULT NULL,
  PRIMARY KEY (`album_id`),
  CONSTRAINT `owner_id` FOREIGN KEY (`owner_id`) REFERENCES `Users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
); 

INSERT INTO `PhotoShare`.`Album`(`album_name`,`owner_id`,`date_created`) VALUES ('ang_alb1','2','2016-10-30');
INSERT INTO `PhotoShare`.`Album`(`album_name`,`owner_id`,`date_created`) VALUES ('jim_alb1','3','2016-10-30');
INSERT INTO `PhotoShare`.`Album`(`album_name`,`owner_id`,`date_created`) VALUES ('ryan_alb1','4','2016-10-30');
INSERT INTO `PhotoShare`.`Album`(`album_name`,`owner_id`,`date_created`) VALUES ('ang_alb2','2','2016-10-30');
INSERT INTO `PhotoShare`.`Album`(`album_name`,`owner_id`,`date_created`) VALUES ('kk_alb1','6','2016-10-30');
INSERT INTO `PhotoShare`.`Album`(`album_name`,`owner_id`,`date_created`) VALUES ('hilton_alb1','8','2016-10-30');
INSERT INTO `PhotoShare`.`Album`(`album_name`,`owner_id`,`date_created`) VALUES ('albert_alb1','10','2016-10-30');
INSERT INTO `PhotoShare`.`Album`(`album_name`,`owner_id`,`date_created`) VALUES ('fm_alb1','11','2016-10-30');
INSERT INTO `PhotoShare`.`Album`(`album_name`,`owner_id`,`date_created`) VALUES ('luo_alb1','15','2016-10-30');
INSERT INTO `PhotoShare`.`Album`(`album_name`,`owner_id`,`date_created`) VALUES ('luo_alb2','15','2016-10-30');
INSERT INTO `PhotoShare`.`Album`(`album_name`,`owner_id`,`date_created`) VALUES ('lisa_alb1','17','2016-10-30');
INSERT INTO `PhotoShare`.`Album`(`album_name`,`owner_id`,`date_created`) VALUES ('laura_alb1','20','2016-10-30');

CREATE TABLE `Photo` (
  `photo_id` int(11) NOT NULL AUTO_INCREMENT,
  `caption` varchar(45) NOT NULL,
  `imgdata` longblob,
  `album_id` int(11) NOT NULL,
  PRIMARY KEY (`photo_id`),
  CONSTRAINT `album_id` FOREIGN KEY (`album_id`) REFERENCES `Album` (`album_id`) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE `Tag` (
  `tag_id` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(45) NOT NULL,
  PRIMARY KEY (`tag_id`),
  UNIQUE KEY `word_UNIQUE` (`word`)
);

INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('friend');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('friends');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('friendship');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('dogs');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('puppy');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('cute');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('pets');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('boston');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('BOS');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('food');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('taste');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('restaurantweek');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('foodie');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('steak');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('italian');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('love');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('flower');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('garden');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('plant');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('outdoor');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('people');
INSERT INTO `PhotoShare`.`Tag`(`word`) VALUES ('artistic');

CREATE TABLE `Photo_Tag` (
  `photo_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`photo_id`,`tag_id`),
  CONSTRAINT `photo_id` FOREIGN KEY (`photo_id`) REFERENCES `Photo` (`photo_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tag_id` FOREIGN KEY (`tag_id`) REFERENCES `Tag` (`tag_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `Comments` (
  `comment_id` int(11) NOT NULL AUTO_INCREMENT,
  `texts` varchar(45) DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `date_created` date DEFAULT NULL,
  `photo_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`comment_id`),
  CONSTRAINT `comment_owner_id` FOREIGN KEY (`owner_id`) REFERENCES `Users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `comment_photo_id` FOREIGN KEY (`photo_id`) REFERENCES `Photo` (`photo_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE `Likes` (
  `photo_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`photo_id`,`user_id`),
  CONSTRAINT `likes_photo_id` FOREIGN KEY (`photo_id`) REFERENCES `Photo` (`photo_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `likes_user_id` FOREIGN KEY (`user_id`) REFERENCES `Users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
);
