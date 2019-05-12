#The below 2 values are mandatory
INSERT INTO role (name)
VALUES ('admin'),('user');

UPDATE role
SET `default` = 1
WHERE name = 'user';

INSERT INTO content (name,content,page_id,update_date)
VALUES ('content1','test',1,now()),('content1','test',2,now());

INSERT INTO page (name) VALUES ('about'),('contact');
