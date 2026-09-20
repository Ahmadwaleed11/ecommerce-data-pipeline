from airflow.decorators import dag, task
from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd

FOLDER = '/usr/local/airflow/include/data'  # adjust to match your Docker volume path

TABLES = {
    'customers': 'olist_customers_dataset.csv',
    'sellers': 'olist_sellers_dataset.csv',
    'products': 'olist_products_dataset.csv',
    'orders': 'olist_orders_dataset.csv',
    'order_items': 'olist_order_items_dataset.csv',
}

@dag(
    dag_id='ecommerce_postgres_load',
    schedule=None,          # run manually for now; can set to '@daily' later
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['ecommerce', 'postgres'],
)
def ecommerce_pipeline():

    @task
    def load_table(table_name: str, file_name: str):
        engine = create_engine('postgresql://postgres:8681@host.docker.internal:5432/ecommerce_dw')
        df = pd.read_csv(f'{FOLDER}/{file_name}')
        df.to_sql(table_name, engine, if_exists='append', index=False)
        return f'Loaded {table_name}'

    # Load dimension tables first, fact table last (same order as before)
    customers_task = load_table.override(task_id='load_customers')('customers', TABLES['customers'])
    sellers_task = load_table.override(task_id='load_sellers')('sellers', TABLES['sellers'])
    products_task = load_table.override(task_id='load_products')('products', TABLES['products'])
    orders_task = load_table.override(task_id='load_orders')('orders', TABLES['orders'])
    order_items_task = load_table.override(task_id='load_order_items')('order_items', TABLES['order_items'])

    # order dependencies based on foreign key relationships:
    # - orders depends on customers (orders.customer_id -> customers.customer_id)
    # - order_items depends on customers, sellers, products, AND orders
    customers_task >> orders_task
    [customers_task, sellers_task, products_task, orders_task] >> order_items_task

ecommerce_pipeline()