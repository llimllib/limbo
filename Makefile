NAMESPACE=llimllib
APP=limbo

.PHONY: testall
testall: requirements
	tox

.PHONY: test
test: install
	LANG=en_US.UTF-8 pytest --cov=limbo --cov-report term-missing

.PHONY: clean
clean:
	rm -rf build dist limbo.egg-info

.PHONY: run
run: install
	bin/limbo

.PHONY: repl
repl: install
	bin/limbo -t

# non-empty if we're on python 2.6
PYTHON2_6 = $(shell python --version 2>&1 | grep 2.6)

.PHONY: requirements
requirements:
	pip install -r requirements.txt
ifneq ($(PYTHON2_6), )
	pip install -r requirements-2.6.txt
endif

.PHONY: install
install: requirements
	python setup.py install
	make clean

.PHONY: publish
publish:
	pandoc -s -w rst README.md -o README.rst
	python setup.py sdist upload
	rm README.rst

.PHONY: flake8
flake8:
	flake8 limbo test

NAMESPACE=petergrace
APP=limbo

.PHONY: docker_build
docker_build:
	docker build -f Dockerfile.dev -t ${NAMESPACE}/${APP} .

.PHONY: docker_run
docker_run:
	docker run -d -e SLACK_TOKEN=${SLACK_TOKEN} ${NAMESPACE}/${APP}

.PHONY: docker_stop
docker_clean:
	docker stop $(docker ps -a -q  --filter ancestor=petergrace/limbo --format="{{.ID}}")
