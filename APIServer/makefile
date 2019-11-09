PYLINT = flake8
PYLINTFLAGS = --ignore=E741,W503 --exclude=interactive.py,__main__.py
PYTHONFILES = $(shell ls *.py)

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

pytests: $(PYTHONFILES)
	./pytests.sh

tests: pytests lint

api_server: 
	./api.sh

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

