from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import desc
from flask_login import login_required, current_user
from . import db
from .models import Groups, Posts, UsersGroups
from .profiles import save_image
import uuid as uuid
# A blueprint of an application means that it stores your urls
groups = Blueprint('groups', __name__)


@groups.route('/groups')
@login_required
def show_groups():
    group_users = UsersGroups.query.all()
    discover = Groups.query.all()
    return render_template("groups.html", user=current_user, group_users=group_users, discover=discover)

@groups.route('/createGroup', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method == 'POST':
        name = request.form.get('name')
        profile_pic = save_image(request.files.get('profile_pic'))
        details = request.form.get('details')
        group = Groups(name=name, details=details, admin_id=current_user.id,
                           profile_pic=profile_pic)
        db.session.add(group)
        db.session.commit()
        return redirect(url_for('groups.group_id', groupname=name))
    return render_template("createGroup.html", user=current_user)

@groups.route('/editGroup/<groupid>', methods=['GET', 'POST'])
@login_required
def edit_group(groupid):
    group = Groups.query.filter_by(id=groupid).first()
    if request.method == 'POST':
        group.name = request.form['name']
        group.details = request.form['details']
        db.session.commit()
        return redirect(url_for('groups.group_id', groupname=group.name))
    return render_template("editGroup.html", groupid=group.id, user=current_user)


@groups.route('/deleteGroup/<groupid>', methods=['GET', 'POST'])
@login_required
def delete_group(groupid):
    group = Groups.query.filter_by(id=groupid).first()
    if request.method == 'POST':
        if group:
            db.session.delete(group)
            db.session.commit()
            return redirect(url_for('groups.show_groups'))
        else:
            flash('Group does not exist.', category='error')
    return render_template('deleteGroup.html', groupid=group.id, user=current_user)


@groups.route("/groups/<groupname>", methods=['GET', 'POST'])
def group_id(groupname):
    group = Groups.query.filter_by(name=groupname).first()
    if group.admin_id == current_user.id:
        posts = Posts.query.filter_by(
            group_id=group.id).order_by(desc(Posts.date)).all()
    content = request.form.get('content')
    if not group:
        flash('No group with that name exists.', category='error')
        return redirect(url_for('groups.create_group'))
        
    if request.method == 'POST':
        if not content:
            flash('Comment cannot be empty.', category='error')
        else:
            group_post = Posts(user_id=current_user.id,
                              content=content, group_id=group.id)
            db.session.add(group_post)
            db.session.commit()
            return redirect(url_for('groups.group_id', groupname=groupname))
    return render_template("groupPage.html", user=current_user, group=group, posts=posts)


@groups.route("/join-group/<groupid>", methods=['POST'])
@login_required
def join(groupid):
    group = Groups.query.filter_by(id=groupid).first()
    group_users = UsersGroups.query.filter_by(
        group_id=groupid, user_id=current_user.id).first()

    if not group:
        return jsonify({'error': 'Group does not exist.'}, 400)
    elif group_users:
        db.session.delete(group_users)
        db.session.commit()
    else:
        group_users = UsersGroups(group_id=groupid, user_id=current_user.id)
        db.session.add(group_users)
        db.session.commit()
    return jsonify({"members": len(group.users), "joined": current_user.id in map(lambda x: x.user_id, group.users)})
