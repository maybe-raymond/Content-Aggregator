from blitz import db
from datetime import datetime
from blitz import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key= True)
    Username =db.Column(db.String(25), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default="cover.jpg")
    comments = db.relationship("Comment", backref="comments", lazy="dynamic")
    following = db.relationship("Followers", backref="following", lazy="dynamic")


    def __repr__(self):
        return f"User('{self.username}', '{self.Email}', '{self.posts}')"

class Article(db.Model):
    __tablename__ ="Article"

    id = db.Column(db.Integer, primary_key= True)
    title = db.Column(db.String(200), nullable=False)
    source = db.Column(db.String(200), nullable=False)
    link =  db.Column(db.String(200), nullable=False, unique=True)
    summary = db.Column(db.Text, nullable=False)
    date =db.Column(db.DateTime, nullable=False, default= datetime.utcnow())
    image_src = db.Column(db.String(200), nullable=False)
    comments = db.relationship("Comment", backref="Comments", lazy="dynamic")
    follower = db.relationship("Followers", backref="follower", lazy="dynamic")

    def __repr__(self):
        return f"Article('{self.title}','{self.source}', '{self.link}', '{self.summary}')"

class Exchange_rate(db.Model):
    __tablename__ ="Exchange rate"

    id =  db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(200), nullable=False)
    rtgs = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default= datetime.utcnow())

    def __repr__(self):
        return f"Exchange_rate('{self.rtgs}','{self.name}', '{self.date}')"

class Covid(db.Model):
    __tablename__ ="Covid"

    id =  db.Column(db.Integer, primary_key= True)
    cases = db.Column(db.Integer, nullable=False)
    death =  db.Column(db.Integer, nullable=False)
    recovery = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default= datetime.utcnow())

    def __repr__(self):
            return f"Covid('{self.cases}', '{self.death}', '{self.recovery}')"



class Comment(db.Model):
    __tablename__ ="Comment"

    id =  db.Column(db.Integer, primary_key= True)
    content = db.Column(db.Text, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey("User.id"))
    article_post = db.Column(db.Integer, db.ForeignKey("Article.id"))
    date_posted=db.Column(db.DateTime, nullable=False, default= datetime.utcnow())

    def __repr__(self):
            return f"Comment('{self.content}', '{self.user}', '{self.article_post}')"


class Followers(db.Model):
    __tablename__ ="Followers"

    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    article_source = db.Column(db.String, db.ForeignKey("Article.source"))

    def __repr__(self):
        return f"Followers('{self.id}','{self.user_id}', '{self.article_source}')"
