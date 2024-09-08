#The below 2 values are mandatory
INSERT INTO role (name)
VALUES ('admin'),('user');

UPDATE role
SET `default` = 1
WHERE name = 'user';

INSERT INTO content (name,content,page_id,update_date)
VALUES ('content1','test',1,now()),('content1','test',2,now());

INSERT INTO page (name) VALUES ('about'),('contact');

INSERT INTO role (name, `default`)
VALUES ('special',0);

INSERT INTO user
    (email, role_id, last_seen,create_date, firstname, lastname)
VALUES
    ('mfoong109@gmail.com',3, now(),now(),'Michael', 'Foong');

from app import db
from app.models import User
u = User.query.filter_by(email='kevin_foong@yahoo.com').first()
u.set_password('abc')
db.session.add(u)
db.session.commit()

insert into page(name) value('special');

INSERT INTO content (name,content,page_id,update_date)
VALUES ('content1','<h1>Hiya Mikey!</h1>',11,now());
