import streamlit as st
import snowflake.snowpark as snowpark
import altair as alt
import pandas as pd

# Start Snowflake session
session = snowpark.Session.builder.getOrCreate()

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Go to", 
    ["📈 Sales Trends", "🌎 Regional Breakdown", "🛍️ Product & Segment Analysis", "🔁 Repeat Customers"]
)

# Query data
df = session.sql("""
    SELECT
        l.CITY,
        l.STATE,
        l.REGION,
        f.ORDER_DATE,
        d.YEAR,
        d.MONTH,
        d.DAY_NAME,
        d.MONTH_NAME,
        f.ORDER_MONTH,
        p.CATEGORY,
        p.SUB_CATEGORY,
        c.SEGMENT,
        c.CUSTOMER_TYPE,
        c.REPEAT_CUSTOMER_FLAG,
        l.LATITUDE,
        l.LONGITUDE,
        f.SALES
    FROM CORE.FACT_SALES f
    JOIN CORE.DIM_LOCATION l ON f.LOCATION_ID = l.LOCATION_ID
    JOIN CORE.DIM_CUSTOMER c ON f.CUSTOMER_ID = c.CUSTOMER_ID
    JOIN CORE.DIM_PRODUCT p ON f.PRODUCT_ID = p.PRODUCT_ID
    JOIN CORE.DIM_DATE d ON TO_NUMBER(TO_CHAR(f.ORDER_DATE, 'YYYYMMDD')) = d.DATE_ID
""").to_pandas()

# Create Month-Year formatted column
df['ORDER_DATE'] = pd.to_datetime(df['ORDER_DATE'])
df['MONTH_YEAR'] = df['ORDER_DATE'].dt.strftime('%b-%Y')


# Main Filters (used across pages)
st.sidebar.header("Filters")
selected_years = st.sidebar.multiselect(
    "Select Years", 
    sorted(df['YEAR'].dropna().unique()), 
    default=sorted(df['YEAR'].dropna().unique())
)
selected_segments = st.sidebar.multiselect(
    "Select Segments", 
    sorted(df['CUSTOMER_TYPE'].dropna().unique()), 
    default=sorted(df['CUSTOMER_TYPE'].dropna().unique())
)
selected_categories = st.sidebar.multiselect(
    "Select Product Categories",
    sorted(df['CATEGORY'].dropna().unique()),
    default=sorted(df['CATEGORY'].dropna().unique())
)

# Filter DataFrame once for all pages
filtered_df = df[
    (df['YEAR'].isin(selected_years)) &
    (df['CUSTOMER_TYPE'].isin(selected_segments)) &
    (df['CATEGORY'].isin(selected_categories))
]

# === PAGE 1: Sales Trends ===
if page == "📈 Sales Trends":
    st.title("📈 Sales Trends Over Time")

    st.write("""
    Analyze how sales evolve over time across different years, products, and customer segments.
    """)

    # Group Sales by Month and Year
    sales_by_month = filtered_df.groupby(['MONTH_NAME', 'YEAR'])['SALES'].sum().reset_index()

    # Pivot for Multi-line Chart
    sales_pivot = sales_by_month.pivot(index='MONTH_NAME', columns='YEAR', values='SALES')

    # Melt sales_pivot for Altair
    sales_melted = sales_pivot.reset_index().melt(id_vars=['MONTH_NAME'], var_name='YEAR', value_name='SALES')

    chart = alt.Chart(sales_melted).mark_line(point=True).encode(
        x=alt.X('MONTH_NAME:N', title='Month'),
        y=alt.Y('SALES:Q', title='Total Sales ($)'),
        color='YEAR:N'
    ).properties(
        title="Monthly Sales Trends",
        width=700,
        height=400
    )

    st.altair_chart(chart, use_container_width=True)

    # Add Independent Sales Trend by Month-Year (Unfiltered)
    st.subheader("📅 Overall Monthly Sales Trends (All Data)")

    sales_trend_full = df.groupby('MONTH_YEAR')['SALES'].sum().reset_index()

    # Add ORDER_DATE to sort correctly
    month_year_date = df.groupby('MONTH_YEAR')['ORDER_DATE'].min().reset_index()
    sales_trend_full = sales_trend_full.merge(month_year_date, on='MONTH_YEAR')
    sales_trend_full = sales_trend_full.sort_values('ORDER_DATE')

    chart_full = alt.Chart(sales_trend_full).mark_line(point=True).encode(
        x=alt.X('MONTH_YEAR:N', title='Month-Year'),
        y=alt.Y('SALES:Q', title='Total Sales ($)')
    ).properties(
        title="Sales Trend Over Time (Unfiltered)",
        width=800,
        height=400
    )

    st.altair_chart(chart_full, use_container_width=True)



