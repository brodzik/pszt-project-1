all:
	@echo "Available commands:"
	@echo "    init - install dependencies"
	@echo "    sort - sort imports"
	@echo "    test - run tests"

init:
	pip install -r requirements.txt

sort:
	isort --recursive .

test:
	python main.py

.PHONY: init sort test
