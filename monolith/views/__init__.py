from .home import home
from .auth import auth
from .users import users
from .strava import strava
from .objectives import objectives
from .run import run
from .statistics import statistics
from .challenge import challenge
from .report import report

blueprints = [home, auth, users, strava, run, statistics, objectives, challenge, report]
