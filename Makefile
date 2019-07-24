NAMESPACE=llimllib
APP=limbo
PYTHON_MAJOR_VERSION=$(shell python -c "import sys; print(sys.version_info[0])")

.PHONY: testall
testall: requirements
	tox

# to run a single file, with debugger support:
# pytest -s test/test_plugins/test_image.py
.PHONY: test
test: install
	LANG=en_US.UTF-8 pytest --cov=limbo --cov-report term-missing test

.PHONY: clean
clean:
	rm -rf build dist limbo.egg-info

.PHONY: run
run: install
	bin/limbo

.PHONY: repl
repl: install
	bin/limbo -t

.PHONY: requirements
requirements:
ifeq (${PYTHON_MAJOR_VERSION},3)
	pip install -r requirements.txt
else
	pip install -r requirements-python2.txt
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

.PHONY: update-requirements
update-requirements:
	rm -rf update-requirements || true
	python -mvenv update-requirements
	update-requirements/bin/pip install -r requirements-to-freeze.txt --upgrade
	update-requirements/bin/pip freeze > requirements.txt
	rm -rf update-requirements
