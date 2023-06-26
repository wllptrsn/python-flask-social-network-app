from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash,  jsonify
from .models import Users, Posts, PostComments, Groups, Likes, Follows
from . import db
from flask_login import login_required, current_user
from sqlalchemy import desc
import json

# A blueprint of an application means that it stores your urls
posts = Blueprint('posts', __name__)


@posts.route("/")
@posts.route("/home")
def home():
    posts = Posts.query.order_by(desc(Posts.date)).all()
    groups = Groups.query.all()
    return render_template("feed.html", user=current_user, posts=posts, groups=groups)


@posts.route('/createPost', methods=['GET', 'POST'])
@login_required
def createPost():
    following = Follows.query.filter_by(follower_id=current_user.id).all()

    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            flash('Post cannot be empty', category='error')
        else:
            newPost = Posts(user_id=current_user.id, content=content)
            db.session.add(newPost)
            db.session.commit()
            return redirect(url_for('posts.home'))
        return redirect(url_for('posts.createPost'))
    return render_template("createPost.html", user=current_user, following=following)


@posts.route('delete_post', methods=['POST'])
def delete_Post():
    # this function expects a JSON from the INDEX.js file
    posts = json.loads(request.data)
    PostId = posts['PostId']
    posts = Posts.query.get(PostId)
    if posts:
        if posts.user_id == current_user.id:
            db.session.delete(posts)
            db.session.commit()

    return jsonify({})


@posts.route("/posts/<username>")
@login_required
def userPosts(username):
    user = Users.query.filter_by(username=username).first()

    if not user:
        flash('No user with that username exists.', category='error')
        return redirect(url_for('posts.home'))

    posts = user.posts
    return render_template("posts.html", user=current_user, posts=posts, username=username)


@posts.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    content = request.form.get('content')

    if not content:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Posts.query.filter_by(id=post_id)
        if post:
            comment = PostComments(
                content=content, user_id=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('posts.home'))


@posts.route("/like-post/<post_id>", methods=['POST'])
@login_required
def like(post_id):
    post = Posts.query.filter_by(id=post_id).first()
    like = Likes.query.filter_by(
        author=current_user.id, post_id=post_id).first()
    if not post:
        return jsonify({'error': 'Post does not exist.'}, 400)
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Likes(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()

    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})


@posts.route('delete_post_comment', methods=['POST'])
def delete_Post_Comment():
    # this function expects a JSON from the INDEX.js file
    comments = json.loads(request.data)
    CommentId = comments['CommentId']
    comments = PostComments.query.get(CommentId)
    if comments:
        db.session.delete(comments)
        db.session.commit()

    return jsonify({})
