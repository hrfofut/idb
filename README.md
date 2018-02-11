# Build status:
[![Build Status](https://travis-ci.org/hrfofut/idb.svg?branch=master)](https://travis-ci.org/hrfofut/idb)

# Usage and development guide
This project uses python's [virtualenv](https://virtualenv.pypa.io/en/stable/userguide/)
in order to share and maintain libraries.  The list of currently used libraries is listed
in `requirements.txt`.  This list should be updated whenever a new library or tool is
installed.

## Installation
Installation for this project is straightforward.  To install, simply run `make install`.
To run, simply run `make run`.  Finally, rename `default_config.py` in `src/instance/`
to `application.py` and fill with your desired config values.

# Documentation
The UML diagram is generated via [PlantUML](http://plantuml.com/)

# Credits
This is a project for CS373 Software Engineering.

The group consists of:
1. Harrison Foreman
2. Brandon Harrison
3. Wesley Joe
4. Bao Than
5. Cindy Truong

Autoformatter hook grabbed from: https://github.com/chibiegg/git-autopep8/blob/master/pre-commit
