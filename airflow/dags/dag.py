import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.postgres_operator import PostgresOperator

import sys
sys.path.append('/usr/local/airflow/scripts')
sys.path.append('/usr/local/airflow/plugins/operators')
from data_quality import PostgresDataQualityOperator
import sql_queries

default_args = {
    'owner' : 'pathairs'
}

dag = DAG(
    'example_dag',
    default_args = default_args,
    description = 'lineman wongnai data engineer test',
    start_date = datetime.datetime(2021, 4, 21, 0, 0, 0)
)

start = DummyOperator(
    task_id = 'load_data_to_postgres',
    dag = dag
)

drop_order_detail = PostgresOperator(
    task_id = 'drop_order_detail_table',
    dag = dag,
    postgres_conn_id = 'postgres_db',
    sql = sql_queries.drop_order_detail_table,
    autocommit = True
)

create_order_detail = PostgresOperator(
    task_id = 'create_order_detail',
    dag = dag,
    postgres_conn_id = 'postgres_db',
    sql = sql_queries.create_order_detail_table,
    autocommit = True
)

copy_order_detail_data = PostgresOperator(
    task_id = 'copy_order_detail_data',
    dag = dag,
    postgres_conn_id = 'postgres_db',
    sql = sql_queries.copy_order_detail_data,
    autocommit = True
)

drop_restaurant_detail = PostgresOperator(
    task_id = 'drop_restaurant_detail_table',
    dag = dag,
    postgres_conn_id = 'postgres_db',
    sql = sql_queries.drop_restaurant_detail_table,
    autocommit = True
)

create_restaurant_detail = PostgresOperator(
    task_id = 'create_restaurant_detail',
    dag = dag,
    postgres_conn_id = 'postgres_db',
    sql = sql_queries.create_restaurant_detail_table,
    autocommit = True
)

copy_restaurant_detail_data = PostgresOperator(
    task_id = 'copy_restaurant_detail_data',
    dag = dag,
    postgres_conn_id = 'postgres_db',
    sql = sql_queries.copy_restaurant_detail_data,
    autocommit = True
)

postgres_data_quality_check = PostgresDataQualityOperator(
    task_id = 'postgreq_data_quality_check',
    dag = dag,
    postgres_conn_id = 'postgres_db',
    data_quality_checks = sql_queries.postgres_data_quality_check
)

start >> drop_order_detail >> create_order_detail >> copy_order_detail_data >> postgres_data_quality_check
start >> drop_restaurant_detail >> create_restaurant_detail >> copy_restaurant_detail_data >> postgres_data_quality_check