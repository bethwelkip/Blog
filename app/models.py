from . import db, login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255)) 
    logged_in = db.Column(db.Boolean)
    blogs = db.relationship('Blog',backref = 'user',lazy="dynamic")
    def __repr__(self):
        return f'{self.username}'

    def get_id(self):
           return (self.user_id)

    # @property
    # def password(self):
    #     raise AttributeError('You cannot read the password attribute')
    
    # @password.setter
    # def password_hash(self, password):
    #     self.password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password,password)

class Blog(UserMixin, db.Model):
    __tablename__ = 'blogs'
    blog_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    blog = db.Column(db.String())
    date = db.Column(db.DateTime())
    user_id = db.Column(db.Integer,db.ForeignKey('users.user_id'))
    blogs = db.relationship('Comment',backref = 'blog',lazy="dynamic")
    def __repr__(self):
        return f'{self.title}'
class Comment(UserMixin, db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key = True)
    comment = db.Column(db.String())
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.blog_id'))
    def __repr__(self):
        return f'{self.comment}'

class Subscriber(db.Model):
    __tablename__ = 'subscribers'
    subscriber_id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String())
    name = db.Column(db.String())
    def __repr__(self):
        return f'{self.name}'