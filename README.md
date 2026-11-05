# \# modern-datastack-petshop

# 

# Data Engineering project for a pet shop.

# 

# \## Project description

# 

# Проєкт призначений для збору, зберігання та обробки даних інтернет-магазину товарів для домашніх тварин. Для зберігання даних використовується PostgreSQL, а для їх перетворення та підготовки аналітичних моделей використовується dbt Core.

# 

# \## Technologies

# 

# \- Python

# \- PostgreSQL 15

# \- Docker

# \- dbt Core

# \- dbt-postgres

# \- SQL / Jinja

# 

# \## Project structure

# 

# ```text

# modern-datastack-petshop/

# ├── data\_generator.py

# ├── load\_to\_dwh.py

# ├── docker-compose.yml

# ├── requirements.txt

# ├── README.md

# └── ecommerce\_dbt/

# &#x20;   ├── models/

# &#x20;   │   ├── staging/

# &#x20;   │   │   ├── src\_ecommerce.yml

# &#x20;   │   │   ├── stg\_users.sql

# &#x20;   │   │   ├── stg\_orders.sql

# &#x20;   │   │   └── stg\_products.sql

# &#x20;   │   └── marts/

# &#x20;   │       ├── dim\_users.sql

# &#x20;   │       ├── dim\_products.sql

# &#x20;   │       └── fct\_orders.sql

# &#x20;   ├── dbt\_project.yml

# &#x20;   └── .gitignore

# ```

# 

# \## Data transformation

# 

# Для обробки даних створено два рівні моделей:

# 

# \- \*\*Staging:\*\* підготовка та очищення початкових даних із таблиць PostgreSQL.

# \- \*\*Marts:\*\* створення аналітичних таблиць за схемою «Зірка».

# 

# Створені моделі:

# \- `stg\_users`, `stg\_orders`, `stg\_products`

# \- `dim\_users`, `dim\_products`, `fct\_orders`

# 

# \## Database

# 

# Дані зберігаються в PostgreSQL у базі `petshop\_dwh`.

# 

# Початкові таблиці розміщені у схемі `raw`, результати перетворень dbt зберігаються у схемі `analytics`.

# 

# \## Running dbt

# 

# Для запуску моделей необхідно перейти до папки `ecommerce\_dbt`, налаштувати локальний `profiles.yml` та виконати:

# 

# ```bash

# dbt debug

# dbt run

# ```



