# Modern Data Stack Pet Shop

A small end-to-end data engineering project for a pet shop. The project demonstrates how raw business data can be generated, loaded into a PostgreSQL data warehouse, transformed into analytics-ready models with dbt, and orchestrated with Apache Airflow.

## Project overview

The pipeline follows an ELT approach:

1. **Extract and load:** Python scripts generate sample pet shop data and load it into PostgreSQL.
2. **Transform:** dbt prepares the raw data through staging models and analytical marts.
3. **Orchestrate:** Apache Airflow runs the data generation/loading task first, then starts the dbt transformations.

## Architecture

```text
Python data generator
        |
        v
Python loader
        |
        v
PostgreSQL (petshop_dwh)
        |
        | raw schema
        v
dbt staging models
        |
        v
dbt analytical marts
        |
        v
analytics schema

Apache Airflow orchestrates the workflow:
extract_and_load_raw_data
        |
        v
dbt_run_transformations
```

## Technology stack

| Technology | Purpose |
|---|---|
| Python | Generate and load sample data |
| PostgreSQL 15 | Data warehouse |
| Docker | Run the database and Airflow services |
| Apache Airflow | Schedule and orchestrate pipeline tasks |
| dbt Core | Transform raw data into analytical models |
| dbt-postgres | Connect dbt to PostgreSQL |
| SQL / Jinja | Define transformation logic |

## Data model

The generator creates the following sample datasets:

| Dataset | Number of records |
|---|---:|
| `pet_owners` | 50 |
| `brands` | 10 |
| `pet_supplies` | 100 |
| `transactions` | 500 |
| `loyalty_points` | 500 |
| `reviews` | 100 |

Raw source tables are stored in the PostgreSQL `raw` schema. dbt builds the transformed models in the `analytics` schema.

## dbt models

The dbt project contains two layers:

**Staging**
- `stg_users`
- `stg_orders`
- `stg_products`

These models prepare the source data for further analysis.

**Marts**
- `dim_users`
- `dim_products`
- `fct_orders`

These models form an analytical star-schema-style layer with dimensions and a fact table.

## Airflow pipeline

The DAG is defined in `airflow/dags/ecommerce_pipeline.py`.

| Task | Operator | Responsibility |
|---|---|---|
| `extract_and_load_raw_data` | PythonOperator | Runs the data generator and PostgreSQL loader |
| `dbt_run_transformations` | BashOperator | Runs `dbt run` for the dbt project |

The task dependency ensures that dbt starts only after the raw data loading task succeeds. The DAG uses the `@daily` schedule and has catchup disabled. It can also be triggered manually from the Airflow web interface.

## Project structure

```text
modern-datastack-petshop/
├── airflow/
│   └── dags/
│       ├── ecommerce_pipeline.py
│       └── scripts/
│           ├── data_generator.py
│           └── load_to_dwh.py
├── ecommerce_dbt/
│   ├── models/
│   │   ├── staging/
│   │   └── marts/
│   ├── dbt_project.yml
│   └── profiles.yml       # local configuration; do not commit credentials
├── data_generator.py
├── load_to_dwh.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Getting started

### 1. Start PostgreSQL

From the project root, start the database service:

```bash
docker compose up -d dwh_postgres
```

The Compose configuration exposes PostgreSQL on port `5432`.

### 2. Configure dbt

Create or update `ecommerce_dbt/profiles.yml` for your environment. The profile should use the PostgreSQL connection details configured for your database. Keep local credentials out of version control.

### 3. Run dbt manually

With dbt Core and the PostgreSQL adapter installed, run:

```bash
dbt debug --project-dir ecommerce_dbt --profiles-dir ecommerce_dbt
dbt run --project-dir ecommerce_dbt --profiles-dir ecommerce_dbt
```

### 4. Run the Airflow pipeline

Start the Airflow environment with the project DAG directory and dbt project available to the Airflow container. Ensure the container has the Python dependencies used by the scripts, the dbt Core and PostgreSQL adapter packages, and network access to PostgreSQL.

Open [http://localhost:8080](http://localhost:8080), enable `ecommerce_elt_pipeline`, and trigger it manually. In the Airflow Grid or Graph view, check that both tasks complete successfully.

## Configuration notes

- The database name used by the project is `petshop_dwh`.
- The source schema is `raw`; the dbt output schema is `analytics`.
- The dbt profile and database credentials are environment-specific and should remain local.
- Airflow metadata, logs, PID files, and generated configuration files are excluded through `.gitignore`.

## Project status

The data generation/loading scripts, six dbt models, and Airflow orchestration DAG are implemented. The Airflow pipeline has been executed successfully with both tasks completing successfully.

---

Created as a Data Engineering coursework project.
