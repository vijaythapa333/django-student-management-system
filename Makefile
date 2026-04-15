.PHONY: help install dev run test lint format clean migrate

help:
	@echo "可用命令:"
	@echo "  make install    - 安装项目依赖"
	@echo "  make dev        - 安装开发依赖"
	@echo "  make run        - 启动开发服务器"
	@echo "  make test       - 运行测试"
	@echo "  make lint       - 运行代码检查 (flake8)"
	@echo "  make format     - 格式化代码 (black)"
	@echo "  make clean      - 清理临时文件"
	@echo "  make migrate    - 执行数据库迁移"

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements-dev.txt

run:
	python manage.py runserver

test:
	python manage.py test

lint:
	flake8 .

format:
	black .
	isort .

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

migrate:
	python manage.py makemigrations
	python manage.py migrate
