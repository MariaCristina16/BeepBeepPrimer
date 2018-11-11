import pytest
import os
import tempfile
from random import uniform, randint
from datetime import datetime

from monolith.app import create_app
from monolith.database import db, Run, User, Objective, Report


# read in SQL for populating test data
# with open(os.path.join(os.path.dirname(__file__), 'prova.sql'), 'rb') as f:
#    _data_sql = f.read().decode('utf8')

@pytest.fixture
def client():
    """ This function initialize a new DB for every test and creates the app. This function returns a tuple,
    the first element is a test client and the second is the app itself. Test client must be used for sending
    request and the app should be used for getting a context when, for example, we need to query the DB.
    I haven't found a more elegant way to do this."""
    app = create_app()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    print(app.config['DATABASE'])
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+app.config['DATABASE']
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # disable CSRF validation -> DO THIS ONLY DURING TESTS!
    client = app.test_client()

    db.create_all(app=app)
    db.init_app(app=app)
    #with app.app_context():
        #db.engine.execute(_data_sql)
    with app.app_context():
        q = db.session.query(User).filter(User.email == 'example@example.com')
        user = q.first()
        if user is None:
            example = User()
            example.email = 'example@example.com'
            example.is_admin = True
            example.set_password('admin')
            db.session.add(example)
            db.session.commit()

    yield client, app

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


def login(client, email, password):
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def create_user(client, email='marco@prova.it', firstname='marco', lastname='mario', password='123456', age=18,
                weight=70, max_hr=120, rest_hr=65, vo2max=99):

    return client.post('/create_user', data=dict(email=email,
                                                 firstname=firstname,
                                                 lastname=lastname,
                                                 password=password,
                                                 age=age,
                                                 weight=weight,
                                                 max_hr=max_hr,
                                                 rest_hr=rest_hr,
                                                 vo2max=vo2max), follow_redirects=True)


def new_user(strava_token=None):
    user = User()
    user.email = 'test@example.com'
    user.firstname = "A"
    user.lastname = "Tester"
    user.strava_token = 0
    user.age = 0
    user.weight = 0
    user.max_hr = 0
    user.rest_hr = 0
    user.vo2max = 0
    user.set_password('test')
    if strava_token is not None:
        user.strava_token = strava_token
    db.session.add(user)
    db.session.commit()
    return user


def new_report(user, timestamp, choice_time):
    rep = Report()
    rep.runner_id = user.id
    rep.timestamp = timestamp
    rep.choice_time = choice_time
    db.session.add(rep)
    db.session.commit()
    return


def new_run(user, strava_id=randint(100, 100000000), name=None, distance=uniform(50.0, 10000.0), elapsed_time=uniform(30.0, 3600.0),
            average_heartrate=None, total_elevation_gain=uniform(0.0, 25.0), start_date=datetime.now()):
    if name is None :
        name = "Run %s" % strava_id

    run = Run()
    run.runner = user
    run.strava_id = strava_id  # a random number 100 - 1.000.000, we hope is unique
    run.name = name
    run.distance = distance  # 50m - 10 km
    run.elapsed_time = elapsed_time  # 30s - 1h
    run.average_speed = run.distance / run.elapsed_time
    run.average_heartrate = average_heartrate
    run.total_elevation_gain = total_elevation_gain  # 0m - 25m
    run.start_date = start_date
    db.session.add(run)
    db.session.commit()


def new_predefined_run(user):
    run = Run()
    run.runner = user
    run.strava_id = 10  # a random number 100 - 1.000.000, we hope is unique
    run.name = "Run " + str(run.strava_id)
    run.distance = 50000.0  # 50m - 10 km
    run.elapsed_time = 3900.0  # 30s - 1h
    run.average_speed = run.distance / run.elapsed_time
    run.average_heartrate = None
    run.total_elevation_gain = 3.0 # 0m - 25m
    run.start_date = datetime.now()
    db.session.add(run)
    db.session.commit()
    return run


def new_objective(user, name = "Test Objective", target_distance = "42", start_date = datetime.now(), end_date = datetime.now()):
    objective = Objective()
    objective.runner = user
    objective.name = name
    objective.target_distance = target_distance
    objective.start_date = start_date
    objective.end_date = end_date
    db.session.add(objective)
    db.session.commit()

    return objective
