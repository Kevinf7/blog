#The below 2 values are mandatory
INSERT INTO role (name)
VALUES ('admin'),('user');

UPDATE role
SET `default` = 1
WHERE name = 'user';
