from monolith.database import db, User, Run
from monolith.tests.utility import client, create_user, new_predefined_run, login, new_run
from monolith.tests.id_parser import get_element_by_id
import json


def test_runs_data(client):
    tested_app, app = client

    assert create_user(tested_app).status_code == 200

    # trying to retrieve data without logging in
    reply = tested_app.post('run/statistics', data=json.dumps({'runs': [1, 2, 3, 4, 5], 'params': [True, True, True]}),
                            content_type='application/json')
    assert reply.status_code == 401

    assert login(tested_app, email='marco@prova.it', password='123456').status_code == 200

    # creating some fake runs
    with app.app_context():
        q = db.session.query(User).filter(User.email == 'marco@prova.it')
        user = q.first()
        run1 = new_predefined_run(user)  # run with id 1
        run2 = new_predefined_run(user)  # run with id 2
        run3 = new_predefined_run(user)  # run with id 3
        run4 = new_predefined_run(user)  # run with id 4
        run5 = new_predefined_run(user)  # run with id 5

    reply = tested_app.post('run/statistics', data=json.dumps({'runs': [1, 2, 3, 4, 5], 'params': [True, True, True]}),
                            content_type='application/json')

    assert reply.status_code == 200
    body = json.loads(str(reply.data, 'utf8'))
    assert body == {'1': [12.820512820512821, 50000.0, 3900.0, 'Run 10'],
                    '2': [12.820512820512821, 50000.0, 3900.0, 'Run 10'],
                    '3': [12.820512820512821, 50000.0, 3900.0, 'Run 10'],
                    '4': [12.820512820512821, 50000.0, 3900.0, 'Run 10'],
                    '5': [12.820512820512821, 50000.0, 3900.0, 'Run 10']}


def test_statistics(client):
    tested_app, app = client

    reply = create_user(tested_app)
    assert reply.status_code == 200

    with app.app_context():
        q = db.session.query(User).filter(User.email == 'marco@prova.it')
        user = q.first()
        run1 = new_predefined_run(user)  # run with id 1
        run2 = new_predefined_run(user)  # run with id 2
        run3 = new_predefined_run(user)  # run with id 3
        run4 = new_predefined_run(user)  # run with id 4
        run5 = new_predefined_run(user)  # run with id 5

        reply = tested_app.get('/statistics')
        assert reply.status_code == 401

        assert login(tested_app, email='marco@prova.it', password='123456').status_code == 200

        reply = tested_app.get('/statistics')
        assert reply.status_code == 200

        # check the correctness of the fields
        assert get_element_by_id(str(run1.id), str(reply.data)) == str(run1.name)
        assert get_element_by_id(str(run2.id), str(reply.data)) == str(run2.name)
        assert get_element_by_id(str(run3.id), str(reply.data)) == str(run3.name)
        assert get_element_by_id(str(run4.id), str(reply.data)) == str(run4.name)
        assert get_element_by_id(str(run5.id), str(reply.data)) == str(run5.name)


def test_average_speed(client):
    tested_app, app = client

    # prepare the database creating a new user
    reply = create_user(tested_app)  # creates a user with 'marco@prova.it' as email, default
    assert reply.status_code == 200

    # login as new user
    reply = login(tested_app, email='marco@prova.it', password='123456')
    assert reply.status_code == 200

    # retrieve the user object and login
    with app.app_context():
        q = db.session.query(User).filter(User.email == 'marco@prova.it')
        user = q.first()
        user.strava_token = "fake_token"
        db.session.commit()

    # The average speed should be 0 if there are no runs
    reply = tested_app.get('/')
    assert reply.status_code == 200
    assert get_element_by_id('total_average_speed', str(reply.data)) == str(0)

    # add a run
    with app.app_context():
        new_run(user)

    # retrieve the run
    with app.app_context():
        q = db.session.query(Run).filter(Run.id == 1)  # should be the first
        run1 = q.first()

    # with only a run the average speed should be the average speed of the run
    reply = tested_app.get('/')
    assert reply.status_code == 200
    assert get_element_by_id('total_average_speed', str(reply.data)) == str(round(run1.average_speed, 2))

    # add another run
    with app.app_context():
        new_run(user)

    # retrieve the runs list
    with app.app_context():
        runs = db.session.query(Run).filter()  # should be all owned by our user

    # with multiples runs the average speed should be the average of the average speed of each run
    total_average_speed = 0
    for run in runs:
        total_average_speed += run.average_speed
    total_average_speed /= runs.count()

    reply = tested_app.get('/')
    assert reply.status_code == 200
    assert get_element_by_id('total_average_speed', str(reply.data)) == str(round(total_average_speed, 2))




