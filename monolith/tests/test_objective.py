from monolith.tests.utility import client, login, new_run, new_objective, create_user
from monolith.database import db, User, Objective
from datetime import datetime, timedelta
from monolith.tests.id_parser import get_element_by_id


def test_create_objective(client):
    tested_app, app = client

    # test for create_objective having not logged in
    reply = tested_app.post('/create_objective')
    assert reply.status_code == 401
    
    # create a new user
    reply = create_user(tested_app)
    assert reply.status_code == 200

    reply = login(tested_app, email='marco@prova.it', password='123456')
    assert reply.status_code == 200

    # test for create_objective logged in but without data
    reply = tested_app.post('/create_objective')
    assert reply.status_code == 400

    # test for create_objective logged in with wrong data
    reply = tested_app.post('/create_objective', data=dict(
            start_date="asd",
            name="Wrong test1"
    ))
    assert reply.status_code == 400

    reply = tested_app.post('/create_objective', data=dict(
            end_date="asd",
            name="Wrong test2"
    ))
    assert reply.status_code == 400

    reply = tested_app.post('/create_objective', data=dict(
            target_distance=-20,
            name="Wrong test3"
    ))
    assert reply.status_code == 400

    # end date before start date
    reply = tested_app.post('/create_objective', data=dict(
            start_date="2018-07-04",
            end_date="2017-07-04",
            name="Wrong test3"
    ))
    assert reply.status_code == 400

    # test for create_objective logged in with wrong data
    reply = tested_app.post('/create_objective', data=dict(
            start_date="2018-07-04",
            end_date="2018-07-05",
            target_distance=22,
            name="Test OK"
    ))
    assert reply.status_code == 200

def test_view_objectives(client):
    tested_app, app = client

    with app.app_context():
        # create a new user
        reply = create_user(tested_app)
        assert reply.status_code == 200

        reply = login(tested_app, email='marco@prova.it', password='123456')
        assert reply.status_code == 200

        # retrieve the user object
        q = db.session.query(User).filter(User.email == 'marco@prova.it')
        user = q.first()
        
        # add the objective
        new_objective(user, name="Test1")
        new_objective(user, name="Test2")
        new_objective(user, name="Test3")
        new_objective(user, name="Test4")

        # retrieve the objective table
        objectives = db.session.query(Objective) 

        reply = tested_app.get('objectives')
        assert reply.status_code == 200

        for o in objectives.all():
            assert get_element_by_id("objective_%s_name"%(o.id), str(reply.data)) == str(o.name)
            assert get_element_by_id("objective_%s_start_date"%(o.id), str(reply.data)) == str(o.start_date)
            assert get_element_by_id("objective_%s_end_date"%(o.id), str(reply.data)) == str(o.end_date)
            assert get_element_by_id("objective_%s_target_distance"%(o.id), str(reply.data)) == str(o.target_distance)
            assert get_element_by_id("objective_%s_completion"%(o.id), str(reply.data)) == str(o.completion)


def test_check_objective_completion(client):
    tested_app, app = client

    # create a new user
    reply = create_user(tested_app)
    assert reply.status_code == 200

    # login as new user
    reply = login(tested_app, email='marco@prova.it', password='123456')
    assert reply.status_code == 200

    with app.app_context():
        # retrieve the user object and login
        user = db.session.query(User).filter(User.email == 'marco@prova.it').first()

        # check an objective with completion = 0%
        objective_1 = new_objective(user, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=7),
                                    target_distance=3000)
        assert objective_1.completion == 0

        # create some test runs
        new_run(user, distance=500, elapsed_time=1024, start_date=datetime.now())
        new_run(user, distance=10, elapsed_time=660, start_date=datetime.now() + timedelta(days=2))
        new_run(user, distance=30, elapsed_time=2048, start_date=datetime.now() + timedelta(days=4))

        # check an objective with completion 50%
        objective_2 = new_objective(user, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=1),
                                    target_distance=1000)
        assert objective_2.completion == 50

        # check an objective with completion of 100%
        objective_3 = new_objective(user, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=1),
                                    target_distance=400)
        assert objective_3.completion == 100

        # check an objective with completion of 100% with exactly the km needed to complete it
        objective_4 = new_objective(user, start_date=datetime.now(), end_date=datetime.now() + timedelta(days=5),
                                    target_distance=540)
        assert objective_4.completion == 100
