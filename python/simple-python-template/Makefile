PROJECT_NAME := project_name
VERSION ?= v0.0.1

.PHONY: all enter help

all: version help

setup: ## setup environment
	@poetry install
	@poetry shell

run: ## run script
	@poetry run python main.py

version: ## Version Info
    @echo "$(PROJECT_NAME):$(VERSION)\n"

help: ## Show Command Info
    @echo "Command List:"
    @grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
        awk 'BEGIN {FS = ":.*?## "}; {printf " %-20s %s\n", $$1, $$2}'