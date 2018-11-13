# BeepBeep Monolith
_Check also the original [README.rst](README.rst) file._

[![Build Status](https://travis-ci.org/MariaCristina16/BeepBeepPrimer.svg?branch=master)](https://travis-ci.org/MariaCristina16/BeepBeepPrimer)
[![Coverage Status](https://coveralls.io/repos/github/MariaCristina16/BeepBeepPrimer/badge.svg?branch=master)](https://coveralls.io/github/MariaCristina16/BeepBeepPrimer?branch=master)

## First setup

#### 1. Create a Strava API application
- https://strava.github.io/api/#access
- https://www.strava.com/settings/api

Export the variables you have obtained by registering your application
creating a file `variables.sh` in the project root.

```
#!/bin/bash
export STRAVA_CLIENT_ID=<ID>
export STRAVA_CLIENT_SECRET=<SECRET>

export MAIL_USERNAME=<USERNAME>
export MAIL_PASSWORD=<PASSWORD>
```

You can load the variables with `source variables.sh`.

#### 2. Create a virtual env (suggested)
```
pip3.6 install virtualenv
python 3.6 -m virtualenv venv
```

Activate the virtual env with `source venv/bin/activate`.

#### 3. Install requirements
```
pip install -r requirements.txt
python setup.py develop
```

#### 4. Install redis



## Run the app

##### Terminal #1
Start redis: `redis-server`

##### Terminal #2
1. Load environment variables:  
   `source variables.sh`
2. Load the virtual env (only if you have created a virtual env):  
   `source venv/bin/activate`
3. Start a celery worker:  
   `celery worker -A monolith.background -B`

##### Terminal #3
1. Load environment variables:  
  `source variables.sh`
2. Load the virtual env (only if you have created a virtual env):  
  `source venv/bin/activate`
3. Start the server:
   `python monolith/app.py`

##### Browser
- [http://localhost:5000](http://localhost:5000)
- Follow the instruction to register a new user, bind your account with your Strava profile and fetch your runs.


## Contribute

#### Install dev requirements
`pip install -r dev-requirements.txt`

### Test
- Run test with `pytest` from the root folder.
- For the coverage `pytest --cov-config .coveragerc --cov monolith/tests`
