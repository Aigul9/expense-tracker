# Expense-tracker

Проект помогает собрать расходы с различных банковских карт. Поддерживаются 4 банка: Сбер, Тинькофф, Совкомбанк и ВТБ.

## Используемые технологии

- [Python 3.9](https://www.python.org/)
- [Docker 20.10.17](https://docs.docker.com/)
- [PostgreSQL 16](https://www.postgresql.org/)
- [pgAdmin 7](https://www.pgadmin.org/)
- [Metabase 0.48.1](https://www.metabase.com/)

## Список директорий
- ```input```: для выписок по счетам;
- ```py```: python скрипты;
- ```dashboards```: примеры дашбордов

## Инструкция по выгрузке выписок
- **Сбер:** из приложения в формате pdf
- **Тинькофф:** из веба в формате xls
- **Совкомбанк:** из приложения в формате html
- **ВТБ:** из приложения/веба в формате pdf

## Запуск проекта
1. Создать файл ```.env``` на основе шаблона ```.env_template```
2. Положить выписки со счетов в ```input```
3. Выполнить в терминале команду ```docker compose up```
4. Запустить ```main.py```

## Пример заполнения файла .env:
```
# postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=bank_accounts
POSTGRES_HOST=host.docker.internal
POSTGRES_PORT=5434
POSTGRES_SCHEMA=banks

# pgadmin
PGADMIN_EMAIL=pgadmin4@pgadmin.org
PGADMIN_PASSWORD=admin
PGADMIN_PORT=5051

# metabase
METABASE_PORT=3001
```

Теперь можно создавать свои чарты и анализировать доходы и расходы.
