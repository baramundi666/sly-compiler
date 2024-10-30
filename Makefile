install:
	@echo "Installing dependencies"
	pip3 install -r requirements.txt

scanner1:
	@echo "Running scanner test: example.txt"
	python3 -m src example.txt

scanner2:
	@echo "Running scanner test: example_full.txt"
	python3 -m src example_full.txt

lint:
	@echo "Running lint"
	ruff format .
	ruff check --fix .