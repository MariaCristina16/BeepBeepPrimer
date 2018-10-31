from flask import Blueprint, redirect, render_template, request, flash
from flask_login import login_required, current_user, logout_user
from monolith.database import db, User, Run
from monolith.auth import admin_required
from monolith.forms import UserForm, DeleteForm


users = Blueprint('users', __name__)


@users.route('/users')
def _users():
    users = db.session.query(User)
    return render_template("users.html", users=users)


@users.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = UserForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            new_user.set_password(form.password.data) #pw should be hashed with some salt
            db.session.add(new_user)
            db.session.commit()
            return redirect('/users')

    return render_template('create_user.html', form=form)


@users.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
    form = DeleteForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            if current_user.authenticate(form.password.data):
                runs = db.session.query(Run).filter(Run.runner_id == current_user.id)

                for run in runs.all():
                    db.session.delete(run)

                db.session.delete(current_user)
                db.session.commit()
                logout_user()
                return redirect('/')
            else:
                flash("Incorrect password", category='error')

    return render_template("delete_user.html", form=form)

