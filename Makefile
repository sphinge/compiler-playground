.PHONY: run test setup freeze clean

run:
	@. venv/bin/activate && \
	python3 -m ezC_blue.compiler

test:
	@. venv/bin/activate && \
	venv/bin/ptw

setup:
	@echo "\033[1;34m### bluecompiler ###\033[0m \t \033[34mSetting up project with Python virtual environment\033[0m"
	@python3 -m venv venv
	@. venv/bin/activate && \
	pip install -e . && \
	pip install -r requirements.txt
	@echo "\033[1;32m### bluecompiler ###\033[0m \t \033[32mSetup complete (dependencies from requirements.txt installed)\033[0m" 

init:
	@echo "\033[1;34m### bluecompiler ###\033[0m \t \033[34mSetting up project with Python virtual environment\033[0m"
	@python3 -m venv venv
	@. venv/bin/activate && \
	pip install -r requirements.txt
	@echo "\033[1;32m### bluecompiler ###\033[0m \t \033[32mSetup complete (dependencies from requirements.txt installed)\033[0m" 

freeze:
	@. venv/bin/activate && \
	pip freeze > requirements.txt
	@echo "\033[1;32m### bluecompiler ###\033[0m \t \033[32mUpdated requirements.txt with pip freeze\033[0m" 

clean:
	@if [ -d venv ]; then rm -rf venv; fi
	@if [ -d .pytest_cache ]; then rm -rf .pytest_cache; fi
	@if [ -d build ]; then rm -rf build; fi
	@if [ -d src/__pycache__ ]; then rm -rf src/__pycache__; fi
	@if [ -d tests/__pycache__ ]; then rm -rf tests/__pycache__; fi
	@if [ -d src/bluecompiler_source.egg-info ]; then rm -rf src/bluecompiler_source.egg-info; fi
	@echo "\033[1;31m### bluecompiler ###\033[0m \t \033[31mCleaned project install\033[0m"

%:
	@:
