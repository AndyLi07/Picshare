CREATE TRIGGER `PhotoShare`.`Duplicate_Album_Name` BEFORE INSERT ON `Album` FOR EACH ROW
BEGIN
	IF EXISTS (SELECT A.album_id FROM Album A WHERE A.owner_id = NEW.owner_id AND A.album_name = NEW.album_name)
    THEN SIGNAL SQLSTATE '45000' set message_text = "Cannot have duplicate album names.";
    END IF;
END

CREATE TRIGGER `selfComment` BEFORE INSERT ON `Comments` 
FOR EACH ROW
BEGIN
	IF ((SELECT A.owner_id FROM Album A, Photo P WHERE NEW.photo_id = P.photo_id AND P.album_id = A.album_id) = NEW.owner_id)
    THEN SIGNAL SQLSTATE '45000' set message_text = 'Cannot comment on your own photo';
    END IF;
END