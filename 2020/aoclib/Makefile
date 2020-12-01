.PHONY: test
test:  ## run the tests to exersize the solution functions
	python -m unittest --verbose


.PHONY: cover
cover:  ## run unit tests with code coverage
	coverage run -m unittest discover
	coverage report

.PHONY: clean
clean:  ## remove generated files from the directory
	-rm -rf __pycache__
	-rm -rf **/__pycache__
	-rm -rf .mypy_cache
	-rm -rf **/.mypy_cache
	-rm **/.coverage
	-rm -rf **/htmlcov


.PHONY: help
help:  ## display help and options
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	    sort | \
	    awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
