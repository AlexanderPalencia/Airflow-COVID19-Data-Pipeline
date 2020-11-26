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
    "confirmed": "Cases",
    "diff": "Increment"
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
    dag_id = 'covid_confimed',
    default_args = default_args,
    description = 'Confirmed COVID data',
    schedule_interval=None,
)

def etl_process(**kwargs):
    logger.info(kwargs["execution_date"])
    file_path = FSHook(FILE_CONNECTION_NAME).get_path()
    filename = 'time_series_covid19_confirmed_global.csv'
    mysql_connection = MySqlHook(mysql_conn_id=CONNECTION_DB_NAME).get_sqlalchemy_engine()
    full_path = f'{file_path}/{filename}'
    confirmed = pd.read_csv(full_path, encoding = "ISO-8859-1").rename(columns= {'Lat': 'lat', 'Long': 'lon'})
    confirmed['lat'] = confirmed.lat.astype(str)
    confirmed['lon'] = confirmed.lon.astype(str)

    length_colm = len(confirmed.columns)
    for i in range(4, length_colm):
        if i == length_colm-1:
            new_colname = 'diff' + confirmed.columns[i]
            confirmed[new_colname] = 0
        elif i == 4:
            new_colname = 'diff' + confirmed.columns[i]
            confirmed[new_colname] = 0
        else:
                new_colname = ''
                new_colname = 'diff' + confirmed.columns[i]
                confirmed[new_colname] = confirmed[confirmed.columns[i+1]] - confirmed[confirmed.columns[i]]

    first_df = confirmed.iloc[:, 0: length_colm]
    cols = list(range(4,length_colm))
    df = confirmed
    df.drop(df.columns[cols],axis=1,inplace=True)
    second_df = df

    variables = [
        "Province/State",
        "Country/Region",
        "lat",
        "lon"
    ]

    new_confirmed = pd.melt(frame=first_df, id_vars= variables, var_name="fecha",value_name="confirmed")
    new_confirmed["confirmed"] = new_confirmed["confirmed"].astype(int)


    new_diff = pd.melt(frame=df, id_vars= variables, var_name="fecha",value_name="Aumento")
    new_diff["Aumento"] = new_diff["Aumento"].astype(int)

    df_final = new_confirmed
    df_final['diff'] = new_diff['Aumento']

    with mysql_connection.begin() as connection:
        connection.execute("DELETE FROM airflowcovid.confirmed WHERE 1=1")
        df_final.rename(columns=COLUMNS).to_sql('confirmed', con=connection, schema='airflowcovid', if_exists='append', index=False)

    os.remove(full_path)

    logger.info(f"Rows inserted into confirmed table in Mysql")

sensor = FileSensor(
    task_id="covid_sensor_confirmed",
    filepath='time_series_covid19_confirmed_global.csv',
    fs_conn_id=FILE_CONNECTION_NAME,
    poke_interval=10,
    dag=dag,
    )

run_this_task = PythonOperator(
    task_id = 'covid_etl_confirmed',
    python_callable = etl_process,
    provide_context = True,
    dag=dag
)

sensor >> run_this_task
