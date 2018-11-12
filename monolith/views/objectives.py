from flask import Blueprint, redirect, render_template, request, flash, make_response
from flask_login import login_required, current_user
from monolith.database import db, User, Objective
from monolith.auth import admin_required, current_user
from monolith.forms import ObjectiveForm
from monolith.views.home import home, strava_auth_url
from stravalib import Client


objectives = Blueprint('objectives', __name__)

@objectives.route('/objectives', methods=['GET'])
@login_required
def _objectives():
    objectives = db.session.query(Objective).filter(Objective.runner_id == current_user.id)
    return render_template("objectives.html", objectives=objectives)


@objectives.route('/create_objective', methods=['GET', 'POST'])
@login_required
def create_objective():
    status = 200
    
    form = ObjectiveForm()
    if request.method == 'POST':

        if form.validate_on_submit():
            new_objective = Objective()
            form.populate_obj(new_objective)
            new_objective.runner = current_user

            db.session.add(new_objective)
            db.session.commit()
            return redirect('/objectives'), status
        else:
            # Bad data were sent
            status = 400
            
    return render_template('create_objective.html', form=form), status

