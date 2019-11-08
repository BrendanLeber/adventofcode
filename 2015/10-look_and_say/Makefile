.PHONY: run
run:  ## run the program using default options
	python solver.py input.txt


.PHONY: test
test:  ## run the program using test data input
	python solver.py test.txt


.PHONY: format
format:  ## format the source code according to black
	black --line-length 100 --target-version py37 *.py
	isort *.py


.PHONY: lint
lint:  ## use flake8 to lint the code
	flake8 *.py


.PHONY: pre-commit
pre-commit: lint format  ## perform pre-commit checks to all code


.PHONY: help
help:  ## display help and options
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	    sort | \
	    awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
