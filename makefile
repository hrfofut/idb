# Create a githook that automatically formats python code before commit
# Create and install libraries in a virtual enviornment
install: requirements.txt
	- chmod +x .pre-commit.py
	- cp .pre-commit.py .git/hooks/pre-commit
	( \
		virtualenv -p python3 env; \
		. env/bin/activate; \
		pip install -r requirements.txt; \
	) # Used to tell makefile to use the virtualenv shell

# Run flask
run: src/app.py
	( \
		. env/bin/activate; \
		cd src; \
		python3 app.py; \
	) # Used to tell makefile to use the virtualenv shell

# Run all tests
test: src/app.py tests/test.py
	( \
		. env/bin/activate; \
		cd tests; \
		python3 test.py; \
	) # Used to tell makefile to use the virtualenv shell

clean:
	rm -rf .git/hooks/pre-commit

# Reset all virtual enviornment data
scrub-virtualenv:
	rm -rf ./env

# Remove unescessary files and then launch flask
travis:
	ls -a
	make install
	ls -a
	make test
