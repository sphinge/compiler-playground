.PHONY: run setup install uninstall clean

run:
	@-source venv/bin/activate && \
	python3 lexer.py sample.txt

setup:
	@echo "\033[1;34m### bluecompiler ###\033[0m \t \033[34mSetting up project with Python virtual environment\033[0m"
	@python3 -m venv venv
	@source venv/bin/activate && \
	pip install -r requirements.txt
	@echo "\033[1;32m### bluecompiler ###\033[0m \t \033[32mSetup complete (dependencies from requirements.txt installed)\033[0m" 

install:
	@source venv/bin/activate && \
	pip install $(filter-out $@,$(MAKECMDGOALS)) && \
	pip freeze > requirements.txt
	@echo "\033[1;32m### bluecompiler ###\033[0m \t \033[32mInstalled '$(filter-out $@,$(MAKECMDGOALS))'\033[0m" 

uninstall:
	@source venv/bin/activate && \
	pip uninstall $(filter-out $@,$(MAKECMDGOALS)) && \
	pip freeze > requirements.txt
	@echo "\033[1;32m### bluecompiler ###\033[0m \t \033[32mUninstalled '$(filter-out $@,$(MAKECMDGOALS))'\033[0m" 

clean:
	@rm -rf venv
	@echo "\033[1;31m### bluecompiler ###\033[0m \t \033[31mCleaned project install\033[0m"

%:
	@: