from monolith.tests.utility import client, login, create_user, logout, new_objective, new_predefined_run, new_report
from monolith.database import db, User, Run, Report, Objective
from werkzeug.security import check_password_hash


def test_create_user(client):
    tested_app, app = client

    assert tested_app.get('/create_user').status_code == 200

    assert tested_app.post('/create_user', data=None).status_code == 400

    reply = tested_app.post('/create_user', data=dict(email='andrea@prova.it', firstname='andrea', lastname='bongiorno',
                                                      password='123456',
                                                      age=23,
                                                      weight=70,
                                                      max_hr=120,
                                                      rest_hr=60,
                                                      vo2max=99), follow_redirects=True)

    assert reply.status_code == 200  # create_user success (it also redirect to login)

    assert login(tested_app, 'andrea@prova.it', '123456').status_code == 200

    # cannot create a user when already logged in
    assert create_user(tested_app).status_code == 403

    with app.app_context():
        user = db.session.query(User).filter(User.email == 'andrea@prova.it').first()
        assert user is not None
        assert user.email == 'andrea@prova.it'
        assert user.firstname == 'andrea'
        assert user.lastname == 'bongiorno'
        assert check_password_hash(user.password, '123456') is True
        assert user.age == 23
        assert user.weight == 70
        assert user.max_hr == 120
        assert user.rest_hr == 60
        assert user.vo2max == 99

    logout(tested_app)

    # cannot create a user with the same email
    reply = tested_app.post('/create_user', data=dict(email='andrea@prova.it', firstname='andrea', lastname='bongiorno',
                                                      password='123456',
                                                      age=23,
                                                      weight=70,
                                                      max_hr=120,
                                                      rest_hr=60,
                                                      vo2max=99), follow_redirects=False)
    assert reply.status_code == 409


def test_delete_user(client):
    tested_app, app = client

    reply = create_user(tested_app)  # creates a user with 'marco@prova.it' as email, default
    assert reply.status_code == 200

    reply = login(tested_app, 'marco@prova.it', '123456')
    assert reply.status_code == 200

    reply = logout(tested_app)
    assert reply.status_code == 200

    # retrieve delete_user page without logging in before
    reply = tested_app.get('/delete_user')
    assert reply.status_code == 401

    reply = login(tested_app, email='marco@prova.it', password='123456')
    assert reply.status_code == 200

    with app.app_context():
        user = db.session.query(User).filter(User.email == 'marco@prova.it').first()
        new_predefined_run(user)
        assert db.session.query(Run).filter(Run.runner_id == user.id).first() is not None
        new_objective(user)
        assert db.session.query(Objective).filter(Objective.runner_id == user.id).first() is not None
        new_report(user, 1, 1)  # the 2nd and 3rd params doesn't matter
        assert db.session.query(Report).filter(Report.runner_id == user.id).first() is not None

    # retrieve delete_user page
    reply = tested_app.get('/delete_user')
    assert reply.status_code == 200

    # post bad request
    reply = tested_app.post('/delete_user', data=None)
    assert reply.status_code == 400

    # post incorrect password
    reply = tested_app.post('/delete_user', data=dict(password='000000'))
    assert reply.status_code == 401

    # post correct password and checking that the user has been deleted
    reply = tested_app.post('/delete_user', data=dict(password='123456'), follow_redirects=True)
    assert reply.status_code == 200

    with app.app_context():
        assert db.session.query(Run).filter(Run.runner_id == user.id).first() is None
        assert db.session.query(User).filter(User.email == 'marco@prova.it').first() is None
        assert db.session.query(Objective).filter(Objective.runner_id == user.id).first() is None
        assert db.session.query(Report).filter(Report.runner_id == user.id).first() is None


def test_users_list(client):
    tested_app, app = client

    assert login(tested_app, email='example@example.com', password='admin').status_code == 200

    # only admin can get this page
    assert tested_app.get('/users').status_code == 200

    reply = logout(tested_app)
    assert reply.status_code == 200

    assert create_user(tested_app).status_code == 200

    assert login(tested_app, email='marco@prova.it', password='123456').status_code == 200

    # marco@prova.it is not admin
    assert tested_app.get('/users').status_code == 401
