from monolith.background import prepare_body
from monolith.tests.utility import client, create_user, login, new_predefined_run, new_user
from monolith.database import Run, db, User
from monolith.background import fetch_runs
import requests


def test_prepare_body(client):
    tested_app, app = client

    reply = create_user(tested_app)  # creates a user with 'marco@prova.it' as email, default
    assert reply.status_code == 200

    reply = login(tested_app, 'marco@prova.it', '123456')
    assert reply.status_code == 200

    with app.app_context():
        user = db.session.query(User).filter(User.email == 'marco@prova.it').first()
        run = new_predefined_run(user)
        assert db.session.query(Run).filter(Run.runner_id == user.id).first() is not None

    assert prepare_body(user, app) == "name: Run 10\ndistance: 50000.0\nstart_date: "+str(run.start_date)+"\n" \
                                      "average_speed: 12.820512820512821\nelapsed_time: 3900.0\naverage_heartrate: None" \
                                      "\ntotal_elevation_gain: 3.0\n\n\n"


def test_mail_config(client):
    tested_app, app = client

    assert app.config['MAIL_SERVER'] == 'smtp.gmail.com'
    assert app.config['MAIL_PORT'] == 465
    assert app.config['MAIL_USERNAME'] == 'yt.beepbeep'
    assert app.config['MAIL_PASSWORD'] == 'TestYellowTeam7'
    assert app.config['MAIL_USE_TLS'] is False
    assert app.config['MAIL_USE_SSL'] is True


def test_fetch_run(client):
    tested_app, app = client

    # token of a test account
    strava_token = 'f288e7b7f4e118c8aca3f655b8e95f4c4d335434'

    with app.app_context():

        user = new_user(strava_token)
        try:
            runs = fetch_runs(user)

            assert runs == 1

            run = db.session.query(Run).filter(Run.runner_id == user.id).first()
            assert run is not None
            assert run.name == 'Evening Run'

        except requests.exceptions.ConnectionError:
            assert True is True
