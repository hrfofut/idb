# Create a githook that automatically formats python code before commit
# Create and install libraries in a virtual enviornment
install: requirements.txt
	- chmod +x .pre-commit.py
	- cp .pre-commit.py .git/hooks/pre-commit
	( \
		virtualenv -p python3 .; \
		. bin/activate; \
		pip install -r requirements.txt; \
	) # Used to tell makefile to use the virtualenv shell

# Run flask
run: src/app.py
	( \
		. bin/activate; \
		python3 src/app.py; \
	) # Used to tell makefile to use the virtualenv shell

# Run all tests
test: src/app.py tests/test.py
	( \
		. bin/activate; \
		python3 tests/test.py; \
	) # Used to tell makefile to use the virtualenv shell

clean:
	rm -rf .git/hooks/pre-commit

# Reset all virtual enviornment data
scrub-virtualenv:
	make clean
	rm -rf ./bin
	rm -rf ./include
	rm -rf ./lib
	rm -rf ./share

# Remove unescessary files and then launch flask
travis:
	make clean
	ls -a
	make test
