import streamlit as st
import pandas as pd
import plotly.express as px

st.markdown("""
<style>

/* KPI Cards */
div[data-testid="metric-container"]{
    background:#ffffff;
    border:1px solid #E5E7EB;
    border-radius:16px;
    padding:22px;
    box-shadow:0 4px 12px rgba(0,0,0,.08);
    transition:all .3s ease;
}

div[data-testid="metric-container"]:hover{
    transform:translateY(-4px);
    box-shadow:0 10px 24px rgba(0,0,0,.15);
}

div[data-testid="metric-container"] label{
    font-size:16px;
    font-weight:600;
}

div[data-testid="metric-container"] div[data-testid="stMetricValue"]{
    font-size:36px;
    font-weight:700;
}
/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"]{
    background:#F8FAFC;
    border-right:1px solid #E5E7EB;
}

section[data-testid="stSidebar"] h1{
    color:#1E293B;
    font-weight:700;
}

section[data-testid="stSidebar"] h2{
    color:#334155;
    font-weight:700;
}

section[data-testid="stSidebar"] label{
    font-size:15px;
    font-weight:600;
}

section[data-testid="stSidebar"] .stMultiSelect{
    margin-bottom:18px;
}

</style>
""", unsafe_allow_html=True)
# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Nassau Candy Dashboard",
    page_icon="📊",
    layout="wide"
)

# ===============================
# LOAD DATA
# ===============================
@st.cache_data
def load_data():
    return pd.read_excel(
        "data.xlsx",
        sheet_name="Nassau Candy Distributor-RData"
    )

df = load_data()

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Year"] = df["Order Date"].dt.year


# ===============================
# HEADER
# ===============================
st.title("📊 Profitability Analysis of Nassau Candy Distributor")
st.markdown("### Business Analyst Interactive Dashboard")

# ===============================
# SIDEBAR
# ===============================
st.sidebar.title("Navigation")

st.sidebar.success("Data Loaded Successfully")

# ===============================
# KPI CALCULATIONS
# ===============================

total_sales = df["Sales"].sum()
total_cost = df["Cost"].sum()
gross_profit = df["Gross Profit"].sum()
total_units = df["Units"].sum()

gross_margin = (gross_profit / total_sales) * 100
profit_cost_ratio = gross_profit / total_cost

st.subheader("📈 Key Performance Indicators")
st.caption("High-level business performance summary based on the selected filters.")

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
     st.metric(
         "💰 Total Sales",
        f"${total_sales:,.2f}"
     )

with kpi2:
     st.metric(
         "💵 Total Cost",
         f"${total_cost:,.2f}"
     )

with kpi3:
     st.metric(
         "📈 Gross Profit",
         f"${gross_profit:,.2f}"
     )

kpi4, kpi5, kpi6 = st.columns(3)

with kpi4:
     st.metric(
         "📊 Gross Margin",
        f"{gross_margin:.2f}%"
     )

with kpi5:
     st.metric(
         "📦 Units Sold",
         f"{int(total_units):,}"
     )

with kpi6:
     st.metric(
         "💹 Profit / Cost Ratio",
         f"{profit_cost_ratio:.2f}"
     )
st.markdown("---")
st.sidebar.header("🔎 Filters")

year = st.sidebar.multiselect(
    "Select Year",
    options=sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)


division = st.sidebar.multiselect(
    "Select Division",
    options=df["Division"].unique(),
    default=df["Division"].unique()
)

region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

ship_mode = st.sidebar.multiselect(
    "Select Ship Mode",
    options=df["Ship Mode"].unique(),
    default=df["Ship Mode"].unique()
)

filtered_df = df[
    (df["Year"].isin(year)) &
    (df["Division"].isin(division)) &
    (df["Region"].isin(region)) &
    (df["Ship Mode"].isin(ship_mode))
]

st.markdown("---")
st.subheader("📊 Sales by Division")

division_sales = (
    filtered_df.groupby("Division")["Sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    division_sales,
    x="Division",
    y="Sales",
    color="Division",
    text_auto=".2s",
    title="Sales by Division"
)

fig.update_layout(
    height=500,
    xaxis_title="Division",
    yaxis_title="Sales ($)"
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.subheader("🌍 Sales by Region")

region_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()

fig = px.pie(
    region_sales,
    names="Region",
    values="Sales",
    hole=0.4,
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")
st.subheader("📈 Monthly Sales Trend")

filtered_df["Order Date"] = pd.to_datetime(filtered_df["Order Date"])

monthly_sales = (
    filtered_df
    .groupby(filtered_df["Order Date"].dt.month_name())["Sales"]
    .sum()
    .reindex([
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ])
    .reset_index()
)

fig = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales ($)",
    height=500
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")
st.subheader("🏆 Top 10 Products by Gross Profit")

top_products = (
    filtered_df.groupby("Product Name")["Gross Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_products,
    x="Gross Profit",
    y="Product Name",
    orientation="h",
    color="Gross Profit",
    color_continuous_scale="Blues",
    text_auto=".2s"
)

fig.update_layout(
    height=600,
    xaxis_title="Gross Profit ($)",
    yaxis_title="Product",
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")
st.subheader("💰 Gross Profit by Region")

region_profit = (
    filtered_df.groupby("Region")["Gross Profit"]
    .sum()
    .sort_values(ascending=True)
    .reset_index()
)

fig = px.bar(
    region_profit,
    x="Gross Profit",
    y="Region",
    orientation="h",
    color="Gross Profit",
    color_continuous_scale="Greens",
    text_auto=".2s"
)

fig.update_layout(
    height=500,
    xaxis_title="Gross Profit ($)",
    yaxis_title="Region"
)

st.plotly_chart(fig, use_container_width=True)
st.markdown("---")
st.subheader("📋 Top 10 Products Summary")

top10 = (
    filtered_df.groupby("Product Name")
    .agg({
        "Sales":"sum",
        "Gross Profit":"sum",
        "Units":"sum"
    })
    .sort_values("Gross Profit", ascending=False)
    .head(10)
)

st.dataframe(
    top10.style.format({
        "Sales":"${:,.2f}",
        "Gross Profit":"${:,.2f}",
        "Units":"{:,.0f}"
    }),
    use_container_width=True
)
st.markdown("---")
st.subheader("📌 Business Insights")

st.success("""
✔ Chocolate Division generates the highest sales.

✔ Pacific Region contributes the largest revenue.

✔ Gross Margin remains above 65%, indicating strong profitability.

✔ Sugar Division contributes the lowest sales.

✔ Profit to Cost Ratio = 1.93, reflecting healthy financial performance.

✔ Total Units Sold = 38,654.
""")
st.markdown("---")
st.subheader("🎯 Strategic Recommendations")

st.info("""
• Improve Sugar Division performance.

• Reduce production cost of high-cost products.

• Review pricing strategy for low-margin products.

• Increase focus on Pacific Region.

• Expand Chocolate product portfolio.

• Monitor KPIs using this dashboard.
""")
st.markdown("---")

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.subheader("📋 Dataset Information")

col1, col2 = st.columns(2)

with col1:
    st.metric("Rows", f"{filtered_df.shape[0]:,}")

with col2:
    st.metric("Columns", filtered_df.shape[1])

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="Filtered_Nassau_Candy_Data.csv",
    mime="text/csv"
)
st.markdown("---")

st.markdown(
"""
<center>

### 📊 Nassau Candy Distributor Dashboard

Business Analyst Portfolio Project

Developed using Python • Streamlit • Pandas • Plotly

© 2026 Abinash Manna

</center>
""",
unsafe_allow_html=True
)