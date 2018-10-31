from flask import Blueprint, render_template
from stravalib import Client

from monolith.database import db, Run
from monolith.auth import current_user


home = Blueprint('home', __name__)


def _strava_auth_url(config):
    client = Client()
    client_id = config['STRAVA_CLIENT_ID']
    redirect = 'http://127.0.0.1:5000/strava_auth'
    url = client.authorization_url(client_id=client_id,
                                   redirect_uri=redirect)
    return url


@home.route('/')
def index():
    if current_user is not None and hasattr(current_user, 'id'):
        runs = db.session.query(Run).filter(Run.runner_id == current_user.id)
        total_average_speed = 0
        for run in runs:
            total_average_speed += run.average_speed
        if runs.count():
            total_average_speed /= runs.count()
    else:
        runs = None
        total_average_speed = 0
    strava_auth_url = _strava_auth_url(home.app.config)
    return render_template("index.html", runs=runs,
                           strava_auth_url=strava_auth_url, total_average_speed=total_average_speed)
