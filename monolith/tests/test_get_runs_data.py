from monolith.database import db, User
from monolith.tests.utility import client, create_user, new_predefined_run, login
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

