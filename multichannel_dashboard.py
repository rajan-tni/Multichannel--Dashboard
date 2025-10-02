import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

"""
Multi‑Channel Marketing Dashboard
================================

This Streamlit app provides an easy way to explore multi‑channel marketing data.  
It accepts a CSV file with the following columns:

* ``Date`` – the date of the record (e.g. ``2025‑01‑01``)
* ``Channel`` – the marketing channel (e.g. Email, Social Media, SEO, SEM, Referral)
* ``Leads`` – number of leads generated on that date for that channel
* ``Cost`` – total spend for that channel on that date
* ``Conversions`` – number of conversions from the leads
* ``Revenue`` – revenue generated from those conversions

If no file is uploaded, the app falls back to a sample dataset bundled alongside this script
(``sample_multichannel_data.csv``).  You can filter the data by date range and channel, review
key performance indicators (KPIs) at a glance, and explore interactive charts.

To run this app locally:

```
streamlit run multichannel_dashboard.py
```

Then open the provided local URL in your browser.  To use your own data, click
the “Upload a CSV” control in the sidebar.
"""

# Set up the page configuration
st.set_page_config(
    page_title="Multi‑Channel Marketing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📊 Multi‑Channel Marketing Dashboard")


@st.cache_data
def load_data(csv_path: Path | None) -> pd.DataFrame:
    """Load marketing data from the provided CSV or from the bundled sample.

    Parameters
    ----------
    csv_path : Path or None
        Path to the user‑uploaded CSV.  If ``None`` or the file does not exist,
        the function loads the bundled ``sample_multichannel_data.csv``.

    Returns
    -------
    pandas.DataFrame
        Loaded and parsed DataFrame with a parsed ``Date`` column.
    """
    # Determine the data source: user upload or bundled sample
    if csv_path is None or not csv_path.exists():
        csv_path = Path(__file__).parent / "sample_multichannel_data.csv"
    df = pd.read_csv(csv_path)
    # Parse the Date column so that Streamlit's date widgets recognise it
    df["Date"] = pd.to_datetime(df["Date"])
    return df


# File upload control in the sidebar
uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV (Date, Channel, Leads, Cost, Conversions, Revenue)",
    type=["csv"],
    help="If no file is uploaded, a sample dataset is used."
)

# Write uploaded file to a temporary path for pandas
temporary_path: Path | None = None
if uploaded_file is not None:
    temporary_path = Path("uploaded_multichannel_data.csv")
    with open(temporary_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

# Load data into a DataFrame
df = load_data(temporary_path)


# Sidebar filters
st.sidebar.header("Filters")

# Channel filter: allow multi‑select of all available channels
channels = ["All"] + sorted(df["Channel"].unique().tolist())
selected_channels = st.sidebar.multiselect(
    "Channel",
    channels,
    default=["All"],
    help="Choose one or more marketing channels to analyse"
)

# Date range filter: allow selection of a start and end date
min_date, max_date = df["Date"].min().date(), df["Date"].max().date()
date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    help="Select the start and end dates to filter your data"
)

# Apply filters to the DataFrame
filtered_df = df.copy()
if selected_channels and "All" not in selected_channels:
    filtered_df = filtered_df[filtered_df["Channel"].isin(selected_channels)]
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered_df = filtered_df[(filtered_df["Date"] >= start_date) & (filtered_df["Date"] <= end_date)]


# Compute KPI metrics
total_leads = int(filtered_df["Leads"].sum())
total_conversions = int(filtered_df["Conversions"].sum())
total_revenue = float(filtered_df["Revenue"].sum())
total_cost = float(filtered_df["Cost"].sum())

conversion_rate = (total_conversions / total_leads) if total_leads else 0.0
average_cpl = (total_cost / total_leads) if total_leads else 0.0
roi = ((total_revenue - total_cost) / total_cost) if total_cost else 0.0


# Display KPIs in a single row with 6 columns
kpi_cols = st.columns(6)
kpi_cols[0].metric("Total Leads", f"{total_leads:,}")
kpi_cols[1].metric("Total Conversions", f"{total_conversions:,}")
kpi_cols[2].metric("Conversion Rate", f"{conversion_rate:.2%}")
kpi_cols[3].metric("Total Revenue", f"${total_revenue:,.0f}")
kpi_cols[4].metric("Total Cost", f"${total_cost:,.0f}")
kpi_cols[5].metric("Return on Investment", f"{roi:.2%}")

st.divider()


# Leads over time line chart
leads_over_time = filtered_df.groupby("Date", as_index=False)["Leads"].sum()
line_fig = px.line(
    leads_over_time,
    x="Date",
    y="Leads",
    title="Leads Over Time",
    markers=True,
)
line_fig.update_layout(
    margin=dict(l=20, r=20, t=40, b=20),
    hovermode="x unified",
)
st.plotly_chart(line_fig, use_container_width=True)


# Conversions by channel bar chart
conversions_by_channel = (
    filtered_df.groupby("Channel", as_index=False)["Conversions"].sum()
    .sort_values("Conversions", ascending=False)
)
bar_conv_fig = px.bar(
    conversions_by_channel,
    x="Channel",
    y="Conversions",
    title="Conversions by Channel",
)
bar_conv_fig.update_layout(
    margin=dict(l=20, r=20, t=40, b=20),
)
st.plotly_chart(bar_conv_fig, use_container_width=True)


# Revenue by channel bar chart
revenue_by_channel = (
    filtered_df.groupby("Channel", as_index=False)["Revenue"].sum()
    .sort_values("Revenue", ascending=False)
)
bar_rev_fig = px.bar(
    revenue_by_channel,
    x="Channel",
    y="Revenue",
    title="Revenue by Channel",
)
bar_rev_fig.update_layout(
    margin=dict(l=20, r=20, t=40, b=20),
)
st.plotly_chart(bar_rev_fig, use_container_width=True)


# Cost vs Conversions scatter plot
cost_vs_conv = (
    filtered_df.groupby("Channel", as_index=False)[["Cost", "Conversions"]].sum()
)
scatter_fig = px.scatter(
    cost_vs_conv,
    x="Cost",
    y="Conversions",
    size="Conversions",
    color="Channel",
    title="Cost vs. Conversions by Channel",
    hover_name="Channel",
)
scatter_fig.update_layout(
    margin=dict(l=20, r=20, t=40, b=20),
)
st.plotly_chart(scatter_fig, use_container_width=True)


# Display raw data in an expandable section
with st.expander("See raw data"):
    st.dataframe(
        filtered_df.sort_values("Date").reset_index(drop=True),
        use_container_width=True,
    )
