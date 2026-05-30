import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Online Retail Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Online Retail Dashboard")
st.markdown("### Customer Purchasing Behaviour Analysis")

# Load dataset
df = pd.read_excel("Online Retail.xlsx")

# Data cleaning
df = df.dropna(subset=["CustomerID"])
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]

# Create Revenue column
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Convert date
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# KPIs
total_revenue = df["Revenue"].sum()
total_transactions = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()
total_products = df["Description"].nunique()

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue (£)", f"{total_revenue:,.0f}")
col2.metric("Transactions", total_transactions)
col3.metric("Customers", total_customers)
col4.metric("Products", total_products)

st.markdown("---")

# Top Products
st.subheader("Top 10 Best Selling Products")

top_products = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig1 = px.bar(
    x=top_products.values,
    y=top_products.index,
    orientation="h",
    labels={"x": "Quantity Sold", "y": "Product"}
)

st.plotly_chart(fig1, use_container_width=True)

# Revenue by Country
st.subheader("Revenue by Country")

country_sales = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig2 = px.bar(
    x=country_sales.index,
    y=country_sales.values,
    labels={"x": "Country", "y": "Revenue (£)"}
)

st.plotly_chart(fig2, use_container_width=True)

# Monthly Sales Trend
st.subheader("Monthly Sales Trend")

monthly_sales = (
    df.set_index("InvoiceDate")
    .resample("ME")["Revenue"]
    .sum()
    .reset_index()
)

fig3 = px.line(
    monthly_sales,
    x="InvoiceDate",
    y="Revenue",
    markers=True
)

st.plotly_chart(fig3, use_container_width=True)

# Top Customers
st.subheader("Top 10 Customers by Revenue")

top_customers = (
    df.groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig4 = px.bar(
    x=top_customers.index.astype(str),
    y=top_customers.values,
    labels={"x": "Customer ID", "y": "Revenue (£)"}
)

st.plotly_chart(fig4, use_container_width=True)

st.success("Dashboard created for easy interpretation of Online Retail data.")