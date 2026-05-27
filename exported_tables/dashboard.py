import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import os

# Set page config
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Install required packages if not available
try:
    from sklearn.linear_model import LinearRegression
    from sklearn.cluster import KMeans
except ImportError:
    st.error("Please install scikit-learn: pip install scikit-learn")
    st.stop()

# Load data
@st.cache_data
def load_data():
    data_path = "exported_tables"
    if not os.path.exists(data_path):
        data_path = "."
    
    FactSales = pd.read_csv(f"{data_path}/FactSales.csv")
    DimCustomer = pd.read_csv(f"{data_path}/DimCustomer.csv")
    DimModel = pd.read_csv(f"{data_path}/DimModel.csv")
    DimShop = pd.read_csv(f"{data_path}/DimShop.csv")
    DimOffer = pd.read_csv(f"{data_path}/DimOffer.csv")
    DimStock = pd.read_csv(f"{data_path}/DimStock.csv")
    
    FactSales['sale_date'] = pd.to_datetime(FactSales['sale_date'])
    return FactSales, DimCustomer, DimModel, DimShop, DimOffer, DimStock

FactSales, DimCustomer, DimModel, DimShop, DimOffer, DimStock = load_data()

# Title
st.title("Sales KPI Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

min_date = FactSales['sale_date'].min().date()
max_date = FactSales['sale_date'].max().date()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

customers = st.sidebar.multiselect("Customer", FactSales['customer_id'].unique())
brands = st.sidebar.multiselect("Brand", DimModel['brand'].unique())
models = st.sidebar.multiselect("Model", FactSales['model_id'].unique())
shops = st.sidebar.multiselect("Shop", FactSales['shop_id'].unique())

# Apply filters
filtered_data = FactSales.copy()

if len(date_range) == 2:
    filtered_data = filtered_data[(filtered_data['sale_date'].dt.date >= date_range[0]) & 
                                  (filtered_data['sale_date'].dt.date <= date_range[1])]
if customers:
    filtered_data = filtered_data[filtered_data['customer_id'].isin(customers)]
if brands:
    brand_models = DimModel[DimModel['brand'].isin(brands)]['model_id'].tolist()
    filtered_data = filtered_data[filtered_data['model_id'].isin(brand_models)]
if models:
    filtered_data = filtered_data[filtered_data['model_id'].isin(models)]
if shops:
    filtered_data = filtered_data[filtered_data['shop_id'].isin(shops)]

# Top row - KPI cards
col1, col2, col3 = st.columns(3)

total_revenue = filtered_data['final_price'].sum()
total_orders = len(filtered_data)
total_quantity = filtered_data['quantity'].sum()
total_customers = filtered_data['customer_id'].nunique()
total_models = filtered_data['model_id'].nunique()
total_shops = filtered_data['shop_id'].nunique()

with col1:
    st.metric("Total Revenue", f"₹{total_revenue:,.2f}")
    st.metric("Total Orders", f"{total_orders:,}")

with col2:
    st.metric("Total Quantity", f"{total_quantity:,}")
    st.metric("Total Customers", f"{total_customers:,}")

with col3:
    st.metric("Total Models", f"{total_models:,}")
    st.metric("Total Shops", f"{total_shops:,}")

# Show filtered data info and download button
col1, col2 = st.columns([3, 1])
with col1:
    st.write(f"Showing {len(filtered_data):,} records out of {len(FactSales):,} total records")
with col2:
    csv = filtered_data.to_csv(index=False)
    st.download_button("Download CSV", csv, "filtered_sales_data.csv", "text/csv")

# Merge with dimension tables for charts
merged_data = filtered_data.merge(DimModel, on='model_id', how='left') \
                          .merge(DimShop, on='shop_id', how='left')

# Charts
st.header("Analytics")

# Middle row - two charts
col1, col2 = st.columns(2)

with col1:
    # Top 10 models
    top_models = merged_data.groupby('model_id')['final_price'].sum().nlargest(10).reset_index()
    fig1 = px.bar(top_models, x='model_id', y='final_price', title='Top 10 Models by Revenue')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Revenue by shop
    shop_revenue = merged_data.groupby('shop_id')['final_price'].sum().reset_index()
    fig2 = px.bar(shop_revenue, x='shop_id', y='final_price', title='Revenue by Shop')
    st.plotly_chart(fig2, use_container_width=True)

# Bottom row - full-width trend chart
merged_data['month'] = merged_data['sale_date'].dt.to_period('M').astype(str)
monthly_revenue = merged_data.groupby('month')['final_price'].sum().reset_index()
fig3 = px.line(monthly_revenue, x='month', y='final_price', title='Monthly Revenue Trend')
st.plotly_chart(fig3, use_container_width=True)

# Product Performance Analytics
st.header("Product Performance")

model_performance = merged_data.groupby(['model_id', 'brand']).agg({
    'final_price': 'sum',
    'quantity': 'sum'
}).reset_index()
model_performance['revenue_per_unit'] = (model_performance['final_price'] / model_performance['quantity']).round(2)

top_performers = model_performance.nlargest(10, 'final_price')

fig4 = px.bar(top_performers, x='model_id', y='final_price', 
             color='brand', title='Top Revenue Models by Brand')
fig4.update_layout(xaxis_tickangle=45)
st.plotly_chart(fig4, use_container_width=True)

# Performance metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Best Performing Brand", model_performance.groupby('brand')['final_price'].sum().idxmax())
with col2:
    st.metric("Highest Revenue/Unit", f"₹{model_performance['revenue_per_unit'].max():,.2f}")
with col3:
    st.metric("Total Models Sold", len(model_performance))