# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](https://airflow.apache.org/tutorial.html)
"""
from datetime import timedelta

import airflow
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'redshift',
    default_args=default_args,
    description='first redshift dag',
    schedule_interval=timedelta(days=1),
)

insert_chunk_count_sql = \
    """
    INSERT INTO airflow_test.count_users ( 
     id,
     chunk_count
    )
    (
        SELECT user_id, COUNT(*)
        FROM chunks
        GROUP BY user_id
    )
    """

print(insert_chunk_count_sql)

insert_chunk_count = PostgresOperator(
    task_id='insert_chunk_count',
    sql=insert_chunk_count_sql,
    postgres_conn_id='redshift_master',
    dag=dag
)