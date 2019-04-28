from app import app, db, login
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from hashlib import md5
from sqlalchemy.ext.hybrid import hybrid_method
from bs4 import BeautifulSoup

import jwt

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), index=True, unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='commenter', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    last_seen = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

    # override constructor so we can assign default role to user
    def __init__(self,**kwargs):
        # also call parent constructor
        super(User, self).__init__(**kwargs)
        self.role = Role.query.filter_by(default=True).first()

    # generate hash of given password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # return hash of given password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=monsterid&s={}'.format(digest, size)

    # return true if user is admin, false otherwise
    def is_admin(self):
        return self.role.name == 'admin'

    # creates token of user object
    # decode('utf-8') converts token to string
    def get_reset_password_token(self, expires_in=app.config['FORGOT_PASSWORD_TOKEN_EXPIRE']):
        return jwt.encode(
            {'reset_password': self.id, 'exp': datetime.utcnow() + timedelta(seconds=expires_in)},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    # decodes token and returns user object
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.email)

# This allows application to freely call these methods even if you're not logged in
class AnonymousUser(AnonymousUserMixin):
    def set_password(self, password):
        return False
    def check_password(self, password):
        return False
    def avatar(self, size):
        return False
    def is_admin(self):
        return False
    def get_reset_password_token(self, expires_in=app.config['FORGOT_PASSWORD_TOKEN_EXPIRE']):
        return False
# This tells flask login which class to use if user is not logged in
login.anonymous_user = AnonymousUser

class Role(db.Model):
    __tablename__='role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    # only one role must be set to true, we use this role as the default role
    default = db.Column(db.Boolean, default=False, index=True, nullable=False)
    users = db.relationship('User',backref='role',lazy='dynamic')

class Tagged(db.Model):
    __tablename__ = 'tagged'
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'),primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'),primary_key=True)

class Post(db.Model):
    __tablename__='post'

    id = db.Column(db.Integer, primary_key=True)
    heading = db.Column(db.String(100), nullable=False)
    post = db.Column(db.String(2000), nullable=False)
    current = db.Column(db.Boolean, default=True, index=True, nullable=False)
    update_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #joined means all rows returned
    #dynamic means return query objects instead of items so you can use filter
    #cascade delete-orphan means if student object is deleted then association table row is also deleted
    tags = db.relationship('Tagged',foreign_keys=[Tagged.post_id], \
                                    backref=db.backref('posts',lazy='joined'),
                                    lazy='dynamic',
                                    cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def getPost(id):
        return Post.query.filter(Post.id==id).first()

    #return a list of tag names for this post
    def getTagNames(self):
        tags = Tag.query.filter(Tag.posts.any(post_id=self.id)).all()
        return [tag.name for tag in tags]

    #return a string of tag names for this post
    def getTagNamesStr(self):
        return ','.join(self.getTagNames())


    # helper function for search
    def is_txtinHTML(self, str_compare):
        soup = BeautifulSoup(self.post).get_text()
        if soup.count(str_compare) > 0:
            return True
        else:
            return False

    # used for search to return the number of occurrences of string
    @hybrid_method
    def occurrences(self, str_compare):
        # use beautifulsoup to only count text not html
        soup = BeautifulSoup(self.post).get_text()
        return (soup.count(str_compare))

    def __repr__(self):
        return '<Post {}>'.format(self.heading)


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    update_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)
    #joined means all rows returned
    #dynamic means return query objects instead of items so you can use filter
    #cascade delete-orphan means if student object is deleted then association table row is also deleted
    posts = db.relationship('Tagged',foreign_keys=[Tagged.tag_id], \
                                    backref=db.backref('tags',lazy='joined'),
                                    lazy='dynamic',
                                    cascade='all, delete-orphan')

    #return tag id given tag name. Return -1 if not found
    def getTagId(tag_name):
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag is None:
            return -1
        else:
            return tag.id

    def getTag(tag_id):
        return Tag.query.filter_by(id=tag_id).first()

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(200), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    # user can either comment as anonymous user or with a registered account
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    name = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(400), nullable=False)
    create_date = db.Column(db.DateTime,default=datetime.utcnow, nullable=False)

# Used by flask-login
# This callback is used to reload the user object from the user ID stored in the session
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)
