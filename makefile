ACTIVATE := ./bin/activate

install: requirements.txt
	. $(ACTIVATE)
	pip install -r requirements.txt

run: src/app.py
	. $(ACTIVATE)
	python3 src/app.py

