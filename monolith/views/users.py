from flask import Blueprint, redirect, render_template, request, flash, make_response, url_for, abort
from flask_login import login_required, current_user, logout_user
from monolith.database import db, User, Run, Objective, Report
from monolith.auth import admin_required
from monolith.forms import UserForm, DeleteForm


users = Blueprint('users', __name__)


@users.route('/users')
@admin_required  # throws 401 HTTPException
def _users():
    users = db.session.query(User)
    return render_template("users.html", users=users)


@users.route('/create_user', methods=['GET', 'POST'])
def create_user():
    # A connected user cannot create other users
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated is True:
        return abort(403)

    form = UserForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            c = db.session.query(User).filter(new_user.email == User.email)
            if c.first() is None:
                new_user.set_password(form.password.data)  # pw should be hashed with some salt
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('auth.login'))
            else:
                flash('Already existing user', category='error')
                return make_response(render_template('create_user.html', form=form), 409)

    return render_template('create_user.html', form=form)


@users.route('/delete_user', methods=['GET', 'POST'])
@login_required
def delete_user():
    form = DeleteForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            if current_user.authenticate(form.password.data) and hasattr(current_user, 'id'):
                runs = db.session.query(Run).filter(Run.runner_id == current_user.id)
                objectives = db.session.query(Objective).filter(Objective.runner_id == current_user.id)
                reports = db.session.query(Report).filter(Report.runner_id == current_user.id)

                for run in runs.all():
                    db.session.delete(run)

                for report in reports.all():
                    db.session.delete(report)

                for objective in objectives.all():
                    db.session.delete(objective)

                db.session.delete(current_user)
                db.session.commit()
                
                logout_user()  # This will also clean up the remember me cookie if it exists.
                return redirect('/')
            else:
                flash("Incorrect password", category='error')
                return make_response(render_template("delete_user.html", form=form), 401)

    return render_template("delete_user.html", form=form)
