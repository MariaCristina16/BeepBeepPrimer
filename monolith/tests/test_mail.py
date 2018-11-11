from monolith.tests.utility import client, login
from monolith.database import db, User, Report
from monolith.tests.utility import create_user


def test_create_repo(client):
    tested_app, app = client

    reply=tested_app.get('/settingreport')
    assert reply.status_code == 401


    create_user(tested_app,email='mcriucc@gmail.com', firstname='mariacristina', lastname='uccheddu', password='ciao',
                                              age=23,
                                              weight=70,
                                              max_hr=120,
                                              rest_hr=60,
                                              vo2max=99)

    reply = tested_app.get('/settingreport')
    assert reply.status_code == 401

    assert login(tested_app, 'mcriucc@gmail.com', 'ciao').status_code == 200

    # now mcriucc@gmail.com is logged in
    with app.app_context():
        user = db.session.query(User).filter(User.email == 'mcriucc@gmail.com').first()

        reply = tested_app.get('/settingreport')
        assert reply.status_code == 200


        reply = tested_app.post('/settingreport', data=dict(setting_mail='6'), follow_redirects=True)
        assert reply.status_code == 200
        mail = db.session.query(Report).filter(Report.runner_id == user.id).first()
        assert mail is not None
        assert mail.runner_id == user.id
        assert mail.choice_time == 21600.0


        reply = tested_app.post('/settingreport', data=dict(setting_mail='12'), follow_redirects=True)
        assert reply.status_code == 200
        mail = db.session.query(Report).filter(Report.runner_id == user.id).first()
        assert mail is not None
        assert mail.runner_id == user.id
        assert mail.choice_time == 43200.0


        reply = tested_app.post('/settingreport', data=dict(setting_mail='24'), follow_redirects=True)
        assert reply.status_code == 200
        mail = db.session.query(Report).filter(Report.runner_id == user.id).first()
        assert mail is not None
        assert mail.runner_id == user.id
        assert mail.choice_time == 86400.0


        reply = tested_app.post('/settingreport', data=dict(setting_mail=None), follow_redirects=True)
        reply.status_code == 400


