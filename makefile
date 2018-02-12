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

# Run flask
run: idb/ instance/
	printenv | grep "FLASK_APP" # must set environment variable FLASK_APP to "idb/__init__.py"
	( \
		. env/bin/activate; \
		flask run; \
	) # Used to tell makefile to use the virtualenv shell

# Run all tests
test: src/app.py tests/test.py
	( \
		. env/bin/activate; \
		cd tests; \
		python3 test.py; \
	) # Used to tell makefile to use the virtualenv shell

clean:
	- rm -rf .git/hooks/pre-commit
	- rm -rf *.egg*
	- rm -rf idb/__pycache__/
	- rm idb/idb.log

# Reset all virtual enviornment data
scrub-virtualenv:
	- rm -rf ./env

# Remove unescessary files and then launch flask
travis:
	ls -a
	make install
	ls -a
	make test
