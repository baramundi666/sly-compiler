install:
	@echo "Installing dependencies"
	pip3 install -r requirements.txt

lab1:
	@echo "Running lab1"
	python3 -m src example_full.txt