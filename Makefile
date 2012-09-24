# target: help - Display callable targets
help:
	@egrep "^# target:" [Mm]akefile

# target: audit - Audit source code
.PHONY: audit
audit:
	pylama pyga -i E501

# target: test - Run tests
.PHONY: test
test: setup.py
	python setup.py test

# target: clean - Clean repo
.PHONY: clean
clean:
	find $(CURDIR) -name "*.pyc" -delete
	find $(CURDIR) -name "*.orig" -delete
