import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta

st.set_page_config(page_title="Multi-Channel Sales & Marketing Dashboard",
                   layout="wide", initial_sidebar_state="expanded")

# -------------------------
# Helper / Sample Generators
# -------------------------
def make_revenue_series(days=30, base=800_000, jitter=120_000, seed=42):
    rng = np.random.default_rng(seed)
    vals = base + rng.normal(0, jitter, size=days).cumsum()
    vals = np.clip(vals - vals.min() + 300_000, 250_000, None)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=days)
    return pd.DataFrame({"Date": dates, "Revenue": vals.astype(int)})

def funnel_df():
    return pd.DataFrame({
        "Stage": ["Visits", "Add to Cart", "Checkout", "Orders"],
        "Count": [240_000, 68_000, 32_000, 9_300]
    })

def channel_perf_df():
    return pd.DataFrame([
        ["Amazon",        8_250_000, 3367, 825_000, 10.0, "28.5%",  12],
        ["D2C Website",   5_120_000, 2089, 640_000,  8.0, "35.2%",  18],
        ["Flipkart",      4_890_000, 1996, 570_000,  8.6, "26.8%",   5],
        ["Quick Commerce",3_240_000, 1620, 485_000,  6.7, "22.4%",  25],
        ["Offline",       3_100_000, 1240, 680_000,  4.6, "31.5%",  -3],
    ], columns=["Channel","Revenue","Orders","Ad Spend","ROAS","Profit Margin","Trend %"])

def marketing_table_df():
    return pd.DataFrame([
        ["Google Ads",   850_000, 12_500_000, 185_000, "1.48%", 3250, 262, 6_800_000, 8.0],
        ["Meta (FB & IG)",720_000,18_200_000, 145_000, "0.80%", 2880, 250, 5_040_000, 7.0],
        ["Amazon Ads",   580_000,  8_700_000, 122_000, "1.40%", 2320, 250, 5_220_000, 9.0],
        ["YouTube Ads",  320_000, 25_600_000,  51_000, "0.20%",  960, 333, 1_920_000, 6.0],
        ["Others",       730_000, 15_300_000,  95_000, "0.62%", 1825, 400, 3_650_000, 5.0],
    ], columns=["Platform","Spend","Impressions","Clicks","CTR","Conversions","CPA","Revenue","ROAS"])

def pnl_table_df():
    return pd.DataFrame([
        ["Gross Revenue",       "₹24,700,000", "₹21,950,000", "+12.5%", "₹186,200,000"],
        ["(-) Returns & Refunds","₹1,235,000",  "₹1,097,500",  "+12.5%", "₹9,310,000"],
        ["Net Revenue",         "₹23,465,000", "₹20,852,500", "+12.5%", "₹176,890,000"],
        ["(-) COGS",            "₹9,386,000",  "₹8,341,000",  "+12.5%", "₹70,756,000"],
        ["Gross Profit",        "₹14,079,000", "₹12,511,500", "+12.5%", "₹106,134,000"],
        ["(-) Marketing Spend", "₹3,200,000",  "₹2,955,000",   "+8.3%", "₹24,120,000"],
        ["(-) Platform Fees",   "₹1,482,000",  "₹1,317,000",  "+12.5%", "₹11,173,400"],
        ["(-) Logistics",       "₹988,000",    "₹878,000",    "+12.5%", "₹7,448,800"],
        ["(-) Other OpEx",      "₹741,000",    "₹658,500",    "+12.5%", "₹5,586,700"],
        ["EBITDA",              "₹7,668,000",  "₹6,703,000",  "+14.4%", "₹57,805,100"],
        ["(-) Depreciation",    "₹247,000",    "₹247,000",      "0%",   "₹1,862,000"],
        ["(-) Interest",        "₹123,500",    "₹123,500",      "0%",   "₹931,000"],
        ["Net Profit",          "₹7,297,500",  "₹6,332,500",  "+15.2%","₹55,012,100"],
        ["Net Margin %",        "29.5%",       "28.8%",       "+0.7pp","29.5%"],
    ], columns=["Metric","This Month","Last Month","Change %","YTD"])

