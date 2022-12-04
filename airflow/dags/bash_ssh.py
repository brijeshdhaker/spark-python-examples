from airflow import DAG
import pendulum
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.providers.ssh.hooks.ssh import SSHHook
from datetime import datetime, timedelta

#
#
#
local_ist = pendulum.timezone("Asia/Kolkata")

sshHook = SSHHook(ssh_conn_id='server_ssh')

default_args = {
    'owner': 'brijeshdhaker',
    'schedule_interval': '@once',
    'depends_on_past': False,
    'start_date': datetime(2022, 12, 15, tzinfo=local_ist),
    'email': ['brijeshdhaker@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(dag_id='bash_ssh', default_args=default_args, tags=["ssh"])

current_datetime = datetime.now()
event_datetime = int(current_datetime.timestamp())
str_cmd = f'echo hello >> /tmp/hello-{event_datetime}.txt'
t1 = SSHOperator(
    task_id="task1",
    command=str_cmd,
    ssh_hook=sshHook,
    dag=dag)
