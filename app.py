# ============================================================
# NASSAU CANDY PRODUCT LINE PROFITABILITY DASHBOARD
# Single-file Streamlit Application
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nassau Candy Profitability Dashboard",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f8f9fa;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.dashboard-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 0.2rem;
}

.dashboard-subtitle {
    color: #6b7280;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}

.section-title {
    font-size: 1.35rem;
    font-weight: 650;
    color: #1f2937;
    margin-top: 1.5rem;
    margin-bottom: 0.7KPI-card {
    background-color: white;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

.kpi-title {
    font-size: 0.85rem;
    color: #6b7280;
    margin-bottom: 5px;
}

.kpi-value {
    font-size: 1.55rem;
    font-weight: 700;
    color: #111827;
}

.kpi-subtitle {
    font-size: 0.75rem;
    color: #6b7280;
    margin-top: 3px;
}

.info-box {
    background-color: #f3f4f6;
    padding: 12px 16px;
    border-radius: 8px;
    border-left: 4px solid #6b7280;
    margin: 10px 0;
}

.success-box {
    background-color: #ecfdf5;
    padding: 12px 16px;
    border-radius: 8px;
    border-left: 4px solid #10b981;
}

.warning-box {
    background-color: #fffbeb;
    padding: 12px 16px;
    border-radius: 8px;
    border-left: 4px solid #f59e0b;
}

.danger-box {
    background-color: #fef2f2;
    padding: 12px 16px;
    border-radius: 8px;
    border-left: 4px solid #ef4444;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# FILE LOADING FUNCTIONS
# ============================================================

@st.cache_data
def find_file(prefix):
    """
    Find a file by its starting name.
    Supports CSV and Excel files.
    Searches project folder and subfolders.
    """

    possible_files = []

    for pattern in [
        f"{prefix}.csv",
        f"{prefix}.xlsx",
        f"{prefix}.xls",
        f"{prefix}(1).csv",
        f"{prefix}(1).xlsx",
        f"{prefix}(1).xls"
    ]:
        possible_files.extend(BASE_DIR.rglob(pattern))

    if possible_files:
        return possible_files[0]

    # More flexible search
    all_files = list(BASE_DIR.rglob("*"))

    for file in all_files:
        if file.is_file():
            name = file.stem.lower()
            if prefix.lower() in name:
                if file.suffix.lower() in [".csv", ".xlsx", ".xls"]:
                    return file

    return None


@st.cache_data
def read_data_file(file_path):
    """
    Read CSV or Excel file.
    """

    if file_path is None:
        return None

    try:
        if file_path.suffix.lower() == ".csv":
            return pd.read_csv(file_path)

        elif file_path.suffix.lower() in [".xlsx", ".xls"]:
            return pd.read_excel(file_path)

    except Exception as e:
        st.error(f"Error reading {file_path.name}: {e}")
        return None

    return None


# ============================================================
# COLUMN HELPER FUNCTIONS
# ============================================================

def find_column(df, possible_names):
    """
    Find a column using case-insensitive matching.
    """

    if df is None:
        return None

    normalized = {
        str(col).strip().lower(): col
        for col in df.columns
    }

    for name in possible_names:
        key = name.strip().lower()

        if key in normalized:
            return normalized[key]

    return None


def rename_standard_columns(df):
    """
    Standardize important columns without changing the original
    dataset unnecessarily.
    """

    df = df.copy()

    mapping = {}

    column_groups = {
        "order_date": [
            "order_date",
            "Order Date",
            "order date"
        ],

        "ship_date": [
            "ship_date",
            "Ship Date",
            "ship date"
        ],

        "sales": [
            "sales",
            "Sales",
            "Total_Sales"
        ],

        "cost": [
            "cost",
            "Cost",
            "Total_Cost"
        ],

        "gross_profit": [
            "gross_profit",
            "Gross Profit",
            "Total_Gross_Profit"
        ],

        "units": [
            "units",
            "Units",
            "Total_Units"
        ],

        "product_name": [
            "product_name",
            "Product Name",
            "product name"
        ],

        "division": [
            "division",
            "Division"
        ],

        "region": [
            "region",
            "Region"
        ],

        "state": [
            "state/province",
            "State/Province",
            "state",
            "State"
        ],

        "customer_id": [
            "customer_id",
            "Customer ID"
        ],

        "order_id": [
            "order_id",
            "Order ID"
        ]
    }

    for standard_name, possible_names in column_groups.items():

        actual_column = find_column(df, possible_names)

        if actual_column is not None:
            mapping[actual_column] = standard_name

    df = df.rename(columns=mapping)

    return df


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_main_dataset():

    file_path = find_file("Nassau_Candy_Cleaned")

    if file_path is None:
        return None, None

    df = read_data_file(file_path)

    if df is None:
        return None, file_path

    df = rename_standard_columns(df)

    # Convert numeric columns
    numeric_columns = [
        "sales",
        "cost",
        "gross_profit",
        "units"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # Convert dates
    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(
            df["order_date"],
            errors="coerce",
            dayfirst=True
        )

    if "ship_date" in df.columns:
        df["ship_date"] = pd.to_datetime(
            df["ship_date"],
            errors="coerce",
            dayfirst=True
        )

    # Calculate gross profit if required
    if "gross_profit" not in df.columns:

        if "sales" in df.columns and "cost" in df.columns:
            df["gross_profit"] = (
                df["sales"] - df["cost"]
            )

    # Calculate gross margin
    if "sales" in df.columns:

        df["gross_margin_%"] = np.where(
            df["sales"] != 0,
            (df["gross_profit"] / df["sales"]) * 100,
            np.nan
        )

    # Calculate profit per unit
    if "units" in df.columns:

        df["profit_per_unit"] = np.where(
            df["units"] != 0,
            df["gross_profit"] / df["units"],
            np.nan
        )

    # Calculate cost to sales ratio
    if "sales" in df.columns:

        df["cost_to_sales_%"] = np.where(
            df["sales"] != 0,
            (df["cost"] / df["sales"]) * 100,
            np.nan
        )

    # Calculate shipment lead time
    if (
        "order_date" in df.columns
        and "ship_date" in df.columns
    ):

        df["shipment_lead_time"] = (
            df["ship_date"] - df["order_date"]
        ).dt.days

    return df, file_path


# ============================================================
# LOAD DATA
# ============================================================

df, main_file = load_main_dataset()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">'
    '🍫 Nassau Candy Product Line Profitability Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Product profitability, division performance, cost efficiency, '
    'pricing diagnostics and profit concentration analysis'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# DATA VALIDATION
# ============================================================

if df is None:

    st.error(
        "Nassau_Candy_Cleaned file could not be found."
    )

    st.info(
        f"Please place Nassau_Candy_Cleaned.csv or "
        f"Nassau_Candy_Cleaned.xlsx in:\n\n{BASE_DIR}"
    )

    st.stop()


required_columns = [
    "sales",
    "cost",
    "gross_profit",
    "units",
    "product_name",
    "division"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:

    st.error(
        f"Required columns are missing: {missing_columns}"
    )

    st.write("Available columns:")
    st.write(list(df.columns))

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("🎛️ Dashboard Filters")

st.sidebar.markdown(
    "Use the filters below to interactively analyze profitability."
)


# -----------------------------
# DATE FILTER
# -----------------------------

if "order_date" in df.columns:

    valid_dates = df["order_date"].dropna()

    if len(valid_dates) > 0:

        min_date = valid_dates.min().date()
        max_date = valid_dates.max().date()

        date_range = st.sidebar.date_input(
            "Order Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        if isinstance(date_range, tuple):

            if len(date_range) == 2:

                start_date = pd.Timestamp(
                    date_range[0]
                )

                end_date = (
                    pd.Timestamp(date_range[1])
                    + pd.Timedelta(days=1)
                )

                filtered_df = df[
                    (df["order_date"] >= start_date)
                    &
                    (df["order_date"] < end_date)
                ].copy()

            else:
                filtered_df = df.copy()

        else:
            filtered_df = df.copy()

    else:
        filtered_df = df.copy()

else:
    filtered_df = df.copy()


# -----------------------------
# DIVISION FILTER
# -----------------------------

divisions = sorted(
    filtered_df["division"]
    .dropna()
    .astype(str)
    .unique()
    .tolist()
)

selected_divisions = st.sidebar.multiselect(
    "Division",
    options=divisions,
    default=divisions
)

if selected_divisions:

    filtered_df = filtered_df[
        filtered_df["division"]
        .astype(str)
        .isin(selected_divisions)
    ]


# -----------------------------
# PRODUCT SEARCH
# -----------------------------

product_search = st.sidebar.text_input(
    "🔎 Product Search",
    placeholder="Enter product name..."
)

if product_search:

    filtered_df = filtered_df[
        filtered_df["product_name"]
        .astype(str)
        .str.contains(
            product_search,
            case=False,
            na=False
        )
    ]


# -----------------------------
# MARGIN THRESHOLD
# -----------------------------

margin_threshold = st.sidebar.slider(
    "Minimum Gross Margin (%)",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
    step=1.0
)

if "gross_margin_%" in filtered_df.columns:

    filtered_df = filtered_df[
        filtered_df["gross_margin_%"]
        >= margin_threshold
    ]


# ============================================================
# SIDEBAR INFORMATION
# ============================================================

st.sidebar.markdown("---")

st.sidebar.metric(
    "Filtered Transactions",
    f"{len(filtered_df):,}"
)

st.sidebar.metric(
    "Products",
    f"{filtered_df['product_name'].nunique():,}"
)

st.sidebar.metric(
    "Divisions",
    f"{filtered_df['division'].nunique():,}"
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = filtered_df["sales"].sum()
total_cost = filtered_df["cost"].sum()
total_profit = filtered_df["gross_profit"].sum()
total_units = filtered_df["units"].sum()

overall_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)

profit_per_unit = (
    total_profit / total_units
    if total_units != 0
    else 0
)


# ============================================================
# KPI DISPLAY
# ============================================================

st.markdown(
    '<div class="section-title">📊 Executive KPIs</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5 = st.columns(5)

with k1:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Sales</div>
            <div class="kpi-value">${total_sales:,.2f}</div>
            <div class="kpi-subtitle">Revenue generated</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Cost</div>
            <div class="kpi-value">${total_cost:,.2f}</div>
            <div class="kpi-subtitle">Total product cost</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Gross Profit</div>
            <div class="kpi-value">${total_profit:,.2f}</div>
            <div class="kpi-subtitle">Profit contribution</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Gross Margin</div>
            <div class="kpi-value">{overall_margin:.2f}%</div>
            <div class="kpi-subtitle">Profitability rate</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k5:

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">Profit / Unit</div>
            <div class="kpi-value">${profit_per_unit:.2f}</div>
            <div class="kpi-subtitle">Average profit per unit</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DATA AVAILABILITY CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "No records match the selected filters. "
        "Please adjust the filters."
    )

    st.stop()


# ============================================================
# PRODUCT-LEVEL ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '1️⃣ Product Profitability Overview'
    '</div>',
    unsafe_allow_html=True
)


product_summary = (
    filtered_df
    .groupby("product_name", as_index=False)
    .agg(
        Total_Sales=("sales", "sum"),
        Total_Cost=("cost", "sum"),
        Total_Gross_Profit=("gross_profit", "sum"),
        Total_Units=("units", "sum")
    )
)

product_summary["Gross_Margin_%"] = np.where(
    product_summary["Total_Sales"] != 0,
    product_summary["Total_Gross_Profit"]
    / product_summary["Total_Sales"] * 100,
    0
)

product_summary["Profit_Per_Unit"] = np.where(
    product_summary["Total_Units"] != 0,
    product_summary["Total_Gross_Profit"]
    / product_summary["Total_Units"],
    0
)

product_summary["Profit_Contribution_%"] = np.where(
    total_profit != 0,
    product_summary["Total_Gross_Profit"]
    / total_profit * 100,
    0
)

product_summary = product_summary.sort_values(
    "Total_Gross_Profit",
    ascending=False
)


# ============================================================
# PRODUCT CHARTS
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.markdown("### Gross Profit by Product")

    fig_profit = px.bar(
        product_summary.sort_values(
            "Total_Gross_Profit",
            ascending=True
        ),
        x="Total_Gross_Profit",
        y="product_name",
        orientation="h",
        labels={
            "Total_Gross_Profit": "Gross Profit ($)",
            "product_name": "Product"
        },
        text="Total_Gross_Profit"
    )

    fig_profit.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside"
    )

    fig_profit.update_layout(
        height=600,
        margin=dict(l=20, r=80, t=30, b=20)
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )


with col2:

    st.markdown("### Gross Margin by Product")

    margin_chart = product_summary.sort_values(
        "Gross_Margin_%",
        ascending=True
    )

    fig_margin = px.bar(
        margin_chart,
        x="Gross_Margin_%",
        y="product_name",
        orientation="h",
        labels={
            "Gross_Margin_%": "Gross Margin (%)",
            "product_name": "Product"
        },
        text="Gross_Margin_%"
    )

    fig_margin.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig_margin.update_layout(
        height=600,
        margin=dict(l=20, r=80, t=30, b=20),
        xaxis=dict(range=[0, 100])
    )

    st.plotly_chart(
        fig_margin,
        use_container_width=True
    )


# ============================================================
# PROFIT CONTRIBUTION
# ============================================================

st.markdown("### Product Profit Contribution")

fig_contribution = px.pie(
    product_summary,
    names="product_name",
    values="Total_Gross_Profit",
    hole=0.45
)

fig_contribution.update_layout(
    height=500
)

st.plotly_chart(
    fig_contribution,
    use_container_width=True
)


# ============================================================
# PRODUCT PROFITABILITY TABLE
# ============================================================

st.markdown("### Product-Level Profitability Leaderboard")

display_product = product_summary.copy()

display_product["Total_Sales"] = display_product[
    "Total_Sales"
].map(lambda x: f"${x:,.2f}")

display_product["Total_Cost"] = display_product[
    "Total_Cost"
].map(lambda x: f"${x:,.2f}")

display_product["Total_Gross_Profit"] = display_product[
    "Total_Gross_Profit"
].map(lambda x: f"${x:,.2f}")

display_product["Gross_Margin_%"] = display_product[
    "Gross_Margin_%"
].map(lambda x: f"{x:.2f}%")

display_product["Profit_Per_Unit"] = display_product[
    "Profit_Per_Unit"
].map(lambda x: f"${x:.2f}")

display_product["Profit_Contribution_%"] = display_product[
    "Profit_Contribution_%"
].map(lambda x: f"{x:.2f}%")

display_product.columns = [
    "Product",
    "Sales",
    "Cost",
    "Gross Profit",
    "Units",
    "Gross Margin",
    "Profit / Unit",
    "Profit Contribution"
]

st.dataframe(
    display_product,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# MARGIN VS PROFIT SCATTER
# ============================================================

st.markdown("### Margin vs Gross Profit")

fig_scatter = px.scatter(
    product_summary,
    x="Gross_Margin_%",
    y="Total_Gross_Profit",
    size="Total_Units",
    hover_name="product_name",
    labels={
        "Gross_Margin_%": "Gross Margin (%)",
        "Total_Gross_Profit": "Gross Profit ($)"
    }
)

fig_scatter.update_layout(
    height=500
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)


# ============================================================
# DIVISION PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">'
    '2️⃣ Division Performance Dashboard'
    '</div>',
    unsafe_allow_html=True
)


division_summary = (
    filtered_df
    .groupby("division", as_index=False)
    .agg(
        Total_Sales=("sales", "sum"),
        Total_Cost=("cost", "sum"),
        Total_Gross_Profit=("gross_profit", "sum"),
        Total_Units=("units", "sum")
    )
)

division_summary["Gross_Margin_%"] = np.where(
    division_summary["Total_Sales"] != 0,
    division_summary["Total_Gross_Profit"]
    / division_summary["Total_Sales"] * 100,
    0
)

division_summary["Profit_Per_Unit"] = np.where(
    division_summary["Total_Units"] != 0,
    division_summary["Total_Gross_Profit"]
    / division_summary["Total_Units"],
    0
)

division_summary["Profit_Contribution_%"] = np.where(
    total_profit != 0,
    division_summary["Total_Gross_Profit"]
    / total_profit * 100,
    0
)


col1, col2 = st.columns(2)


with col1:

    st.markdown("### Revenue vs Gross Profit")

    division_long = division_summary.melt(
        id_vars="division",
        value_vars=[
            "Total_Sales",
            "Total_Gross_Profit"
        ],
        var_name="Metric",
        value_name="Amount"
    )

    division_long["Metric"] = division_long[
        "Metric"
    ].replace({
        "Total_Sales": "Sales",
        "Total_Gross_Profit": "Gross Profit"
    })

    fig_division = px.bar(
        division_long,
        x="division",
        y="Amount",
        color="Metric",
        barmode="group",
        labels={
            "Amount": "Amount ($)",
            "division": "Division"
        }
    )

    fig_division.update_layout(
        height=450
    )

    st.plotly_chart(
        fig_division,
        use_container_width=True
    )


with col2:

    st.markdown("### Division Gross Margin")

    fig_div_margin = px.bar(
        division_summary,
        x="division",
        y="Gross_Margin_%",
        text="Gross_Margin_%",
        labels={
            "Gross_Margin_%": "Gross Margin (%)",
            "division": "Division"
        }
    )

    fig_div_margin.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig_div_margin.update_layout(
        height=450,
        yaxis=dict(range=[0, 100])
    )

    st.plotly_chart(
        fig_div_margin,
        use_container_width=True
    )


# ============================================================
# DIVISION TABLE
# ============================================================

st.markdown("### Division Performance Summary")

division_display = division_summary.copy()

division_display["Total_Sales"] = division_display[
    "Total_Sales"
].map(lambda x: f"${x:,.2f}")

division_display["Total_Cost"] = division_display[
    "Total_Cost"
].map(lambda x: f"${x:,.2f}")

division_display["Total_Gross_Profit"] = division_display[
    "Total_Gross_Profit"
].map(lambda x: f"${x:,.2f}")

division_display["Gross_Margin_%"] = division_display[
    "Gross_Margin_%"
].map(lambda x: f"{x:.2f}%")

division_display["Profit_Per_Unit"] = division_display[
    "Profit_Per_Unit"
].map(lambda x: f"${x:.2f}")

division_display["Profit_Contribution_%"] = division_display[
    "Profit_Contribution_%"
].map(lambda x: f"{x:.2f}%")

division_display.columns = [
    "Division",
    "Sales",
    "Cost",
    "Gross Profit",
    "Units",
    "Gross Margin",
    "Profit / Unit",
    "Profit Contribution"
]

st.dataframe(
    division_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# COST VS MARGIN DIAGNOSTICS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '3️⃣ Cost vs Margin Diagnostics'
    '</div>',
    unsafe_allow_html=True
)


cost_summary = product_summary.copy()

cost_summary["Cost_to_Sales_%"] = np.where(
    cost_summary["Total_Sales"] != 0,
    cost_summary["Total_Cost"]
    / cost_summary["Total_Sales"] * 100,
    0
)


col1, col2 = st.columns(2)


with col1:

    st.markdown("### Cost vs Sales")

    fig_cost_sales = px.scatter(
        cost_summary,
        x="Total_Sales",
        y="Total_Cost",
        size="Total_Gross_Profit",
        hover_name="product_name",
        labels={
            "Total_Sales": "Sales ($)",
            "Total_Cost": "Cost ($)"
        }
    )

    fig_cost_sales.update_layout(
        height=500
    )

    st.plotly_chart(
        fig_cost_sales,
        use_container_width=True
    )


with col2:

    st.markdown("### Cost-to-Sales Ratio")

    cost_chart = cost_summary.sort_values(
        "Cost_to_Sales_%",
        ascending=True
    )

    fig_cost_ratio = px.bar(
        cost_chart,
        x="Cost_to_Sales_%",
        y="product_name",
        orientation="h",
        text="Cost_to_Sales_%",
        labels={
            "Cost_to_Sales_%": "Cost / Sales (%)",
            "product_name": "Product"
        }
    )

    fig_cost_ratio.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig_cost_ratio.update_layout(
        height=500
    )

    st.plotly_chart(
        fig_cost_ratio,
        use_container_width=True
    )


# ============================================================
# MARGIN RISK FLAGS
# ============================================================

st.markdown("### Margin Risk Assessment")


def assign_risk(margin):

    if margin < 20:
        return "🔴 Critical"

    elif margin < 40:
        return "🟠 High Risk"

    elif margin < 60:
        return "🟡 Moderate"

    else:
        return "🟢 Healthy"


risk_df = cost_summary.copy()

risk_df["Risk_Flag"] = (
    risk_df["Gross_Margin_%"]
    .apply(assign_risk)
)

risk_df = risk_df.sort_values(
    "Gross_Margin_%",
    ascending=True
)


risk_display = risk_df[
    [
        "product_name",
        "Total_Sales",
        "Total_Cost",
        "Total_Gross_Profit",
        "Gross_Margin_%",
        "Cost_to_Sales_%",
        "Profit_Per_Unit",
        "Risk_Flag"
    ]
].copy()


risk_display.columns = [
    "Product",
    "Sales",
    "Cost",
    "Gross Profit",
    "Gross Margin %",
    "Cost / Sales %",
    "Profit / Unit",
    "Risk"
]


st.dataframe(
    risk_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# LOWEST MARGIN PRODUCTS
# ============================================================

lowest_margin = cost_summary.sort_values(
    "Gross_Margin_%"
).head(5)


if len(lowest_margin) > 0:

    st.markdown("### ⚠️ Lowest-Margin Products")

    for _, row in lowest_margin.iterrows():

        margin = row["Gross_Margin_%"]

        if margin < 20:

            st.markdown(
                f"""
                <div class="danger-box">
                <b>{row['product_name']}</b> —
                Gross Margin: {margin:.2f}% |
                Gross Profit: ${row['Total_Gross_Profit']:,.2f}
                </div>
                """,
                unsafe_allow_html=True
            )

        elif margin < 40:

            st.markdown(
                f"""
                <div class="warning-box">
                <b>{row['product_name']}</b> —
                Gross Margin: {margin:.2f}% |
                Gross Profit: ${row['Total_Gross_Profit']:,.2f}
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# PRICING ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '4️⃣ Pricing & Unit Economics'
    '</div>',
    unsafe_allow_html=True
)


pricing = product_summary.copy()

pricing["Selling_Price_Per_Unit"] = np.where(
    pricing["Total_Units"] != 0,
    pricing["Total_Sales"]
    / pricing["Total_Units"],
    0
)

pricing["Cost_Per_Unit"] = np.where(
    pricing["Total_Units"] != 0,
    pricing["Total_Cost"]
    / pricing["Total_Units"],
    0
)

pricing["Profit_Per_Unit"] = np.where(
    pricing["Total_Units"] != 0,
    pricing["Total_Gross_Profit"]
    / pricing["Total_Units"],
    0
)


pricing_chart = pricing.sort_values(
    "Profit_Per_Unit",
    ascending=True
)


fig_price = px.bar(
    pricing_chart,
    x="Profit_Per_Unit",
    y="product_name",
    orientation="h",
    text="Profit_Per_Unit",
    labels={
        "Profit_Per_Unit": "Profit per Unit ($)",
        "product_name": "Product"
    }
)

fig_price.update_traces(
    texttemplate="$%{text:.2f}",
    textposition="outside"
)

fig_price.update_layout(
    height=550
)

st.plotly_chart(
    fig_price,
    use_container_width=True
)


pricing_display = pricing[
    [
        "product_name",
        "Total_Units",
        "Selling_Price_Per_Unit",
        "Cost_Per_Unit",
        "Profit_Per_Unit",
        "Gross_Margin_%"
    ]
].copy()

pricing_display.columns = [
    "Product",
    "Units",
    "Selling Price / Unit",
    "Cost / Unit",
    "Profit / Unit",
    "Gross Margin %"
]

pricing_display["Selling Price / Unit"] = (
    pricing_display["Selling Price / Unit"]
    .map(lambda x: f"${x:.2f}")
)

pricing_display["Cost / Unit"] = (
    pricing_display["Cost / Unit"]
    .map(lambda x: f"${x:.2f}")
)

pricing_display["Profit / Unit"] = (
    pricing_display["Profit / Unit"]
    .map(lambda x: f"${x:.2f}")
)

pricing_display["Gross Margin %"] = (
    pricing_display["Gross Margin %"]
    .map(lambda x: f"{x:.2f}%")
)

st.dataframe(
    pricing_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# PROFIT CONCENTRATION / PARETO ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '5️⃣ Profit Concentration Analysis'
    '</div>',
    unsafe_allow_html=True
)


pareto = product_summary[
    [
        "product_name",
        "Total_Gross_Profit"
    ]
].copy()

pareto = pareto.sort_values(
    "Total_Gross_Profit",
    ascending=False
).reset_index(drop=True)

pareto["Profit_Contribution_%"] = np.where(
    total_profit != 0,
    pareto["Total_Gross_Profit"]
    / total_profit * 100,
    0
)

pareto["Cumulative_Profit_%"] = (
    pareto["Profit_Contribution_%"]
    .cumsum()
)


fig_pareto = go.Figure()

fig_pareto.add_trace(
    go.Bar(
        x=pareto["product_name"],
        y=pareto["Total_Gross_Profit"],
        name="Gross Profit"
    )
)

fig_pareto.add_trace(
    go.Scatter(
        x=pareto["product_name"],
        y=pareto["Cumulative_Profit_%"],
        name="Cumulative Profit %",
        yaxis="y2",
        mode="lines+markers"
    )
)

fig_pareto.add_hline(
    y=80,
    line_dash="dash",
    annotation_text="80% Profit Level",
    yref="y2"
)

fig_pareto.update_layout(
    height=600,
    xaxis=dict(
        title="Product",
        tickangle=-45
    ),
    yaxis=dict(
        title="Gross Profit ($)"
    ),
    yaxis2=dict(
        title="Cumulative Profit (%)",
        overlaying="y",
        side="right",
        range=[0, 105]
    ),
    legend=dict(
        orientation="h"
    )
)

st.plotly_chart(
    fig_pareto,
    use_container_width=True
)


# ============================================================
# DEPENDENCY INDICATORS
# ============================================================

top_product_share = (
    pareto.iloc[0]["Total_Gross_Profit"]
    / total_profit * 100
    if total_profit != 0
    else 0
)

top_3_share = (
    pareto.head(3)["Total_Gross_Profit"].sum()
    / total_profit * 100
    if total_profit != 0
    else 0
)

products_to_80 = (
    (pareto["Cumulative_Profit_%"] < 80).sum() + 1
    if len(pareto) > 0
    else 0
)

total_products = len(pareto)

dependency_level = (
    "High"
    if top_3_share >= 70
    else "Moderate"
    if top_3_share >= 50
    else "Low"
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "Top Product Profit Share",
        f"{top_product_share:.2f}%"
    )


with c2:

    st.metric(
        "Top 3 Profit Share",
        f"{top_3_share:.2f}%"
    )


with c3:

    st.metric(
        "Products to Reach 80%",
        f"{products_to_80} / {total_products}"
    )


with c4:

    st.metric(
        "Dependency Level",
        dependency_level
    )


# ============================================================
# PARETO TABLE
# ============================================================

st.markdown("### Profit Concentration Table")

pareto_display = pareto.copy()

pareto_display["Total_Gross_Profit"] = (
    pareto_display["Total_Gross_Profit"]
    .map(lambda x: f"${x:,.2f}")
)

pareto_display["Profit_Contribution_%"] = (
    pareto_display["Profit_Contribution_%"]
    .map(lambda x: f"{x:.2f}%")
)

pareto_display["Cumulative_Profit_%"] = (
    pareto_display["Cumulative_Profit_%"]
    .map(lambda x: f"{x:.2f}%")
)

pareto_display.columns = [
    "Product",
    "Gross Profit",
    "Profit Contribution",
    "Cumulative Profit"
]

st.dataframe(
    pareto_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# STRATEGIC PRODUCT RECOMMENDATIONS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '6️⃣ Strategic Product Recommendations'
    '</div>',
    unsafe_allow_html=True
)


recommendations = product_summary.copy()


def recommendation(row):

    margin = row["Gross_Margin_%"]
    profit = row["Total_Gross_Profit"]
    sales = row["Total_Sales"]
    units = row["Total_Units"]

    # Strong products
    if (
        margin >= 60
        and profit >= product_summary[
            "Total_Gross_Profit"
        ].median()
    ):
        return "🟢 RETAIN / INVEST"

    # Low margin
    elif margin < 30:
        return "🔴 COST / PRICING REVIEW"

    # High margin but low scale
    elif (
        margin >= 60
        and profit < product_summary[
            "Total_Gross_Profit"
        ].median()
    ):
        return "🟡 GROWTH REVIEW"

    # Low volume
    elif units < product_summary["Total_Units"].median():
        return "🟡 VOLUME REVIEW"

    else:
        return "🟡 MONITOR"


recommendations["Recommendation"] = (
    recommendations.apply(
        recommendation,
        axis=1
    )
)


recommendations = recommendations.sort_values(
    "Total_Gross_Profit",
    ascending=False
)


recommendation_display = recommendations[
    [
        "product_name",
        "Total_Sales",
        "Total_Gross_Profit",
        "Total_Units",
        "Gross_Margin_%",
        "Profit_Per_Unit",
        "Recommendation"
    ]
].copy()

recommendation_display.columns = [
    "Product",
    "Sales",
    "Gross Profit",
    "Units",
    "Gross Margin %",
    "Profit / Unit",
    "Recommendation"
]

recommendation_display["Sales"] = (
    recommendation_display["Sales"]
    .map(lambda x: f"${x:,.2f}")
)

recommendation_display["Gross Profit"] = (
    recommendation_display["Gross Profit"]
    .map(lambda x: f"${x:,.2f}")
)

recommendation_display["Gross Margin %"] = (
    recommendation_display["Gross Margin %"]
    .map(lambda x: f"{x:.2f}%")
)

recommendation_display["Profit / Unit"] = (
    recommendation_display["Profit / Unit"]
    .map(lambda x: f"${x:.2f}")
)

st.dataframe(
    recommendation_display,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# EXECUTIVE INSIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '7️⃣ Executive Insights'
    '</div>',
    unsafe_allow_html=True
)


# Highest profit product
top_product = product_summary.iloc[0]

# Lowest margin product
lowest_margin_product = product_summary.sort_values(
    "Gross_Margin_%"
).iloc[0]

# Highest margin product
highest_margin_product = product_summary.sort_values(
    "Gross_Margin_%",
    ascending=False
).iloc[0]

# Best division
best_division = division_summary.sort_values(
    "Total_Gross_Profit",
    ascending=False
).iloc[0]


st.markdown(
    f"""
    <div class="success-box">
    <b>Profit Leader:</b>
    {top_product['product_name']} generates
    ${top_product['Total_Gross_Profit']:,.2f} in gross profit,
    representing
    {top_product['Profit_Contribution_%']:.2f}% of filtered profit.
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <div class="warning-box">
    <b>Margin Risk:</b>
    {lowest_margin_product['product_name']} has the lowest gross
    margin at {lowest_margin_product['Gross_Margin_%']:.2f}%.
    This product should be reviewed for cost structure,
    pricing and sourcing efficiency.
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <div class="success-box">
    <b>Highest Margin:</b>
    {highest_margin_product['product_name']} has the highest gross
    margin at {highest_margin_product['Gross_Margin_%']:.2f}%.
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <div class="info-box">
    <b>Division Leader:</b>
    {best_division['division']} contributes
    ${best_division['Total_Gross_Profit']:,.2f}
    in gross profit and represents
    {best_division['Profit_Contribution_%']:.2f}%
    of filtered profit.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# GEOGRAPHIC ANALYSIS
# ============================================================

if "state" in filtered_df.columns:

    st.markdown(
        '<div class="section-title">'
        '8️⃣ Geographic Performance'
        '</div>',
        unsafe_allow_html=True
    )

    state_summary = (
        filtered_df
        .groupby("state", as_index=False)
        .agg(
            Sales=("sales", "sum"),
            Gross_Profit=("gross_profit", "sum"),
            Units=("units", "sum")
        )
        .sort_values(
            "Sales",
            ascending=False
        )
    )

    state_summary["Revenue_Contribution_%"] = (
        state_summary["Sales"]
        / total_sales
        * 100
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Top States by Sales")

        top_states = state_summary.head(10).sort_values(
            "Sales"
        )

        fig_states = px.bar(
            top_states,
            x="Sales",
            y="state",
            orientation="h",
            text="Sales",
            labels={
                "Sales": "Sales ($)",
                "state": "State"
            }
        )

        fig_states.update_traces(
            texttemplate="$%{text:,.0f}",
            textposition="outside"
        )

        fig_states.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_states,
            use_container_width=True
        )

    with col2:

        st.markdown("### Top States by Gross Profit")

        top_profit_states = (
            state_summary
            .sort_values(
                "Gross_Profit",
                ascending=False
            )
            .head(10)
            .sort_values("Gross_Profit")
        )

        fig_state_profit = px.bar(
            top_profit_states,
            x="Gross_Profit",
            y="state",
            orientation="h",
            text="Gross_Profit",
            labels={
                "Gross_Profit": "Gross Profit ($)",
                "state": "State"
            }
        )

        fig_state_profit.update_traces(
            texttemplate="$%{text:,.0f}",
            textposition="outside"
        )

        fig_state_profit.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_state_profit,
            use_container_width=True
        )


# ============================================================
# SHIPPING / LEAD TIME ANALYSIS
# ============================================================

if "shipment_lead_time" in filtered_df.columns:

    st.markdown(
        '<div class="section-title">'
        '9️⃣ Shipping Lead-Time Diagnostics'
        '</div>',
        unsafe_allow_html=True
    )

    lead_time = filtered_df[
        "shipment_lead_time"
    ].dropna()

    if len(lead_time) > 0:

        avg_lead_time = lead_time.mean()
        median_lead_time = lead_time.median()
        delayed_orders = (lead_time > 5).sum()
        delay_percentage = (
            delayed_orders / len(lead_time) * 100
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Average Lead Time",
                f"{avg_lead_time:.2f} days"
            )

        with c2:
            st.metric(
                "Median Lead Time",
                f"{median_lead_time:.2f} days"
            )

        with c3:
            st.metric(
                "Orders > 5 Days",
                f"{delay_percentage:.2f}%"
            )

        fig_lead = px.histogram(
            filtered_df,
            x="shipment_lead_time",
            nbins=20,
            labels={
                "shipment_lead_time":
                "Shipment Lead Time (Days)"
            }
        )

        fig_lead.update_layout(
            height=400
        )

        st.plotly_chart(
            fig_lead,
            use_container_width=True
        )

        st.info(
            "Note: Shipment lead-time metrics are screening "
            "indicators based on the order and ship dates in the "
            "dataset. They should not by themselves be interpreted "
            "as confirmed physical logistics congestion."
        )


# ============================================================
# DATASET SUMMARY
# ============================================================

with st.expander("📋 View Dataset Summary"):

    st.write(
        f"**Source file:** "
        f"{main_file.name if main_file else 'Unknown'}"
    )

    st.write(
        f"**Original records:** {len(df):,}"
    )

    st.write(
        f"**Filtered records:** {len(filtered_df):,}"
    )

    st.write(
        f"**Number of products:** "
        f"{filtered_df['product_name'].nunique():,}"
    )

    st.write(
        f"**Number of divisions:** "
        f"{filtered_df['division'].nunique():,}"
    )

    st.write(
        f"**Number of columns:** "
        f"{len(filtered_df.columns):,}"
    )

    st.write("### Available Columns")

    st.write(
        list(filtered_df.columns)
    )


# ============================================================
# DOWNLOAD FILTERED DATA
# ============================================================

st.markdown(
    '<div class="section-title">'
    '⬇️ Export Filtered Analysis'
    '</div>',
    unsafe_allow_html=True
)


csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv_data,
    file_name="Nassau_Candy_Filtered_Analysis.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#6b7280;">
    <b>Nassau Candy Product Line Profitability Analysis</b><br>
    Data Analytics & Business Intelligence Dashboard
    </div>
    """,
    unsafe_allow_html=True
)