def cohort_df():
    # Build the exact table shown
    rows = [
        ["Jan 2025", 2450, "100%", "-", "-", "-", "-", "-", "-"],
        ["Dec 2024", 2180, "100%", "42%", "35%", "-", "-", "-", "-"],
        ["Nov 2024", 2340, "100%", "45%", "38%", "32%", "-", "-", "-"],
        ["Oct 2024", 1980, "100%", "44%", "36%", "31%", "28%", "-", "-"],
        ["Sep 2024", 2120, "100%", "48%", "40%", "34%", "30%", "27%", "-"],
        ["Aug 2024", 1850, "100%", "43%", "35%", "30%", "26%", "24%", "22%"],
    ]
    return pd.DataFrame(rows, columns=["Cohort","Users","Month 0","Month 1","Month 2","Month 3","Month 4","Month 5","Month 6"])

# --------------
# Sidebar Filters
# --------------
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Time range",
    options=["Today", "Last 7 Days", "Last 30 Days", "Last Quarter", "Year to Date"],
    index=2
)
start_date = st.sidebar.date_input("Start date", value=date.today() - timedelta(days=30))
end_date   = st.sidebar.date_input("End date",   value=date.today())
st.sidebar.button("↻ Refresh")

# ----------------
# Page Header / KPIs
# ----------------
st.title("Omnichannel Performance Dashboard")

kpi_cols = st.columns(6)
kpi_cols[0].metric("Total Revenue", "₹24.7M", "+12.5%")
kpi_cols[1].metric("Total Ad Spend", "₹3.2M", "+8.3%")
kpi_cols[2].metric("ROAS", "7.72x", "+3.8%")
kpi_cols[3].metric("Net Profit", "₹8.9M", "+15.2%")
kpi_cols[4].metric("CAC", "₹287", "-5.3%")
kpi_cols[5].metric("AOV", "₹2,450", "+7.8%")

st.write("")  # small spacer

# ------------
# Tabs (pages)
# ------------
tabs = st.tabs(["Overview", "Sales Channels", "Marketing", "P&L Analysis", "Cohort Analysis"])

# ----------
# OVERVIEW
# ----------
with tabs[0]:
    left1, right1 = st.columns(2)
    with left1:
        st.subheader("Revenue Trend (30 Days)")
        rev_df = make_revenue_series(30)
        fig = px.line(rev_df, x="Date", y="Revenue", markers=True)
        fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

    with right1:
        st.subheader("Channel Performance (Revenue Share)")
        chan_df = channel_perf_df()
        pie_fig = px.pie(chan_df, names="Channel", values="Revenue", hole=0.35)
        st.plotly_chart(pie_fig, use_container_width=True)

    left2, right2 = st.columns(2)
    with left2:
        st.subheader("Marketing Mix (Spend vs Revenue)")
        mk = marketing_table_df()
        mix_fig = go.Figure(data=[
            go.Bar(name="Spend", x=mk["Platform"], y=mk["Spend"]),
            go.Bar(name="Revenue", x=mk["Platform"], y=mk["Revenue"])
        ])
        mix_fig.update_layout(barmode="group", margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(mix_fig, use_container_width=True)

    with right2:
        st.subheader("Conversion Funnel")
        fdf = funnel_df()
        funnel_fig = px.funnel(fdf, x="Count", y="Stage")
        st.plotly_chart(funnel_fig, use_container_width=True)

    st.subheader("Top Performing Channels - Quick View")
    st.dataframe(channel_perf_df(), use_container_width=True, hide_index=True)

    # Extra: LTV & Segment Value (synthetic)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("LTV by Acquisition Channel")
        ltv = pd.DataFrame({
            "Channel": ["Amazon","D2C Website","Flipkart","Quick Commerce","Offline"],
            "LTV": [5400, 6100, 4900, 4200, 3800]
        })
        st.plotly
