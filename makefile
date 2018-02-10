ACTIVATE := ./bin/activate

install: requirements.txt
	- chmod +x .pre-commit.py
	- cp .pre-commit.py .git/hooks/pre-commit
	. $(ACTIVATE)
	pip install -r requirements.txt

run: src/app.py
	. $(ACTIVATE)
	python3 src/app.py

travis:
	#make clean
	ls -a
	python3 tests/test.py
