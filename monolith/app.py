import os
from flask import Flask
from monolith.views import blueprints
from monolith.auth import login_manager
from monolith.errors import render_error_page


def create_app():
    app = Flask(__name__)
    # App
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # suppress pytest warning
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'
    app.config['STRAVA_CLIENT_ID'] = os.environ['STRAVA_CLIENT_ID']
    app.config['STRAVA_CLIENT_SECRET'] = os.environ['STRAVA_CLIENT_SECRET']
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beepbeep.db'

    # Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
    app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    from monolith.database import db, User, Report
    db.init_app(app)
    login_manager.init_app(app)
    db.create_all(app=app)

    # create a first admin user
    with app.app_context():
        app.register_error_handler(401, render_error_page)
        app.register_error_handler(403, render_error_page)
        app.register_error_handler(404, render_error_page)
        q = db.session.query(User).filter(User.email == 'example@example.com')
        user = q.first()
        if user is None:
            example = User()
            example.email = 'example@example.com'
            example.is_admin = True
            example.set_password('admin')
            db.session.add(example)
            db.session.commit()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
