import streamlit as st
import pandas as pd
import plotly.express as px

# Set Zillow-style color theme
ZILLOW_BLUE = "#0074E4"
BG_COLOR = "#f7f7f7"

# Load data
df = pd.read_csv("nike_business_performance_dataset.csv")

# Convert Month to datetime
df['Month'] = pd.to_datetime(df['Month'])

# Sidebar Filters
st.sidebar.title("🔎 Filter Options")
regions = st.sidebar.multiselect("Select Region(s):", options=df["Region"].unique(), default=df["Region"].unique())
categories = st.sidebar.multiselect("Select Product Category:", options=df["Product_Category"].unique(), default=df["Product_Category"].unique())
date_range = st.sidebar.date_input("Select Date Range:", [df["Month"].min(), df["Month"].max()])

# Filter dataset
filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Product_Category"].isin(categories)) &
    (df["Month"] >= pd.to_datetime(date_range[0])) &
    (df["Month"] <= pd.to_datetime(date_range[1]))
]

# Zillow-style Dashboard Title
st.markdown(f"<h1 style='color:{ZILLOW_BLUE};'>Nike Business Scorecard (Zillow Style)</h1>", unsafe_allow_html=True)
st.markdown("This dashboard mimics a Zillow-like housing overview, but for Nike's business performance.")

# Metrics Section
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📈 Avg Revenue", f"${filtered_df['Revenue'].mean():,.0f}")
with col2:
    st.metric("👟 Avg Units Sold", f"{filtered_df['Units_Sold'].mean():,.0f}")
with col3:
    st.metric("⏱️ Avg Inventory Turnover", f"{filtered_df['Inventory_Turnover'].mean():.2f}")

# Charts Section
st.subheader("📊 Revenue by Region")
rev_region = filtered_df.groupby("Region")["Revenue"].sum().reset_index()
fig1 = px.bar(rev_region, x="Region", y="Revenue", color="Region", color_discrete_sequence=px.colors.qualitative.Bold)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🛍️ Product Category Revenue Breakdown")
rev_cat = filtered_df.groupby("Product_Category")["Revenue"].sum().reset_index()
fig2 = px.pie(rev_cat, names="Product_Category", values="Revenue", hole=0.4, color_discrete_sequence=px.colors.qualitative.Bold)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("📅 Revenue Trend Over Time")
fig3 = px.line(filtered_df.groupby("Month")["Revenue"].sum().reset_index(), x="Month", y="Revenue", markers=True)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.caption("🔹 Dashboard styled with Zillow inspiration — Powered by Streamlit + Plotly")
