from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from elastic_hook import ElasticHook
import re
import os
import logging

default_args = {
    'owner': 'airflow',
    'depends_on_past': False, #will depend on the ES index 
    'start_date': datetime(2017, 1, 24),
    'email': ['angel.angelio@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(seconds=10),
}

dag = DAG('elastic_search_logs', default_args=default_args, schedule_interval="@daily")

def dump_index(**kwargs):
    logging.info('------------------------------------------------------------------------------------------------')
    hook = ElasticHook('POST', 'http://elasticsearch:9200')
    #load Directory
    logs = os.listdir("/usr/local/airflow/data/apache_logs/")
    #Define regex by log line
    regex = '^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S+)\s*" (\d{3}) (\S+)'
    #Read file log of directory
    for i in range(len(logs)):
        path_log =  "/usr/local/airflow/data/apache_logs/" + logs[i]
        f = open(path_log, "r")
        logging.info('Abriendo fichero')
        #Read Lines
        index = 1
        for line in f:
            if re.match(regex, line):
                logging.info('parciando linia')
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
                resp = hook.insert_log('logs/'+ str(index), {
                        "log":{
                        "auth":client_identd,
                        "bytes":content_size,
                        "clientip":host, 
                        "httpversion":protocol, 
                        "ident":client_identd,
                        "request":endpoint,
                        "response":response_code,
                        "timestamp":int(datetime.strptime(date_time[1:date_time.find(' ')], '%d/%b/%Y:%H:%M:%S').strftime("%s")) ,
                        "verb":"",
                        "geo": {"lg": 200, "lt":300},
                        "city": "EU"
                        }
                    })
                index = index + 1    
                logging.info('------------------------------------------------------------------------------------------------')
        f.close()

    return resp['hits']['hits']

# insert apachelog
def insert_in_index(**kwargs):
    ds = kwargs['ds']
    hook = ElasticHook('GET', 'elastic_conn_id')
    resp = hook.search('logs/my_type', {
        'size': 10000,
        'sort': [
            {'created_at': 'asc'}
        ],
        'query': {
            'range': {
                'created_at': {
                    'gte': ds + '||-1d/d',
                    'lt': ds + '||/d'
                }
            }
        }
    })

    return resp['hits']['hits']

# insert apachelog
def create_index(**kwargs):
    ds = kwargs['ds']
    hook = ElasticHook('GET', 'elastic_conn_id')
    resp = hook.search('logs/my_type', {
        'size': 10000,
        'sort': [
            {'created_at': 'asc'}
        ],
        'query': {
            'range': {
                'created_at': {
                    'gte': ds + '||-1d/d',
                    'lt': ds + '||/d'
                }
            }
        }
    })

    return resp['hits']['hits']


task = PythonOperator(
    task_id='elastic_search_log',
    python_callable=dump_index,
    op_kwargs={'random_base': float(12) / 10},
    dag=dag,
)
