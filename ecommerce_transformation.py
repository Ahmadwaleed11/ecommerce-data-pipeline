# Databricks notebook source
import pandas as pd
from pyspark.sql.functions import col


# COMMAND ----------

silver_products.printSchema()

# COMMAND ----------

silver_order_items.printSchema()

# COMMAND ----------

gold_revenue = spark.sql('''
    select silver_products.product_category_name, 
           SUM(silver_order_items.price) as total_revenue
    from silver_products 
    join silver_order_items 
    on silver_products.product_id = silver_order_items.product_id
    group by silver_products.product_category_name
    order by total_revenue desc
''')

display(gold_revenue)

# COMMAND ----------

Average_del= spark.sql('''
    select silver_customers.customer_state, avg(date_diff(silver_orders.order_delivered_customer_date,silver_orders.order_purchase_timestamp )) as avg_del_days
    from silver_customers join silver_orders on silver_customers.customer_id=silver_orders.customer_id group by customer_state order by avg_del_days desc
                       
                       ''')

display(Average_del)