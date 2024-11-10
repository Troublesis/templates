# Project Configuration
VERSION ?= v0.0.1-dev
DOCKER_COMPOSE_FILE ?= compose.dev.yml
DOCKERFILE ?= Dockerfile.dev

PROJECT_NAME ?= python-docker-template
PYTHON_VERSION ?= 3.9.19
POETRY_VERSION ?= 1.8.3

NAME := troublesis
EMAIL := bamboo5320@gmail.com

# Colors
BLUE := \033[1;34m
GREEN := \033[1;32m
RED := \033[1;31m
YELLOW := \033[1;33m
NC := \033[0m

# Docker Compose Environment
COMPOSE_ENV := PROJECT_NAME=$(PROJECT_NAME) VERSION=$(VERSION)

.PHONY: all init git_init setup push up enter clean local cz_setup acp test help

# Default target
all: help

# Project Initialization
init:  ## 初始化项目
	@echo "$(BLUE)Initializing project: $$(basename $$(pwd))$(NC)"
	@# Set PYTHONPATH
	@export PYTHONPATH="$$PYTHONPATH:$$(pwd)/src"

	@# Create .env file
	@echo "$(GREEN)Creating environment variable file...$(NC)"
	@echo "DEBUG=true" > .env

	@# Python environment setup
	@if [ -d ".venv" ]; then \
		echo "$(YELLOW).venv directory already exists$(NC)"; \
	else \
		if command -v pyenv >/dev/null 2>&1; then \
			echo "$(GREEN)Setting up Python environment...$(NC)"; \
			if pyenv exec poetry env use $(PYTHON_VERSION); then \
				pyenv exec poetry lock && \
				pyenv exec poetry install && \
				if command -v pre-commit >/dev/null 2>&1; then \
					pre-commit autoupdate && \
					pre-commit install --hook-type commit-msg --hook-type pre-push && \
					pre-commit run --all-files; \
				else \
					echo "$(RED)Warning: pre-commit is not installed$(NC)"; \
				fi; \
			else \
				echo "$(RED)Warning: Poetry command failed$(NC)"; \
			fi; \
		else \
			echo "$(RED)Warning: pyenv is not installed, skipping Python environment setup$(NC)"; \
		fi; \
	fi
	@echo "$(GREEN)Project initialization complete$(NC)"

git_init: ## 初始化 Git 仓库
	@echo "$(BLUE)Initializing Git repository$(NC)"
	@rm -rf .git
	@git init
	@git config user.name "${NAME}"
	@git config user.email "${EMAIL}"
	@echo "$(GREEN)Git repository initialized$(NC)"

# Docker Operations
setup: ## 构建 Docker 镜像并启动容器
	@echo "$(BLUE)Setting up $(PROJECT_NAME):$(VERSION) using $(DOCKERFILE)$(NC)"
	@$(COMPOSE_ENV) DOCKER_BUILDKIT=1 DOCKERFILE=$(DOCKERFILE) docker compose -f $(DOCKER_COMPOSE_FILE) build \
		--build-arg POETRY_VERSION=$(POETRY_VERSION) || \
		(echo "$(RED)Docker compose build failed$(NC)" && exit 1)
	@$(COMPOSE_ENV) docker compose -f $(DOCKER_COMPOSE_FILE) up -d || \
		(echo "$(RED)Docker compose up failed$(NC)" && exit 1)

push: ## 推送 Docker 镜像到仓库
	@echo "$(BLUE)Pushing Docker image: $(PROJECT_NAME):$(VERSION)$(NC)"
	@docker push $(PROJECT_NAME):$(VERSION) || \
		(echo "$(RED)Push failed$(NC)" && exit 1)
	@echo "$(GREEN)Image pushed successfully$(NC)"

up: ## 启动 Docker 容器
	@echo "$(BLUE)Starting project: $(PROJECT_NAME)$(NC)"
	@$(COMPOSE_ENV) docker compose -f $(DOCKER_COMPOSE_FILE) up -d || \
		(echo "$(RED)Failed to start containers$(NC)" && exit 1)
	@echo "$(GREEN)Project running in background$(NC)"

enter: ## 进入 Docker 容器
	@echo "$(YELLOW)Entering container shell...$(NC)"
	@docker exec -it $(PROJECT_NAME) sh || \
		(echo "$(RED)Failed to enter container$(NC)" && \
		docker logs $(PROJECT_NAME) && exit 1)

clean: ## 清除 Docker 容器
	@echo "$(BLUE)Cleaning up project$(NC)"
	@docker stop $(PROJECT_NAME) 2>/dev/null || true
	@$(COMPOSE_ENV) docker compose -f $(DOCKER_COMPOSE_FILE) down
	@docker rmi $(PROJECT_NAME):$(VERSION) 2>/dev/null || true
	@docker network prune
	@echo "$(GREEN)Cleanup complete$(NC)"

# Development Environment
local: ## 设定本地项目环境
	@echo "$(BLUE)Setting up local development environment$(NC)"
	@export PYTHONPATH="${PYTHONPATH}:$PWD/src"
	@pyenv exec poetry env use $(PYTHON_VERSION)
	@poetry install
	@poetry shell
	@echo "$(GREEN)Local environment ready$(NC)"

cz_setup: ## 设定 cz commit
	@echo "$(BLUE)Setting up Git commit workflow$(NC)"
	@poetry run pre-commit autoupdate
	@poetry run pre-commit install --hook-type commit-msg --hook-type pre-push
	@echo "$(GREEN)Git commit workflow configured$(NC)"

acp: ## Git --all push
	@git status
	@read -p "Proceed with commit? (y/n): " confirm && \
	if [ "$$confirm" = "y" ]; then \
		git add --all && \
		git status && \
		pre-commit run --all-files && \
		cz commit && git push; \
	else \
		echo "$(YELLOW)Commit cancelled$(NC)"; \
	fi

# Testing
test: ## 测试
	@echo "$(BLUE)Running tests with coverage$(NC)"
	@docker exec $(PROJECT_NAME) python3 -m poetry run pytest tests \
		--cov=/var/task \
		--cov-report term-missing \
		--cov-report html:coverage_html || \
		(echo "$(RED)Tests failed$(NC)" && exit 1)
	@echo "$(GREEN)Tests completed$(NC)"

# Help
help: ## 显示帮助信息
	@echo "$(BLUE)可用命令:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; \
		{printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
