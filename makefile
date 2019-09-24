# Need to export as ENV var
export TEST_DIR = tests
export TEST_DATA = test_data
export CODE_DIR = .
export HTML_DIR = .
export DATA_DIR = $(CODE_DIR)/data
export DOCKER_DIR = docker
PYTHONFILES = $(shell ls *.py)
PYTHONFILES += $(shell ls $(LIB_DIR)/*.py)

FORCE:

container: $(DOCKER_DIR)/Dockerfile  $(DOCKER_DIR)/requirements-dev.txt
	docker build -t utils docker

html_tests: FORCE
	$(TEST_DIR)/html_tests.sh

pytests: FORCE
	$(LIB_DIR)/pytests.sh

tests: html_tests 

lint: 
	flake8 $(PYTHONFILES)

prod: $(INCS) $(HTMLFILES) lint tests
	-git commit -a 
	git pull origin master
	git push origin master
