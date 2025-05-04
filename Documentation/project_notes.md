# Project Notes - Retail Sales Analytics Pipeline

---

## Key Design Decisions

- Used a lightly normalized Star Schema with Fact and Dimension tables.
- Created a surrogate key for Date (`DATE_ID`) based on YYYYMMDD format for easier joins.
- Added a Repeat Customer Flag to identify loyal customers based on multiple orders.
- Standardized Postal Codes using `LPAD(POSTAL_CODE, 5, '0')` to fix missing leading zeros.
- Enriched location data with Latitude and Longitude from Deep Sync US ZIP Code dataset.

---

## Data Quality Handling

- Null checks for important fields (e.g., `ORDER_ID`, `SALES`, `POSTAL_CODE`).
- Outlier detection: no sales removed after business validation (high sales values considered real).
- Manual fix for Postal Codes missing leading zeros.
- Basic de-duplication checks (e.g., multiple entries for same `ORDER_ID` handled).

---

## Feature Engineering

- Added Month-Year (`MONTH_YEAR`), Month, Year, Day of week, month name and other date fields.
- Built sales trends by Month-Year instead of just Month or Year individually.
- Mapped Customer Segments into broader Customer Types (B2B, B2C).
- Created Repeat vs New Customer Analysis.

---

## Dashboard Enhancements

- Sidebar multi-filters for Year, Product Category, and Customer Type.
- Multiple charts per page: sales trends (filtered and unfiltered), regional sales by top cities and states.
- Colored bar charts for better readability (using Altair).
- Simplified maps to show individual sales transaction density (due to Snowflake Streamlit limitations).

---

## Challenges and Solutions

| Challenge | Solution |
|-----------|----------|
| `st.line_chart()` no custom titles | Switched to Altair charts for flexible labeling |
| No center/zoom control on `st.map()` | Simplified map to show points density |
| Month sorting problem (alphabetical) | Created `MONTH_YEAR` with proper datetime sort order |

---

## Future Enhancements

- Deploy the dashboard publicly using Streamlit Cloud.
- Create automatic Snowpipe ingestion from AWS S3 into Snowflake if future iterations of this data becomes available.
- Add forecasting models for Sales Trends page (e.g., ARIMA, Prophet models).
- Switch mapping to Pydeck or Mapbox when available natively.

---

# Notes

- Streamlit Native App inside Snowflake was used — limited compared to external Streamlit, but good for embedded analytics.
- Snowflake region and S3 bucket matched (`ca-central-1`) to minimize latency and cost.
- All transformations are pushed down to Snowflake SQL instead of being handled in Python (following best practice).

---



