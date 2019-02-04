# -*- coding: utf-8 -*-

from __future__ import print_function
import airflow
from airflow.operators import PythonOperator
from airflow.models import DAG
from datetime import timedelta
import boto3
import time


def run_athena_query(query, db, s3_output):
    session = boto3.Session(profile_name='labtwin_bi')
    client = session.client('athena', region_name='eu-central-1')
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': db},
        ResultConfiguration={'OutputLocation': s3_output})
    return response

final_query_status = ['SUCCEEDED', 'FAILED', 'CANCELLED']


def check_query_status(**kwargs):
    query_resp = kwargs['ti'].xcom_pull(task_ids='submit_athena_query')
    query_id = query_resp["QueryExecutionId"]
    client = boto3.client('athena')
    result = client.get_query_execution(QueryExecutionId=query_id)
    while (True):
        time.sleep(3)
        if result["QueryExecution"]["Status"]["State"] in final_query_status:
            break
        result = client.get_query_execution(QueryExecutionId=query_id)
    return result


# s3 query output location
s3_output = "s3://labtwin-bi-etl/count_query"
# query to run on aws athena
count_query = "SELECT COUNT(1) FROM cdc_from_production.core_public_chunks"
# aws athena database name
db_name = "cdc_from_production"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG(
    'athena_query_wk',
    default_args=default_args,
    dagrun_timeout=timedelta(hours=2),
    schedule_interval='0 3 * * *'
)

submit_query = PythonOperator(
    task_id='submit_athena_query',
    python_callable=run_athena_query,
    op_kwargs={'query': count_query, 'db': db_name, 's3_output': s3_output},
    dag=dag)

check_query_result = PythonOperator(
    task_id='check_query_result',
    python_callable=check_query_status,
    provide_context=True,
    dag=dag)

submit_query.set_downstream(check_query_result)

