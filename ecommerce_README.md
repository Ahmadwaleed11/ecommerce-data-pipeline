# E-Commerce Data Pipeline — Star Schema + Medallion Architecture

An end-to-end data engineering project that models, loads, and transforms real-world e-commerce data using PostgreSQL and Databricks (PySpark), following industry-standard data modeling and pipeline design patterns.

## Dataset

[Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — real, anonymized order data from a Brazilian marketplace, spanning customers, orders, products, sellers, and order items.

## What This Project Does

1. **Data Modeling** — designed a star schema from raw CSVs: one fact table (`order_items`) surrounded by four dimension tables (`customers`, `orders`, `products`, `sellers`)
2. **Load (PostgreSQL)** — created the schema in PostgreSQL and loaded all 5 datasets using Python (pandas + SQLAlchemy)
3. **Transform (Databricks / PySpark)** — rebuilt the pipeline using the **Medallion Architecture**:
   - **Bronze** — raw data loaded as-is from source CSVs, no changes
   - **Silver** — cleaned: deduplicated, null-checked against primary keys, data types corrected, text formatting validated
   - **Gold** — joined and aggregated into business-ready tables answering real questions

## Star Schema

```
                customers
                    |
sellers ---- order_items (FACT) ---- products
                    |
                 orders
```

**Fact table:** `order_items` (price, freight_value, quantity — the measurable data)
**Dimension tables:** `customers`, `sellers`, `products`, `orders` (descriptive context)

## Gold Layer — Business Questions Answered

- **Revenue by product category** — which categories generate the most revenue
- **Average delivery time by state** — which regions experience the longest delivery delays

## Tech Stack

- **PostgreSQL** — relational warehouse, schema design
- **Python** (pandas, SQLAlchemy) — data loading
- **Databricks** — cloud data platform
- **PySpark** — distributed data transformation
- **Delta Lake** — Bronze/Silver/Gold table storage format
- **SQL** — joins, aggregations, analytical queries

## Setup

### 1. PostgreSQL
```bash
# Create the database and run the schema
psql -U postgres -c "CREATE DATABASE ecommerce_dw;"
psql -U postgres -d ecommerce_dw -f create_tables.sql
```

### 2. Load Data into PostgreSQL
```bash
pip install pandas sqlalchemy psycopg2-binary
python load_data.py
```

### 3. Databricks Transformation
- Upload the 5 CSVs to a Databricks Volume
- Run `ecommerce_transformation` notebook — creates Bronze → Silver → Gold tables in order

## What I Learned

Real datasets don't come clean. This project involved debugging actual production-style issues: missing CSV columns not matching the initial schema, inconsistent naming (Olist's own "lenght" typo), column size mismatches (VARCHAR too short for real IDs), and schema evolution conflicts in Delta tables. Solving these was a better lesson in data engineering fundamentals than working with a pre-cleaned dataset would have been.

## Next Steps

- [ ] Orchestrate with Airflow
- [ ] Add pytest / data quality tests
- [ ] CI/CD with GitHub Actions
- [ ] Connect Power BI for visualization
