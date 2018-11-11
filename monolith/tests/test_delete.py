from monolith.tests.utility import client, login, create_user, logout, new_predefined_run, new_objective
from monolith.database import db, User, Run, Objective, Report


def test_delete(client):
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

    # retrieve delete_user page
    reply = tested_app.get('/delete_user')
    assert reply.status_code == 200

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


