.PHONY: help install test test-ui test-ui-headed test-api test-all test-parallel lint format allure clean

# Цвета для вывода
GREEN  := \033[0;32m
CYAN   := \033[0;36m
NC     := \033[0m

help: ## Показать справку
	@echo ""
	@echo "$(CYAN)Доступные команды:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

install: ## Установить зависимости и браузеры
	pip install -r requirements.txt
	playwright install chromium

test: ## Запустить все тесты
	pytest

test-ui: ## Запустить UI тесты (headless)
	pytest tests/ui/ -m ui

test-ui-headed: ## Запустить UI тесты с открытым браузером
	pytest tests/ui/ -m ui --headed

test-api: ## Запустить API тесты
	pytest tests/api/ -m api

test-parallel: ## Запустить тесты параллельно (4 процесса)
	pytest -n 4

lint: ## Проверить код с ruff
	ruff check .

lint-fix: ## Автоматически исправить ошибки ruff
	ruff check . --fix

format: ## Отформатировать код с ruff
	ruff format .

format-check: ## Проверить форматирование
	ruff format --check .

allure: ## Сгенерировать и открыть Allure отчёт
	rm -rf reports/allure-results
	pytest --alluredir=reports/allure-results
	@echo ""
	@echo "$(GREEN)Отчёт сгенерирован в reports/allure-results$(NC)"
	@echo "$(CYAN)Для просмотра выполните: allure serve reports/allure-results$(NC)"
	@echo ""

allure-generate: ## Только сгенерировать Allure отчёт (без открытия)
	rm -rf reports/allure-results
	pytest --alluredir=reports/allure-results
	allure generate reports/allure-results -o reports/allure-report --clean
	@echo ""
	@echo "$(GREEN)Отчёт сгенерирован в reports/allure-report$(NC)"
	@echo "$(CYAN)Откройте reports/allure-report/index.html в браузере$(NC)"
	@echo ""

clean: ## Очистить временные файлы и кэш
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf reports
	rm -rf logs
	rm -rf .ruff_cache
	@echo "$(GREEN)Очистка завершена$(NC)"

# Кроссплатформенная очистка (для Windows)
clean-all: ## Очистить всё (включая venv)
	@echo "$(CYAN)🧹 Очистка временных файлов...$(NC)"
	rm -rf .pytest_cache __pycache__ reports logs .ruff_cache allure-results allure-report
	@echo "$(GREEN)Очистка завершена$(NC)"
	@echo ""
	@echo "$(CYAN)Для удаления venv выполните вручную:$(NC)"
	@echo "   rm -rf venv  (Linux/Mac)"
	@echo "   rmdir /s venv  (Windows)"