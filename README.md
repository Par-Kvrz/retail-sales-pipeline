# Retail Sales Analytics Pipeline - Snowflake & Streamlit

---

## Project Overview

This project simulates a complete data warehouse and dashboard ETL pipeline for Retail Sales Analytics.  
It includes raw data ingestion (using s3, storage integration, pipes), cleaning, feature engineering, data modelling (star schema with fact and dim tables), data enrichment using ZIP code dataset, and building an interactive dashboard using Streamlit Native Apps inside Snowflake.

The final output supports sales trends analysis, regional sales exploration, product and customer segment performance tracking, and repeat customer behaviour evaluation.

---

## Architecture Overview

- **Data Storage and Processing**: Snowflake
- **Staging Layer**: Raw sales data loaded from CSV files
- **Core Layer**: Dimensional Star Schema (Fact and Dimension tables)
- **Feature Engineering**:
  - Repeat Customer Flag
  - Month-Year formatted dates
- **External Enrichment**:
  - SafeGraph US ZIP Code Dataset for Latitude/Longitude enrichment
- **Dashboard**: Built with Streamlit Native App inside Snowflake
- **Visualization Types**: Line charts, bar charts, tables, maps

---

## Data Sources

- **Superstore Sales Data** from [https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting/data]
- **Deep Sync US ZIP Code Metadata** from [Snowflake Marketplace](https://app.snowflake.com/marketplace)

---

## Tools Used

- Snowflake SQL
- Python
- Streamlit Native Apps (inside Snowflake)
- Altair package for charting
- AWS S3 (for staging ingestion)
- dbdiagram.io for schema diagram

---

## Project Structure

```plaintext
retail-sales-pipeline/
├── README.md
├── sql/
│   ├── Initial set Up.sql
│   ├── Raw Data DQ.sql
│   ├── Core Schema Set-up.sql
├── streamlit_app/
│   └── streamlit_app.py
├── data/
│   ├── dim_customer.csv
│   ├── dim_product.csv
│   ├── dim_location.csv
│   ├── dim_date.csv
│   ├── fact_sales.csv
├── documentation/
│   ├── dq_findings_maxLength.csv
│   ├── schema_diagram.png
│   ├── database_structure_snowflake.png
│   ├── zip_code_overview.png
│   ├── zip_code_dictionary.png
├── images/
│   ├── dashboard_sales_trends.png
│   ├── dashboard_regional_no_filter.png
│   ├── dashboard_regional_filtered.png
│   ├── dashboard_regional_bottom_graph.png
│   ├── dashboard_product_segment_no_filter.png
│   ├── dashboard_product_segment_filtered.png
│   ├── dashboard_repeat_customers.png



