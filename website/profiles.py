import json
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, current_app
from .models import Users, Interests, UsersInterests, Profiles, Follows
from . import db
from flask_login import login_required, current_user
# A blueprint of an application means that it stores your urls
from sqlalchemy import desc
import os
import secrets
import uuid as uuid
profiles = Blueprint('profiles', __name__)


def save_image(photo):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extension = os.path.splitext(photo.filename)
    photo_name = hash_photo + file_extension
    file_path = os.path.join(current_app.root_path, 'static/img', photo_name)
    photo.save(file_path)
    return photo_name


@profiles.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("feed.html", user=current_user)


@profiles.route('/create_profile', methods=['GET', 'POST'])
@login_required
def createProfile():
    if request.method == 'POST':
        description = request.form.get('description')
        profile_pic = save_image(request.files.get('profile_pic'))
        profile = Profiles(description=description,
                           profile_pic=profile_pic, name=current_user.username, user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
        return redirect(url_for('profiles.show_interests', user=current_user))
    return render_template("createProfile.html", user=current_user)


@profiles.route('/account_settings', methods=['GET', 'POST'])
@login_required
def accountSettings():
    account = Profiles.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        account.profile_pic = save_image(request.files.get('profile_pic'))
        account.description = request.form['description']
        account.name = request.form['username']
        try:
            db.session.commit()
            return redirect(url_for('profiles.posts', username=current_user.username))
        except:
            return "You Suck!"
    return render_template("accountSettings.html", user=current_user)


@profiles.route('/add_interest', methods=['GET', 'POST'])
@login_required
def add_interest():
    interests = json.loads(request.data)
    InterestId = interests['InterestId']
    interests = Interests.query.get(InterestId)

    usersInterests = UsersInterests.query.filter_by(
        interest_id=InterestId, user_id=current_user.id).first()

    if usersInterests:
        db.session.delete(usersInterests)
        db.session.commit()
    else:
        new_user_interest = UsersInterests(
            user_id=current_user.id, interest_id=InterestId)
        db.session.add(new_user_interest)
        db.session.commit()
    return jsonify({})


@profiles.route('choose_interests', methods=['GET', 'POST'])
def show_interests():
    interests = Interests.query.order_by(Interests.id).all()
    userInterests = UsersInterests.query.order_by(UsersInterests.id).all()
    if request.method == 'POST':
        return redirect(url_for('posts.home'))
    return render_template("interests.html", interests=interests, userInterests=userInterests, user=current_user)


@profiles.route("/users/<username>", methods=['GET', 'POST', 'DELETE'])
def posts(username):
    account = Users.query.filter_by(username=username).first()
    profile = Profiles.query.filter_by(user_id=account.id).first()
    user_follows = Follows.query.filter_by(
        follower_id=current_user.id, followed_id=account.id).first()

    if not account:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('profiles.home'))

    posts = account.posts
    return render_template("users.html", user=current_user, posts=posts, account=account, profile=profile, username=username, user_follows=user_follows)


@profiles.route("/follow/<username>", methods=['GET',])
@login_required
def follow(username):
    account = Users.query.filter_by(username=username).first()
    user_follows = Follows.query.filter_by(
        follower_id=current_user.id, followed_id=account.id).first()
    if user_follows:
        db.session.delete(user_follows)
        db.session.commit()
    else:
        follows = Follows(follower_id=current_user.id, followed_id=account.id,
                          follower_username=current_user.username,
                          followed_username=account.username)
        db.session.add(follows)
        db.session.commit()
    return redirect(url_for('profiles.posts', username=username))


@profiles.route("/followers_page", methods=['GET'])
@login_required
def followerPage():
    return redirect(url_for('profiles.showFollowers'))


@profiles.route("/show_followers", methods=['GET'])
@login_required
def showFollowers():
    followers = Follows.query.filter_by(followed_id=current_user.id).all()
    accounts = Users.query.all()
    return render_template("showFollowers.html", followers=followers, user=current_user, accounts=accounts)


@profiles.route("/show_following", methods=['GET'])
@login_required
def showFollowing():
    following = Follows.query.filter_by(follower_id=current_user.id).all()
    accounts = Users.query.all()
    return render_template("showFollowing.html", following=following, user=current_user, accounts=accounts)
