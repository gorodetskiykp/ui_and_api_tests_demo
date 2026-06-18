# UI & API Tests Demo

Автоматизированные тесты на Python с использованием **Playwright** (UI) и **httpx + Pydantic** (API).

[![Test Pipeline](https://github.com/gorodetskiykp/ui_and_api_tests_demo/actions/workflows/test.yml/badge.svg)](https://github.com/gorodetskiykp/ui_and_api_tests_demo/actions/workflows/test.yml)
[![Allure Report](https://img.shields.io/badge/Allure-Report-blue)](https://gorodetskiykp.github.io/ui_and_api_tests_demo/)

## Содержание

- [Реализовано по ТЗ](#реализовано-по-тз)
- [Стек технологий](#стек-технологий)
- [Запуск локально с нуля](#запуск-локально-с-нуля)
- [Makefile команды](#makefile-команды)
- [Запуск через Docker](#запуск-через-docker)
- [Структура проекта](#структура-проекта)
- [UI тесты](#ui-тесты)
- [API тесты](#api-тесты)
- [Best Practices](#best-practices)
- [Тестируемые ресурсы](#тестируемые-ресурсы)

## Реализовано по ТЗ

| Требование | Статус |
|------------|--------|
| Развернуть фреймворк с нуля (Playwright + PyTest) | Выполнено |
| UI тесты на авторизацию (best practices) | Выполнено |
| API тесты POST/GET/PUT (best practices) | Выполнено |
| Документация запуска с нуля | Выполнено |
| Репозиторий на GitHub | Выполнено |

## Стек технологий

- **Python 3.10+**
- **pytest** — тестовый фреймворк
- **pytest-playwright** — UI тестирование
- **httpx** — HTTP клиент для API тестов
- **pydantic** — валидация моделей данных
- **loguru** — логирование
- **allure-pytest** — отчёты
- **Faker** — генерация тестовых данных
- **ruff** — линтер

## Запуск локально с нуля

### 1. Клонировать репозиторий

```bash
git clone https://github.com/gorodetskiykp/ui_and_api_tests_demo.git
cd ui_and_api_tests_demo
```

### 2. Создать виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate          # Linux/Mac
# или
venv\Scripts\activate             # Windows
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Установить браузеры Playwright

```bash
playwright install chromium

# Для Linux дополнительно:
playwright install-deps chromium
```

### 5. Настроить переменные окружения

```bash
cp .env.example .env
```

Содержимое `.env`:
```env
BASE_URL=https://the-internet.herokuapp.com
API_BASE_URL=https://reqres.in/api
VALID_USERNAME=tomsmith
VALID_PASSWORD=SuperSecretPassword!
HEADLESS=true
```

### 6. Запустить тесты

```bash
# Все тесты
pytest

# Только UI тесты
pytest tests/ui/ -m ui

# Только API тесты
pytest tests/api/ -m api

# UI тесты с открытым браузером
pytest tests/ui/ -m ui --headed

# С Allure отчётом
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## Makefile команды

Для удобства доступны команды через `make`:

### Установка

```bash
make install          # Установить зависимости и браузеры
```

### Тесты

```bash
make test             # Все тесты
make test-ui          # UI тесты (headless)
make test-ui-headed   # UI тесты с открытым браузером
make test-api         # API тесты
make test-parallel    # Параллельный запуск (4 процесса)
```

### Качество кода

```bash
make lint             # Проверить код с ruff
make lint-fix         # Автоматически исправить ошибки
make format           # Отформатировать код
make format-check     # Проверить форматирование
```

### Отчёты

```bash
make allure           # Сгенерировать и открыть Allure отчёт
make allure-generate  # Только сгенерировать отчёт (без открытия)
```

### Очистка

```bash
make clean            # Очистить временные файлы
make clean-all        # Очистить всё (включая кэш)
```

### Справка

```bash
make help             # Показать все доступные команды
```

### Docker

```bash
make docker-build           # Собрать Docker образ
make docker-test            # Запустить все тесты в Docker
make docker-ui              # Запустить UI тесты в Docker
make docker-api             # Запустить API тесты в Docker
make docker-allure          # Тесты + Allure сервер (порт 5050)
make docker-allure-generate # Только генерация Allure отчёта
make docker-shell           # Войти в контейнер для отладки
make docker-clean           # Остановить и удалить контейнеры
make docker-logs            # Показать логи последнего запуска
```

### Пример использования

```bash
# Полный цикл: установка → тесты → отчёт
make install
make test
make allure

# Или одной командой (если allure CLI установлен)
make install && make test && make allure
```

> **Примечание**: Для команды `make allure` требуется установленный [Allure CLI](https://docs.qameta.io/allure/#_installing_a_commandline).
> Альтернатива: используйте `make allure-generate` и откройте `reports/allure-report/index.html` в браузере.

#### macOS

```bash
brew install allure
```

#### Windows

```bash
# Через scoop
scoop install allure

# Или через npm
npm install -g allure-commandline
```

## Запуск через Docker

Для запуска тестов в изолированном окружении используется Docker. Все зависимости (Python, Playwright, Allure CLI) уже установлены в образе.

### Предварительные требования

- Docker Engine 20.10+
- Docker Compose 2.0+

### Сборка образа

```bash
docker compose build
# или
make docker-build
```

### Запуск тестов

```bash
# Все тесты
docker compose run --rm tests
make docker-test

# Только UI тесты
docker compose run --rm ui-tests
make docker-ui

# Только API тесты
docker compose run --rm api-tests
make docker-api
```

### Allure отчёты

**Вариант 1: С веб-сервером (рекомендуется)**

```bash
docker compose run --rm allure
make docker-allure
```

Отчёт будет доступен по адресу: http://localhost:5050

**Вариант 2: Только генерация отчёта**

```bash
docker compose run --rm allure-generate
make docker-allure-generate
```

Отчёт сохранится в `reports/allure-report/index.html` — откройте его в браузере.

### Отладка

Войти в контейнер для интерактивной работы:

```bash
docker compose run --rm tests bash
make docker-shell
```

Внутри контейнера можно запускать любые команды:

```bash
pytest tests/ui/test_login.py::TestLogin::test_successful_login -v -s
```

### Логи

```bash
docker compose logs --tail=100
make docker-logs
```

### Очистка

```bash
docker compose down
make docker-clean
```

### Переменные окружения

Docker автоматически загружает `.env` файл из корня проекта:

```env
BASE_URL=https://the-internet.herokuapp.com
API_BASE_URL=https://reqres.in/api
VALID_USERNAME=tomsmith
VALID_PASSWORD=SuperSecretPassword!
HEADLESS=true
```

### Тома (Volumes)

Отчёты и логи сохраняются на хост-машине:

- `./reports` → `/app/reports` — Allure отчёты
- `./logs` → `/app/logs` — логи тестов

## Структура проекта

```
ui_and_api_tests_demo/
├── config/
│   └── settings.py              # Конфигурация через pydantic-settings
├── tests/
│   ├── ui/
│   │   ├── pages/
│   │   │   ├── base_page.py     # Базовый Page Object
│   │   │   └── login_page.py    # Page Object для логина
│   │   ├── conftest.py          # UI фикстуры
│   │   └── test_login.py        # UI тесты авторизации
│   └── api/
│       ├── clients/
│       │   ├── base_client.py   # Базовый HTTP клиент
│       │   └── users_client.py  # Клиент для /users
│       ├── schemas/
│       │   └── user_schema.py   # Pydantic модели
│       ├── conftest.py          # API фикстуры
│       ├── test_users_get.py    # GET тесты
│       ├── test_users_post.py   # POST тесты
│       └── test_users_put.py    # PUT тесты
├── utils/
│   └── logger.py                # Настройка loguru
├── .env.example
├── .gitignore
├── pytest.ini
├── pyproject.toml               # Конфигурация ruff
├── requirements.txt
├── Makefile
└── README.md
```

## UI тесты

**Сайт**: https://the-internet.herokuapp.com/login

**Покрытие**:
- Успешный вход с валидными credentials
- Вход с неверным паролем
- Вход с несуществующим пользователем
- Вход с пустыми полями (параметризация)
- Проверка отображения формы
- Пробелы в начале/конце логина и пароля
- Логин/пароль в другом регистре

**Паттерн**: Page Object Model

## API тесты

**API**: https://reqres.in/api

**Покрытие**:
- `GET /users` — получение списка пользователей
- `GET /users/{id}` — получение пользователя по ID
- `POST /users` — создание пользователя
- `PUT /users/{id}` — обновление пользователя
- Негативные сценарии: пустые данные, невалидный JSON, несуществующие ресурсы

**Паттерн**: API Client + Pydantic валидация ответов

## Best Practices

### Архитектура
- **Page Object Model** — изоляция локаторов от тестов
- **API Client паттерн** — инкапсуляция HTTP-логики
- **Разделение UI и API тестов** — независимые модули

### Код
- **Типизация** (type hints) во всех модулях
- **Pydantic модели** для валидации данных и ответов API
- **Константы HTTP статусов** (`http.HTTPStatus.OK` вместо `200`)
- **Конфигурация через `.env`** — секреты не в коде
- **Логирование** через loguru с ротацией

### Тесты
- **Фикстуры pytest** с правильными scope (`session`, `function`)
- **Параметризация** тестов через `@pytest.mark.parametrize`
- **Маркеры** для группировки (`@pytest.mark.ui`, `@pytest.mark.smoke`)
- **Allure декораторы** (`@allure.title`, `@allure.severity`, `@allure.step`)
- **Автоскриншоты** при падении UI тестов
- **Faker** для генерации тестовых данных

### Инфраструктура
- **ruff** для линтинга и форматирования
- **`.gitignore`** для исключения временных файлов
- **`pytest.ini`** с централизованной конфигурацией

## Тестируемые ресурсы

- **UI**: https://the-internet.herokuapp.com/login
- **API**: https://reqres.in/api