@echo off
REM Django 学生管理系统便捷命令脚本

if "%1"=="" goto help
if "%1"=="install" goto install
if "%1"=="dev" goto dev
if "%1"=="run" goto run
if "%1"=="test" goto test
if "%1"=="lint" goto lint
if "%1"=="format" goto format
if "%1"=="clean" goto clean
if "%1"=="migrate" goto migrate
goto help

:help
echo 可用命令:
echo   scripts\make.bat install    - 安装项目依赖
echo   scripts\make.bat dev        - 安装开发依赖
echo   scripts\make.bat run        - 启动开发服务器
echo   scripts\make.bat test       - 运行测试
echo   scripts\make.bat lint       - 运行代码检查 (flake8)
echo   scripts\make.bat format     - 格式化代码 (black)
echo   scripts\make.bat clean      - 清理临时文件
echo   scripts\make.bat migrate    - 执行数据库迁移
goto end

:install
pip install -r requirements.txt
goto end

:dev
pip install -r requirements-dev.txt
goto end

:run
python manage.py runserver
goto end

:test
python manage.py test tests.test_settings
goto end

:lint
flake8 .
goto end

:format
black .
isort .
goto end

:clean
del /s /q *.pyc 2>nul
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
goto end

:migrate
python manage.py makemigrations
python manage.py migrate
goto end

:end
