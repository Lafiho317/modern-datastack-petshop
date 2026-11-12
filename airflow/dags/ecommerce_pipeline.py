from datetime import datetime, timedelta
import os
import subprocess
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator


SCRIPTS_DIR = "/opt/airflow/dags/scripts"
DBT_PROJECT_DIR = "/opt/airflow/ecommerce_dbt"
DBT_EXECUTABLE = "/home/airflow/.local/bin/dbt"


def extract_and_load_data():
    subprocess.run(
        [sys.executable, os.path.join(SCRIPTS_DIR, "data_generator.py")],
        check=True
    )

    subprocess.run(
        [sys.executable, os.path.join(SCRIPTS_DIR, "load_to_dwh.py")],
        check=True
    )


default_args = {
    "owner": "data_engineer",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="ecommerce_elt_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    extract_load_task = PythonOperator(
        task_id="extract_and_load_raw_data",
        python_callable=extract_and_load_data,
    )

    dbt_run_task = BashOperator(
        task_id="dbt_run_transformations",
        bash_command=(
            f"{DBT_EXECUTABLE} run "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROJECT_DIR}"
        ),
    )

    dbt_test_task = BashOperator(
        task_id="dbt_test_task",
        bash_command=(
            f"{DBT_EXECUTABLE} test "
            f"--project-dir {DBT_PROJECT_DIR} "
            f"--profiles-dir {DBT_PROJECT_DIR}"
        ),
    )

    extract_load_task >> dbt_run_task >> dbt_test_task