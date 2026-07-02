.PHONY: install test lint run clean

install:
	pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest tests/

lint:
	flake8 src app tests
	black --check src app tests

run:
	streamlit run app/main.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
