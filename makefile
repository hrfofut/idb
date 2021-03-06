# Create a githook that automatically formats python code before commit
# Create and install libraries in a virtual enviornment
install: requirements.txt idb/ setup.py
	- chmod +x .pre-commit.py
	- cp .pre-commit.py .git/hooks/pre-commit
	( \
		virtualenv -p python3 env; \
		. env/bin/activate; \
		pip3 install -r requirements.txt; \
		pwd; \
		pip3 install -e .; \
	) # Used to tell makefile to use the virtualenv shell
	make gecko

# Run Flask
run: idb/ instance/
	printenv | grep "FLASK_APP" # must set environment variable FLASK_APP to "idb/__init__.py"
	( \
		. env/bin/activate; \
		flask run; \
	) # Used to tell makefile to use the virtualenv shell

# Restart everything on the production server
restart-prod:
	systemctl stop nginx
	systemctl stop idb
	systemctl start idb
	systemctl start nginx

# Run all tests
test: idb/ tests/test.py tests/guitests.py instance/
	( \
		. env/bin/activate; \
		mocha ./frontend/tests.js; \
		python3 backend/tests.py; \
		python3 tests/guitests.py; \
	) # Used to tell makefile to use the virtualenv shell

gecko:
	- wget https://github.com/mozilla/geckodriver/releases/download/v0.20.0/geckodriver-v0.20.0-linux64.tar.gz 
	- tar -xvzf geckodriver-v0.20.0-linux64.tar.gz 
	- rm geckodriver-v0.20.0-linux64.tar.gz 
	- chmod +x geckodriver 
	- mv geckodriver ./env/bin/geckodriver2
	- echo "#!/bin/bashpath/to/geckodriver \"\$\@\" --marionette-port 2828" >> geckodriver 
	- cp gs ./env/bin/geckodriver
	- chmod +x env/bin/geckodriver 

clean:
	- rm -rf .git/hooks/pre-commit
	- rm -rf *.egg*
	- rm idb/idb.log
	- find . | grep -E "(__pycache__|\.pyc|\.pyo)" | xargs rm -rf

# Reset all virtual enviornment data
scrub-virtualenv:
	- rm -rf ./env

# Remove unescessary files and then launch flask
travis:
	ls -a
	make install
	ls -a
	make test

# Requirements for the last phase
GithubID = hrfofut
RepoName = idb

githubid:
	@echo "${GithubID}"

reponame:
	@echo "${RepoName}"

sha:
	git rev-parse HEAD

github:
	@echo "http://www.github.com/${GithubID}/${RepoName}"

issues:
	@echo "http://www.github.com/${GithubID}/${RepoName}/issues"

stories:
	@echo "http://www.github.com/${GithubID}/${RepoName}/projects"

uml:
	@echo "http://www.github.com/${GithubID}/${RepoName}/blob/master/docs/diagram.png"

selenium: idb/ tests/guitests.py instance/
	( \
		. env/bin/activate; \
		python3 tests/guitests.py; \
	) # Used to tell makefile to use the virtualenv shell

frontend: idb/ tests/guitests.py instance/
	( \
		. env/bin/activate; \
		mocha ./frontend/tests.js; \
	) # Used to tell makefile to use the virtualenv shell

backend: idb/ tests/guitests.py instance/
	( \
		. env/bin/activate; \
		python3 backend/tests.py; \
	) # Used to tell makefile to use the virtualenv shell

website:
	@echo "http://caloriekiller.club"

report:
	@echo "https://hrfofut.gitbooks.io/report/content/"

apidoc:
	@echo "https://hrfofut.gitbooks.io/api/content/"

self:
	@echo "https://hrfofut.gitbooks.io/report/content/self-critiques.html"

other:
	@echo "https://hrfofut.gitbooks.io/report/content/other-critiques.html"
