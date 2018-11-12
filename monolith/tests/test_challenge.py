from monolith.tests.utility import client, login
from monolith.database import db, User, Challenge
from monolith.tests.utility import create_user, new_run

def test_create_challenge(client):
    tested_app, app = client

    # test for create_challenge having not logged in
    reply = tested_app.get('/create_challenge')
    assert reply.status_code == 401

    # test for /challenge , list of all user challenges having not logged in
    reply = tested_app.get('/challenge')
    assert reply.status_code == 401

    # test for comparison of runs in a challenge having not logged in
    reply = tested_app.get('/challenge/1')
    assert reply.status_code == 401

    reply = create_user(tested_app,email='mcriucc@gmail.com', firstname='mariacristina', lastname='uccheddu', password='ciao',
                                              age=23,
                                              weight=70,
                                              max_hr=120,
                                              rest_hr=60,
                                              vo2max=99)

    assert login(tested_app, 'mcriucc@gmail.com', 'ciao').status_code == 200

    # test for comparison of runs in a challenge logged in but the challenge doesn't exists
    reply = tested_app.get('/challenge/1')
    assert reply.status_code == 404

    # test for /challenge , list of all user challenges having logged in , return the vision of an empty list, you can see only the title of the page
    reply = tested_app.get('/challenge')
    assert reply.status_code == 200

    reply = tested_app.post('create_challenge',data=dict(
            run_one="0",
            run_two="0"
    ))
    assert reply.status_code == 400

    with app.app_context():
        query = db.session.query(User).filter(User.email == 'mcriucc@gmail.com')
        user = query.first()
        new_run(user)
        new_run(user)
        new_run(user)

        var = 0
        reply = tested_app.post('create_challenge', data=dict(
            run_one="1",
            run_two="1"
        ))
        assert reply.status_code == 400

        reply = tested_app.post('create_challenge', data=dict(
            run_one="1",
            run_two="2"
        ))
        assert reply.status_code == 200
        var = var+1

        challenge = db.session.query(Challenge).filter(Challenge.id == var).first()
        assert challenge.run_one == 1
        assert challenge.run_two == 2


        reply = tested_app.post('create_challenge', data=dict(
            run_one="1",
            run_two="3"
        ))
        assert reply.status_code == 200
        var = var+1

        challenge = db.session.query(Challenge).filter(Challenge.id == var).first()
        assert challenge.run_one == 1
        assert challenge.run_two == 3

        reply = tested_app.post('create_challenge', data=dict(
            run_one="1",
            run_two="40"
        ))
        assert reply.status_code == 400

        reply = tested_app.post('create_challenge', data=dict(
            run_one="40",
            run_two="0"
        ))
        assert reply.status_code == 400

        reply = tested_app.post('create_challenge', data=dict(
            run_one="90",
            run_two="90"
        ))
        assert reply.status_code == 400

        # test for /challenge , list of all user challenges having logged in , return the vision of an empty list, you can see only the title of the page
        reply = tested_app.get('/challenge')
        assert reply.status_code == 200
