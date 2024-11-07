install:
	@echo "Installing dependencies"
	pip3 install -r requirements.txt

scanner:
	@echo "Running scanner tests"
	@echo "Running scanner test: example.txt"
	@python3 -m src scanner example.txt
	@echo "Running scanner test: example_full.txt"
	@python3 -m src scanner example_full.txt
	@echo "Scanner tests completed"

parser:
	@echo "Running parser tests"
	@echo "Running parser test: example1.m"
	@python3 -m src parser example1.m
	@echo "Running parser test: example2.m"
	@python3 -m src parser example2.m
	@echo "Running parser test: example3.m"
	@python3 -m src parser example3.m
	@echo "Parser tests completed"

lint:
	@echo "Running lint"
	ruff format .
	ruff check --fix .