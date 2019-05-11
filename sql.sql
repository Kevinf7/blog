#The below 2 values are mandatory
INSERT INTO role (name)
VALUES ('admin'),('user');

UPDATE role
SET `default` = 1
WHERE name = 'user';

INSERT INTO page (name,content,page_id,update_date)
VALUES ('content1','test',7,now()),('content1','test',8,now()),('content1','test',9,now());

INSERT INTO content (name,update_date)
VALUES ('main',now()),('about',now()),('contact',now());
