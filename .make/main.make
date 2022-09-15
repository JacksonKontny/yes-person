MODULE_MAIN=.

##@ MAIN

run: ## Run the app                                                          
	PYTHONPATH=${MODULE_MAIN}/:${PYTHONPATH} pipenv run python src/main.py
