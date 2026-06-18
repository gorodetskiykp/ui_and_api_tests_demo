# UI & API Tests Demo

Автоматизированные тесты на Python с использованием **Playwright** (UI) и **httpx + Pydantic** (API).

##  Реализовано по ТЗ

| Требование | Статус |
|------------|--------|
| Развернуть фреймворк с нуля (Playwright + PyTest) | ✅ |
| UI тесты на авторизацию (best practices) | ✅ |
| API тесты POST/GET/PUT (best practices) | ✅ |
| Документация запуска с нуля | ✅ |
| Репозиторий на GitHub | ✅ |

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

##  Запуск локально с нуля

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
```

---

## 🔧 Установка Allure CLI (опционально)

Если хотите использовать `make allure` с автоматическим открытием:

### Linux (Ubuntu/Debian):
```bash
sudo apt-add-repository ppa:qameta/allure
sudo apt update
sudo apt install allure
```

### macOS:
```bash
brew install allure
```

### Windows:
```bash
# Через scoop
scoop install allure

# Или через npm
npm install -g allure-commandline
```

### Или через Docker (кроссплатформенно):
```bash
# Добавьте в Makefile:
allure-docker:
	docker run --rm -v $$(pwd)/reports/allure-results:/data -p 5050:5050 \
		frankescobar/allure-docker-service
```

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
- ✅ Успешный вход с валидными credentials
- ✅ Вход с неверным паролем
- ✅ Вход с несуществующим пользователем
- ✅ Вход с пустыми полями (параметризация)
- ✅ Проверка отображения формы
- ✅ Пробелы в начале/конце логина и пароля
- ✅ Логин/пароль в другом регистре

**Паттерн**: Page Object Model

## API тесты

**API**: https://reqres.in/api

**Покрытие**:
- ✅ `GET /users` — получение списка пользователей
- ✅ `GET /users/{id}` — получение пользователя по ID
- ✅ `POST /users` — создание пользователя
- ✅ `PUT /users/{id}` — обновление пользователя
- ✅ Негативные сценарии: пустые данные, невалидный JSON, несуществующие ресурсы

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

## Отчётность

Для генерации Allure отчёта:

```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## Тестируемые ресурсы

- **UI**: https://the-internet.herokuapp.com/login
- **API**: https://reqres.in/api
```
