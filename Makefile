install:
	@echo "Installing dependencies"
	pip3 install -r requirements.txt

scanner:
	@echo "Running Scanner tests"
	@echo "Running Scanner test: example.txt"
	@python3 -m src scanner example.txt
	@echo "Running Scanner test: example_full.txt"
	@python3 -m src scanner example_full.txt
	@echo "Scanner tests completed"

parser:
	@echo "Running Parser tests"
	@echo "Running Parser test: example1.m"
	@python3 -m src parser example1.m
	@echo "Running Parser test: example2.m"
	@python3 -m src parser example2.m
	@echo "Running Parser test: example3.m"
	@python3 -m src parser example3.m
	@echo "Parser tests completed"

parser:
	@echo "Running AST tests"
	@echo "Running AST test: example1.tree"
	@python3 -m src ast example1.tree
	@echo "Running AST test: example2.tree"
	@python3 -m src ast example2.tree
	@echo "Running AST test: example3.tree"
	@python3 -m src ast example3.tree
	@echo "AST tests completed"

lint:
	@echo "Running lint"
	ruff format .
	ruff check --fix .