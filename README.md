# Сервис терминологии (Справочники)

Тестовое задание на Django.

## Как запустить проект локально

1. Клонировать репозиторий и перейти в папку:
   ```bash
   git clone <ссылка_на_ваш_репозиторий>
   cd terminology_service
   ```
2. Создать и активировать виртуальное окружение:
   ```bash
   python -m venv .venv
   # Для Windows:
   .venv\Scripts\activate
   # Для macOS/Linux:
   source .venv/bin/activate
   ```
3. Установить зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Применить миграции базы данных:
   ```bash
   python manage.py migrate
   ```
5. Создать суперпользователя для панели администратора:
   ```bash
   python manage.py createsuperuser
   ```
6. Запустить локальный сервер:
   ```bash
   python manage.py runserver
   ```

## Документация и проверка

* **Интерактивная документация Swagger UI:** `http://127.0.0.1:8000`
* **Панель администратора (на русском языке):** `http://127.0.0.1:8000/admin`

## Запуск тестов

Для запуска автоматических тестов (на базе `pytest`) выполните:
```bash
pytest
```
