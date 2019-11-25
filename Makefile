all:
	@echo "Available commands:"
	@echo "    init - install dependencies"
	@echo "    sort - sort imports"

init:
	pip install -r requirements.txt

sort:
	isort --recursive .

.PHONY: init sort
