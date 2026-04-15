.PHONY: install format lint test run clean logs help

help:
	@echo "Available commands:"
	@echo "  install  - Install dependencies"
	@echo "  format   - Format code with black"
	@echo "  lint     - Run flake8 code check"
	@echo "  test     - Run Django tests"
	@echo "  run      - Run development server"
	@echo "  clean    - Clean temporary files"
	@echo "  logs     - Create logs directory"

install:
	pip install -r requirements.txt

format:
	black .

lint:
	flake8 .

test:
	python manage.py test

run:
	python manage.py runserver

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -delete
	rm -rf .pytest_cache
	rm -rf .coverage

logs:
	mkdir -p logs
