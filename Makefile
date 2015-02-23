.PHONY: test
test: install
	nosetests -s --nologcapture

.PHONY: clean
clean:
	rm -rf build dist slask.egg-info

.PHONY: run
run: install
	bin/slask

.PHONY: repl
repl: install
	bin/slask -t

.PHONY: install
install:
	python setup.py install
	make clean
