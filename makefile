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
	printenv | grep "FLASK_APP"
	( \
		. env/bin/activate; \
		python3 tests/test.py; \
		python3 tests/guitests.py; \
	) # Used to tell makefile to use the virtualenv shell


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
