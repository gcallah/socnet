# Need to export as ENV var
export TEST_DIR = tests
export TEST_DATA = test_data
export CODE_DIR = .
export HTML_DIR = .
export DATA_DIR = $(CODE_DIR)/data
export DOCKER_DIR = docker
PYTHONFILES = $(shell ls *.py)
PYTHONFILES += $(shell ls $(LIB_DIR)/*.py)
PSHELL_SCRIPTS = $(shell ls *.sh | sed -e 's/.sh/.ps1')
PSHELL_SCRIPTS += $(shell ls $(TEST_DIR)/*.sh | sed -e 's/.sh/.ps1')
BASH2PS = python bash_to_powershell.py

FORCE:

container: $(DOCKER_DIR)/Dockerfile  $(DOCKER_DIR)/requirements.txt
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
