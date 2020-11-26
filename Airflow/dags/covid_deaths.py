from airflow import DAG
from airflow.contrib.hooks.fs_hook import FSHook
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.hooks.mysql_hook import MySqlHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from structlog import get_logger
import pandas as pd
import os

logger = get_logger()

COLUMNS = {
    "Province/State": "Province",
    "Country/Region": "Country",
    "lat": "Lat",
    "lon": "Lon",
    "fecha": "Date",
    "deaths": "Deaths",
}


FILE_CONNECTION_NAME = 'covid_data_monitor'
CONNECTION_DB_NAME = 'airflow_db'

default_args = {
    'owner': 'Alex',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': '',
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
dag = DAG(
    dag_id = 'covid_deaths',
    default_args = default_args,
    description = 'Deaths COVID data',
    schedule_interval=None,
)

def etl_process(**kwargs):
    logger.info(kwargs["execution_date"])
    file_path = FSHook(FILE_CONNECTION_NAME).get_path()
    filename = 'time_series_covid19_deaths_global.csv'
    mysql_connection = MySqlHook(mysql_conn_id=CONNECTION_DB_NAME).get_sqlalchemy_engine()
    full_path = f'{file_path}/{filename}'
        
    deaths = pd.read_csv(full_path, encoding = "ISO-8859-1").rename(columns= {'Lat': 'lat', 'Long': 'lon'})
    deaths['lat'] = deaths.lat.astype(str)
    deaths['lon'] = deaths.lon.astype(str)

    variables = [
        "Province/State",
        "Country/Region",
        "lat",
        "lon"
    ]

    new_deaths = pd.melt(frame=deaths, id_vars= variables, var_name="fecha",value_name="deaths")
    new_deaths["deaths"] = new_deaths["deaths"].astype(int)



    with mysql_connection.begin() as connection:
        connection.execute("DELETE FROM airflowcovid.death WHERE 1=1")
        new_deaths.rename(columns=COLUMNS).to_sql('death', con=connection, schema='airflowcovid', if_exists='append', index=False)

    os.remove(full_path)

    logger.info(f"Rows inserted into death table in Mysql")

sensor = FileSensor(
    task_id="covid_file_sensor_confirmed",
    dag=dag,
    filepath='time_series_covid19_deaths_global.csv',
    fs_conn_id=FILE_CONNECTION_NAME,
    poke_interval=10
    )

run_this_task = PythonOperator(
    task_id = 'covid_etl_confirmed',
    python_callable = etl_process,
    provide_context = True,
    dag=dag
)

sensor >> run_this_task
