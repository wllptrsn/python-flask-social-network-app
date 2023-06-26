from . import db
from flask_login import UserMixin
from datetime import datetime
from flask_wtf.file import FileField


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_username = db.Column(db.String)
    recipient_username = db.Column(db.String)
    date = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow)
    content = db.Column(db.String)


class Follows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    follower_username = db.Column(db.String)
    followed_username = db.Column(db.String)
    recipient_username = db.Column(db.String)


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    posts = db.relationship('Posts', backref='user', passive_deletes=True)
    messages = db.relationship("Messages", foreign_keys=[Messages.user_id])
    recipient_messages = db.relationship(
        "Messages", foreign_keys=[Messages.recipient_id])

    interests = db.relationship('Interests')
    admin_group = db.relationship('Groups')
    profiles = db.relationship('Profiles')
    users_interests = db.relationship(
        'UsersInterests', backref='user', passive_deletes=True)
    postComments = db.relationship(
        'PostComments', backref='user', passive_deletes=True)
    feed = db.relationship('Feed')
    likes = db.relationship('Likes', backref='user', passive_deletes=True)
    groups = db.relationship(
        'UsersGroups', backref='user', passive_deletes=True)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.Integer)
    content = db.Column(db.String(10000))
    type = db.Column(db.String(20))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    feed = db.relationship('Feed')
    postComments = db.relationship(
        'PostComments', backref='post', passive_deletes=True)
    likes = db.relationship('Likes', backref='post', passive_deletes=True)


class PostComments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', ondelete="CASCADE"), nullable=False)


class Interests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    description = db.Column(db.String)
    icon = db.Column(db.String)
    users_interests = db.relationship('UsersInterests')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String())
    profile_pic = db.Column(db.String(120), default='image.jpg')
    cover_photo = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True)
    details = db.Column(db.String(1000))
    date_created = db.Column(db.DateTime(timezone=True), default=datetime.now)
    profile_pic = db.Column(db.String(120), default='image.jpg')
    cover_photo = db.Column(db.String())
    posts = db.relationship('Posts')
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    users = db.relationship(
        'UsersGroups', backref='group', passive_deletes=True)


class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.Integer)
    date_created = db.Column(
        db.DateTime(timezone=True), default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))


class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id', ondelete="CASCADE"), nullable=False)


class UsersGroups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey(
        'groups.id', ondelete="CASCADE"), nullable=False)


class UsersInterests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    interest_id = db.Column(db.Integer, db.ForeignKey('interests.id'))
