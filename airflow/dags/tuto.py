"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import re
import os


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2015, 6, 1),
    "email": ["airflow@airflow.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

def write_logs():
    #load Directory
    logs = os.listdir("airflow/data/apache_logs")
    #Define regex by log line
    regex = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S+)\s*" (\d{3}) (\S+)'
    #Read file log of directory
    for i in range(len(logs)):
        path_log =  "airflow/data/apache_logs/" + logs[i]
        f = open(path_log, "r")
        #Read Lines
        for line in f:
            if re.match(regex, line):
                match =  re.search(regex, line).groups()
                host          = match[0]
                client_identd = match[1]
                user_id       = match[2]
                date_time     = match[3]
                method        = match[4]
                endpoint      = match[5]
                protocol      = match[6]
                response_code = int(match[7])
                content_size  = match[8]
        f.close()

dag = DAG("tutorial", default_args=default_args, schedule_interval=timedelta(1))

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)

t2 = BashOperator(task_id="sleep", bash_command="sleep 5", retries=3, dag=dag)

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id="templated",
    bash_command=templated_command,
    params={"my_param": "Parameter I passed in"},
    dag=dag,
)

t4 = PythonOperator(
    task_id='write_elastic_serach',
    provide_context=True,
    python_callable=write_logs,
    dag=dag,

t2.set_upstream(t1)
t3.set_upstream(t1)