"""
Code that goes along with the Airflow tutorial located at:
https://github.com/airbnb/airflow/blob/master/airflow/example_dags/tutorial.py
"""
from airflow import DAG
import pendulum
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

local_ist = pendulum.timezone("Asia/Kolkata")

default_args = {
    'owner': 'brijeshdhaker',
    'depends_on_past': False,
    'start_date': datetime(2020, 10, 10, tzinfo=local_ist),
    'email': ['brijeshdhaker@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    dag_id='airflow_test',
    default_args=default_args,
    catchup=False,
    schedule_interval="0 * * * *",
    tags=["test"])

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

t2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag)

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag)

# t2.set_upstream(t1)
# t3.set_upstream(t1)

t1 >> [t2, t3]
