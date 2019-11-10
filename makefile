# A template makefile that works for static websites.
# Need to export as ENV var
export TEMPLATE_DIR = templates
PTML_DIR = html_src
UTILS_DIR = utils
REPO = socnet
DOCKER_DIR = docker
API_DIR = APIServer

INCS = $(TEMPLATE_DIR)/head.txt $(TEMPLATE_DIR)/logo.txt $(TEMPLATE_DIR)/menu.txt

HTMLFILES = $(shell ls $(PTML_DIR)/*.ptml | sed s/.ptml/.html/ | sed 's/html_src\///')

FORCE:

%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 $(UTILS_DIR)/html_checker.py $< 
	$(UTILS_DIR)/html_include.awk <$< >$@
	git add $@

local: $(HTMLFILES)

# we need a `tests` target for prod to run!
prod: $(INCS) $(HTMLFILES)
	make tests
	-git commit -a 
	git pull origin master
	git push origin master

tests: 
	cd APIServer; make tests

api_server:
	cd APIServer; make api_server

submods:
	git submodule foreach 'git pull origin master'

# dev container has dev tools
dev_container: $(DOCKER_DIR)/Dockerfile # $(DOCKER_DIR)/requirements.txt $(DOCKER_DIR)/requirements-dev.txt
	docker build -t gcallah/$(REPO)-dev docker
	
nocrud:
	rm *~
	rm .*swp
	rm $(PTML_DIR)/*~
	rm $(PTML_DIR)/.*swp

clean:
	touch $(PTML_DIR)/*.ptml; make local
