.PHONY: run
run:  ## run the program using default options
	python solve.py


.PHONY: test
test:  ## run the tests to exersize the solution functions
	python solve.py test.txt 3 2


.PHONY: format
format:  ## format the source code according to black
	black --line-length 100 --target-version py37 *.py
	isort *.py


.PHONY: lint
lint:  ## use flake8 to lint the code
	flake8 *.py
	mypy *.py


.PHONY: pre-commit
pre-commit: lint format  ## perform pre-commit checks to all code


.PHONY: clean
clean:  ## remove generated files from the directory
	-rm *.dot *.pdf


.PHONY: help
help:  ## display help and options
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	    sort | \
	    awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
