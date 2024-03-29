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
	pip install -r requirements.txt

.PHONY: install
install: requirements
	python setup.py install
	make clean

.PHONY: publish
publish:
	pandoc -s -w rst README.md -o README.rst
	pip install wheel twine
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm README.rst
	rm -rf dist

.PHONY: flake8
flake8:
	flake8 limbo test

.PHONY: update-requirements
update-requirements:
	rm -rf update-requirements || true
	python -mvenv update-requirements
	update-requirements/bin/pip install -r requirements-to-freeze.txt --upgrade
	update-requirements/bin/pip freeze > requirements.txt
	rm -rf update-requirements
