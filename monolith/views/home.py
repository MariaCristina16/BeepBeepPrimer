from flask import Blueprint, render_template, request, flash
from stravalib import Client
from flask_login import current_user, LoginManager, login_required, confirm_login
from monolith.database import db, Run, Report
from monolith.forms import MailForm
from datetime import time

home = Blueprint('home', __name__)


def _strava_auth_url(config):
    client = Client()
    client_id = config['STRAVA_CLIENT_ID']
    redirect = 'http://127.0.0.1:5000/strava_auth'
    url = client.authorization_url(client_id=client_id,
                                   redirect_uri=redirect)
    return url


def strava_auth_url(config):
    return _strava_auth_url(config)


@home.route('/')
def index():
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        runs = db.session.query(Run).filter(Run.runner_id == current_user.id)
        total_average_speed = 0
        print(current_user.strava_token)
        for run in runs:
            total_average_speed += run.average_speed
            print(run.name)
        if runs.count():
            total_average_speed /= runs.count()
        total_average_speed = round(total_average_speed, 2)
    else:
        runs = None
        total_average_speed = 0
    strava_auth_url_ = strava_auth_url(home.app.config)
    return render_template("index.html", runs=runs,
                           strava_auth_url=strava_auth_url_, total_average_speed=total_average_speed)
