.PHONY: test
test: install
	nosetests -s --nologcapture

.PHONY: clean
clean:
	rm -rf build dist slask.egg-info

.PHONY: run
run: install
	bin/slask

.PHONY: install
install:
	python setup.py install
	make clean
