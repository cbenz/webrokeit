.PHONY: clean flake8

all: clean flake8

clean:
	find -name "*.pyc" | xargs rm -f
	rm -rf cache/*

flake8:
	flake8 --max-line-length=120 --ignore=E123,E128,E251 webrokeit sample_handlers scripts
