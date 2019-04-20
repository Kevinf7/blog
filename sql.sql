#The below 2 values are mandatory
INSERT INTO Role (name)
VALUES ('admin'),('user');

UPDATE Role
SET `default` = 1
WHERE name = 'user'
