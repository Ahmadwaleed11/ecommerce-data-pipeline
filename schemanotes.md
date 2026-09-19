# E-Commerce Data Pipeline — Final Schema Documentation
 
## Source Dataset
Olist Brazilian E-Commerce Public Dataset (Kaggle) — 5 core CSVs used.
 
---
 
## Star Schema
 
**FACT TABLE — order_items**
| Column | Type | Notes |
|---|---|---|
| order_id | VARCHAR(50), FK → orders | part of composite key |
| order_item_id | INTEGER | part of composite key |
| product_id | VARCHAR(50), FK → products | |
| seller_id | VARCHAR(50), FK → sellers | |
| price | NUMERIC | measure |
| freight_value | NUMERIC | measure |
| shipping_limit_date | TIMESTAMP | |
 
**DIMENSION — customers**
| Column | Type | Notes |
|---|---|---|
| customer_id | VARCHAR(50), PK | matches orders.customer_id |
| customer_unique_id | VARCHAR(50) | true unique person |
| customer_zip_code_prefix | VARCHAR/INT | |
| customer_city | VARCHAR(100) | |
| customer_state | VARCHAR(10) | |
 
**DIMENSION — orders**
| Column | Type | Notes |
|---|---|---|
| order_id | VARCHAR(50), PK | |
| customer_id | VARCHAR(50), FK → customers | |
| order_status | VARCHAR(30) | delivered, shipped, canceled, etc. |
| order_purchase_timestamp | TIMESTAMP | never null |
| order_approved_at | TIMESTAMP | null if not yet approved/canceled |
| order_delivered_carrier_date | TIMESTAMP | null if not yet shipped |
| order_delivered_customer_date | TIMESTAMP | null if not yet delivered |
| order_estimated_delivery_date | TIMESTAMP | never null |
 
**DIMENSION — products**
| Column | Type | Notes |
|---|---|---|
| product_id | VARCHAR(50), PK | |
| product_category_name | VARCHAR(100) | |
| product_name_lenght | NUMERIC | Olist's own spelling (not "length") |
| product_description_lenght | NUMERIC | |
| product_photos_qty | NUMERIC | |
| product_weight_g | NUMERIC | |
| product_length_cm / height_cm / width_cm | NUMERIC | |
 
**DIMENSION — sellers**
| Column | Type | Notes |
|---|---|---|
| seller_id | VARCHAR(50), PK | |
| seller_zip_code_prefix | VARCHAR(50) | |
| seller_city | VARCHAR(100) | |
| seller_state | VARCHAR(50) | |
 
---
 
## Medallion Architecture Layers
 
### Bronze (Raw)
All 5 tables loaded as-is from CSV, no transformation.
 
### Silver (Cleaned)
Each table passed through a 4-point check:
1. Duplicates removed (`dropDuplicates()`)
2. Primary key nulls checked (none found)
3. Data types verified (`printSchema()`)
4. Text formatting checked (no inconsistent casing/spacing found)
Tables: `silver_customers`, `silver_sellers`, `silver_products`, `silver_orders`, `silver_order_items`
 
**Known nulls in silver_orders (expected, not errors):**
- `order_approved_at`: 160 nulls — orders not yet approved/canceled
- `order_delivered_carrier_date`: 1783 nulls — not yet shipped
- `order_delivered_customer_date`: 2965 nulls — not yet delivered
### Gold (Business-Ready)
- `gold_revenue_by_category` — total revenue per product category (order_items JOIN products, GROUP BY category, SUM price)
- `gold_delivery_time_by_state` — average delivery time (days) per customer state (orders JOIN customers, DATEDIFF, AVG, GROUP BY state)
---
 
## Status: ✅ Pipeline Complete (Bronze → Silver → Gold)
 