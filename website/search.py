from flask import Blueprint, render_template, jsonify
from .models import Users, Posts, Groups, Profiles
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_login import login_required, current_user
search = Blueprint('search', __name__)


class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")


@search.route("/search", methods=["GET", "POST"])
@login_required
def live_search():
    return render_template("search.html", user=current_user)


@search.route("/searchFor", methods=["GET", "POST"])
@login_required
def search_users():
    users = Users.query.all()
    usersJS = [(user.id, user.username) for user in users]
    profiles = Profiles.query.all()
    profilesJS = [(profile.id, profile.name, profile.profile_pic)
                  for profile in profiles]
    posts = Posts.query.all()
    postJs = [(post.id, post.content) for post in posts]
    groups = Groups.query.all()
    groupJs = [(group.id, group.name, group.profile_pic) for group in groups]
    return jsonify({"users": usersJS, "posts": postJs, "groups": groupJs, "profiles": profilesJS})
