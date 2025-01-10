install:
	@echo "Installing dependencies"
	pip3 install -r requirements.txt

lint:
	@echo "Running lint"
	ruff format .
	ruff check --fix .

test-all: test-scanner test-parser test-ast test-tc test-interpreter

test-scanner:
	@echo "Running Scanner tests"
	@echo "Running Scanner test: example.txt"
	@python3 -m src scanner example.txt
	@echo "Running Scanner test: example_full.txt"
	@python3 -m src scanner example_full.txt
	@echo "Scanner tests completed"

test-parser:
	@echo "Running Parser tests"
	@echo "Running Parser test: example1.m"
	@python3 -m src parser example1.m
	@echo "Running Parser test: example2.m"
	@python3 -m src parser example2.m
	@echo "Running Parser test: example3.m"
	@python3 -m src parser example3.m
	@echo "Parser tests completed"

test-ast:
	@echo "Running AST tests"
	@echo "Running AST test: example1.m"
	@python3 -m src ast example1.m
	@echo "Running AST test: example2.m"
	@python3 -m src ast example2.m
	@echo "Running AST test: example3.m"
	@python3 -m src ast example3.m
	@echo "AST tests completed"

test-tc:
	@echo "Running Type checker tests"
	@echo "Running Type checker test: control_transfer.m"
	@python3 -m src tc control_transfer.m
	@echo "Running Type checker test: init.m"
	@python3 -m src tc init.m
	@echo "Running Type checker test: opers.m"
	@python3 -m src tc opers.m
	@echo "Type checker tests completed"

test-interpreter:
	@echo "Running Interpreter tests"
	@echo "Running Interpreter test: basic.m"
	@python3 -m src interpreter basic.m
	@echo "Running Interpreter test: fibonacci.m"
	@python3 -m src interpreter fibonacci.m
	@echo "Running Interpreter test: matrix.m"
	@python3 -m src interpreter matrix.m
		@echo "Running Interpreter test: pi.m"
	@python3 -m src interpreter pi.m
		@echo "Running Interpreter test: primes.m"
	@python3 -m src interpreter primes.m
		@echo "Running Interpreter test: sqrt.m"
	@python3 -m src interpreter sqrt.m
		@echo "Running Interpreter test: triangle.m"
	@python3 -m src interpreter triangle.m
	@echo "Interpreter tests completed"