# === PAGE 2: Regional Breakdown ===
elif page == "🌎 Regional Breakdown":
    st.title("🌎 Regional Sales Breakdown")

    st.write("""
    Explore sales by state and city with flexible selection and top N filters.
    """)

    selected_states = st.multiselect(
        "Select States to View:",
        options=sorted(df['STATE'].dropna().unique())
    )

    top_n = st.slider("Select Top N Cities by Sales", min_value=1, max_value=10, value=5)

    # Filter by selected states if chosen
    if selected_states:
        regional_filtered = filtered_df[filtered_df['STATE'].isin(selected_states)]
    else:
        regional_filtered = filtered_df

    city_summary = regional_filtered.groupby(['STATE','CITY'])['SALES'].sum().reset_index()
    city_summary = city_summary.sort_values('SALES', ascending=False).head(top_n)

    st.dataframe(city_summary, use_container_width=True)

    st.map(regional_filtered[['LATITUDE', 'LONGITUDE']])
    st.caption("Map shows sales locations. Advanced map styles available in future enhancements.")

    st.subheader("🏙️ Sales by Region and State (All Data)")

    region_state_summary = df.groupby(['REGION', 'STATE'])['SALES'].sum().reset_index()
    
    region_chart = alt.Chart(region_state_summary).mark_bar().encode(
        x=alt.X('STATE:N', title='State'),
        y=alt.Y('SALES:Q', title='Total Sales ($)'),
        color='REGION:N'
    ).properties(
        title="Total Sales by State and Region (Unfiltered)",
        width=700,
        height=400
    )
    
    st.altair_chart(region_chart, use_container_width=True)


# === PAGE 3: Product & Segment Analysis ===
elif page == "🛍️ Product & Segment Analysis":
    st.title("🛍️ Product and Segment Analysis")

    st.write("""
    Dive deep into product and customer segment-based sales analysis across different time periods.
    """)

    selected_months = st.multiselect(
        "Select Months",
        options=sorted(df['MONTH_NAME'].dropna().unique()),
        default=sorted(df['MONTH_NAME'].dropna().unique())
    )

    time_filtered = filtered_df[filtered_df['MONTH_NAME'].isin(selected_months)]

    # --- Product Category Sales ---
    category_sales = time_filtered.groupby('CATEGORY')['SALES'].sum().reset_index()

    st.subheader("🛍️ Sales by Product Category")

    category_chart = alt.Chart(category_sales).mark_bar().encode(
        x=alt.X('CATEGORY:N', title='Product Category'),
        y=alt.Y('SALES:Q', title='Total Sales ($)'),
        color=alt.Color('CATEGORY:N')  # Different color for each category
    ).properties(
        title="Sales by Product Category",
        width=700,
        height=400
    )
    
    st.altair_chart(category_chart, use_container_width=True)


    # --- Customer Segment Sales ---
    segment_sales = time_filtered.groupby('CUSTOMER_TYPE')['SALES'].sum().reset_index()

    st.subheader("Sales by Customer Type")

    seg_chart = alt.Chart(segment_sales).mark_bar().encode(
        x=alt.X('CUSTOMER_TYPE:N', title='Customer Type'),
        y=alt.Y('SALES:Q', title='Total Sales ($)'),
        color=alt.Color('CUSTOMER_TYPE:N')
    ).properties(
        title="Sales by Customer Type",
        width=700,
        height=400
    )

    st.altair_chart(seg_chart, use_container_width=True)


# === PAGE 4: Repeat Customers Analysis ===
elif page == "🔁 Repeat Customers":
    st.title("🔁 New vs Repeat Customer Sales")

    st.write("""
    See how much revenue comes from first-time buyers versus repeat customers.
    """)

    repeat_summary = filtered_df.groupby('REPEAT_CUSTOMER_FLAG')['SALES'].sum().reset_index()
    repeat_summary['Customer_Type'] = repeat_summary['REPEAT_CUSTOMER_FLAG'].replace({
        0: 'New Customer',
        1: 'Repeat Customer'
    })
    
    repeat_chart = alt.Chart(repeat_summary).mark_bar().encode(
        x=alt.X('Customer_Type:N', title='Customer Type'),
        y=alt.Y('SALES:Q', title='Total Sales ($)'),
        color=alt.Color('Customer_Type:N')
    ).properties(
        title="Sales by Customer Type (New vs Repeat)",
        width=700,
        height=400
    )
    
    st.altair_chart(repeat_chart, use_container_width=True)




