from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from common import youtube #common lib defined locally in airflow/common

def fetch_and_insert_videos(execution_date):
    # Connect to the Postgres database
    postgres_hook = PostgresHook(postgres_conn_id='postgres_default')

    # Define the query to select records from the "videos" table created within the past hour
    query = f"""
        INSERT INTO videos_1d
        SELECT * FROM videos
        WHERE created_at >= '{execution_date - timedelta(hours=1)}';
    """

    # Execute the query
    postgres_hook.run(query)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('fetch_videos_hourly', default_args=default_args, schedule_interval='@hourly', catchup=True) as dag:
    create_videos_1d_table = PostgresOperator(
        task_id='create_videos_1d_table',
        postgres_conn_id='postgres_default',
        sql="""
        CREATE TABLE IF NOT EXISTS videos_1d (
            id SERIAL PRIMARY KEY,
            -- Add your columns here
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    fetch_and_insert_videos_task = PythonOperator(
        task_id='fetch_and_insert_videos',
        python_callable=fetch_and_insert_videos,
        provide_context=True,
    )

    create_videos_1d_table >> fetch_and_insert_videos_task
