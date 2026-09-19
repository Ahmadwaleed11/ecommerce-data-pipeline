from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

engine=create_engine(os.getenv('Database_url'))

tables={
    'customers':'olist_customers_dataset.csv',
    'sellers':'olist_sellers_dataset.csv',
    'products':'olist_products_dataset.csv',
    'orders':'olist_orders_dataset.csv',
    'order_items':'olist_order_items_dataset.csv',

}
for table_name,file_name in tables.items():
    df=pd.read_csv(fr'C:\Users\pc\Desktop\new\{file_name}')
    df.to_sql(table_name,engine,if_exists='append',index=False)
    print(f'loaded{table_name}')


