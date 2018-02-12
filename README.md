# Build status:
[![Build Status](https://travis-ci.org/hrfofut/idb.svg?branch=master)](https://travis-ci.org/hrfofut/idb)

# Usage and development guide
This project uses python's [virtualenv](https://virtualenv.pypa.io/en/stable/userguide/)
in order to share and maintain libraries.  The list of currently used libraries is listed
in `requirements.txt`.  This list should be updated whenever a new library or tool is
installed.

## Installation
Installation for this project is as follows.  To install, first create an enviornment variable
called `FLASK_APP` set to `idb/__init.py`.  In Linux, this is `export FLASK_APP=idb/__init__.py`.
Then, run `make install`.

To run, simply run `make run`.  Finally, to have non-default configs copy `default_config.py`
in `src/instance/` to `application.py` and fill with your desired config values.

# Documentation
The UML diagram is generated via [PlantUML](http://plantuml.com/)

# Connecting to AWS server
For now, to connect to AWS server, first download the pem file on Slack. Then ssh by saying 
$ ssh -i "FileName.pem" ubuntu@ec2-34-209-147-2.us-west-2.compute.amazonaws.com 
This will be updated when the domain name is working. 

# Credits
This is a project for CS373 Software Engineering.

The group consists of:
1. Harrison Foreman
2. Brandon Harrison
3. Wesley Joe
4. Bao Than
5. Cindy Truong

Autoformatter hook grabbed from: https://github.com/chibiegg/git-autopep8/blob/master/pre-commit
