.PHONY: solve
solve:  ## run the program using default options
	python solve.py drone.int


.PHONY: test
test:  ## run the program using test options
	python solve.py drone.int 10 10 --display


.PHONY: tests
tests:  ## run unit tests to exersize the solution functions
	python geometry.py --verbose


.PHONY: format
format:  ## format the source code according to black
	black --line-length 100 --target-version py37 *.py
	isort *.py


.PHONY: lint
lint:  ## use flake8 to lint the code
	flake8 *.py
	#mypy *.py


.PHONY: pre-commit
pre-commit: lint format  ## perform pre-commit checks to all code


.PHONY: clean
clean:  ## remove generated files from the directory
	-rm -rf __pycache__
	-rm -rf .mypy_cache
	-rm .coverage
	-rm -rf htmlcov


.PHONY: help
help:  ## display help and options
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	    sort | \
	    awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
