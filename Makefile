.PHONY: install run test format lint clean

install:
	pip install -r requirements.txt
	pre-commit install

run:
	streamlit run app/main.py

test:
	pytest tests/

format:
	black .
	isort .

lint:
	ruff check .
	mypy src/ app/

clean:
	rm -rf __pycache__ .pytest_cache logs/*.log
