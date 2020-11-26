# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.fs_hook import FSHook
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization

FILE_CONNECTION_NAME = 'covid_data_monitor'

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
    dag_id = 'file_sensor_dag',
    default_args = default_args,
    description = 'My first sensor dag',
    schedule_interval=None,
)

def run_this_func(**context):
    print('Hola joven')

# operators that will constitute the tasks

sensor = FileSensor(
    task_id="file_sensor_example",
    dag=dag,
    filepath='test.txt',
    fs_conn_id=FILE_CONNECTION_NAME,
    poke_interval=10
    )


run_this_task = PythonOperator(
    task_id = 'Say_hello',
    python_callable = run_this_func,
    provide_context = True,
    dag=dag
)

sensor >> run_this_task