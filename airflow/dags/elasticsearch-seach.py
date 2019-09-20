from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from elastic_hook import ElasticHook

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

dag = DAG('elastic_search', default_args=default_args, schedule_interval="@daily")

def dump_index(**kwargs):
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


t1 = PythonOperator(
    task_id='elastic_search',
    python_callable=dump_index,
    provide_context=True,
    dag=dag)