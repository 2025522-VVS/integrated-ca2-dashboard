import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Online Retail Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
html, body, [class*="css"] {
    font-size: 22px;
}
h1 {
    font-size: 48px !important;
}
h2, h3 {
    font-size: 32px !important;
}
[data-testid="stMetricValue"] {
    font-size: 34px;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Online Retail Dashboard")
st.markdown("## Simple Customer Purchasing Behaviour Analysis")
st.info("This dashboard was designed with large text, simple charts and clear explanations to support users aged 65+.")

df = pd.read_excel("Online Retail.xlsx")

df = df.dropna(subset=["CustomerID"])
df = df[df["Quantity"] > 0]
df = df[df["UnitPrice"] > 0]

df["Revenue"] = df["Quantity"] * df["UnitPrice"]
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

total_revenue = df["Revenue"].sum()
total_transactions = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()
total_products = df["Description"].nunique()

st.header("Key Numbers")
st.write("These cards show the main results of the online retail data.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue (£)", f"{total_revenue:,.0f}")
col2.metric("Transactions", total_transactions)
col3.metric("Customers", total_customers)
col4.metric("Products", total_products)

st.divider()

st.header("Best Selling Products")
st.write("This chart shows the 10 products sold in the highest quantity.")

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
    labels={"x": "Quantity Sold", "y": "Product"},
    text=top_products.values
)
fig1.update_layout(font=dict(size=20), height=650)
fig1.update_traces(textposition="outside")
st.plotly_chart(fig1, use_container_width=True)

st.divider()

st.header("Revenue by Country")
st.write("This chart shows which countries generated the highest revenue.")

country_sales = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig2 = px.bar(
    x=country_sales.index,
    y=country_sales.values,
    labels={"x": "Country", "y": "Revenue (£)"},
    text=country_sales.values.round(0)
)
fig2.update_layout(font=dict(size=20), height=600)
fig2.update_traces(textposition="outside")
st.plotly_chart(fig2, use_container_width=True)

st.divider()

st.header("Monthly Sales Trend")
st.write("This line chart helps users understand how revenue changed over time.")

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
    markers=True,
    labels={"InvoiceDate": "Month", "Revenue": "Revenue (£)"}
)
fig3.update_layout(font=dict(size=20), height=600)
fig3.update_traces(line=dict(width=5), marker=dict(size=12))
st.plotly_chart(fig3, use_container_width=True)

st.divider()

st.header("Top Customers by Revenue")
st.write("This chart shows the customers who generated the highest revenue.")

top_customers = (
    df.groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig4 = px.bar(
    x=top_customers.index.astype(str),
    y=top_customers.values,
    labels={"x": "Customer ID", "y": "Revenue (£)"},
    text=top_customers.values.round(0)
)
fig4.update_layout(font=dict(size=20), height=600)
fig4.update_traces(textposition="outside")
st.plotly_chart(fig4, use_container_width=True)

st.success("This dashboard uses simple language, large text and clear charts to make Online Retail data easier to understand for older users.")a.")
