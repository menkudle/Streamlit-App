import streamlit as st
import pandas as pd
import plotly.express as px
import os
from utils.auth import require_auth
from utils.data_generator import ensure_data_exists

st.set_page_config(layout="wide")

# 1. Security & Config
require_auth()


# 2. Efficient Data Loading
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data_from_csv():
    # Ensure file exists using our utility
    file_path = ensure_data_exists()

    # Read CSV
    df = pd.read_csv(file_path)

    # Convert Date column back to datetime objects (CSV stores them as strings)
    df['Date'] = pd.to_datetime(df['Date'])
    # This ensures KPIs and Charts match perfectly.
    if len(df) > 1000:
        df = df.sample(n=1000, random_state=42)

    return df


with st.spinner("Loading cached dataset..."):
    df = load_data_from_csv()

# 3. Sidebar (Global Filters)
# These trigger a full rerun because they affect ALL fragments
st.sidebar.header("🔍 Global Filters")
selected_regions = st.sidebar.multiselect(
    "Regions", df['Region'].unique(), default=df['Region'].unique()
)
selected_categories = st.sidebar.multiselect(
    "Categories", df['Category'].unique(), default=df['Category'].unique()
)

# Filter Data Globally
filtered_df = df[
    (df['Region'].isin(selected_regions)) &
    (df['Category'].isin(selected_categories))
    ]

st.title("🚀 Detailed Analysis with Plotly Charts")
st.markdown("""
This dashboard uses **`@st.fragment`** for independent component updating.
Try changing the *Time Interval* or *Map Style* below—notice the whole page doesn't reload!
""")
st.markdown("---")


# --- FRAGMENT 1: KPI Section ---
# This is fast, so we don't strictly need a fragment, but good for isolation
def render_kpis(data):
    total_sales = data['Sales'].sum()
    total_profit = data['Profit'].sum()
    avg_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Revenue", f"${total_sales / 1e6:.2f}M", "12%")
    c2.metric("Profit", f"${total_profit / 1e6:.2f}M", "-5%")
    c3.metric("Margin", f"{avg_margin:.1f}%", "1.2%")
    c4.metric("Transactions", len(data), "Live")


render_kpis(filtered_df)

st.markdown("---")


# --- FRAGMENT 2: Trend Analysis (Interactive) ---
@st.fragment
def render_trend_section(data):
    st.subheader("📈 Interactive Trend Analysis")

    # LOCAL CONTROL: This only re-runs this specific function!
    col_ctrl, col_chart = st.columns([1, 4])
    with col_ctrl:
        st.info("⚡ Fragment Control")
        interval = st.radio("Time Grain", ["Daily", "Weekly", "Monthly"])
        chart_type = st.selectbox("Chart Type", ["Line", "Bar", "Area"])

    # Process Data based on Local Control
    freq_map = {"Daily": "D", "Weekly": "W", "Monthly": "ME"}
    trend_data = data.groupby(pd.Grouper(key='Date', freq=freq_map[interval]))['Sales'].sum().reset_index()

    with col_chart:
        chart_color = ['#00CC96']
        if chart_type == "Line":
            fig = px.line(trend_data, x='Date', y='Sales', markers=True, template="plotly_dark", color_discrete_sequence=chart_color)
        elif chart_type == "Bar":
            fig = px.bar(trend_data, x='Date', y='Sales', template="plotly_dark", color_discrete_sequence=chart_color)
        else:
            fig = px.area(trend_data, x='Date', y='Sales', template="plotly_dark", color_discrete_sequence=chart_color)

        st.plotly_chart(fig, width='stretch')


render_trend_section(filtered_df)


# --- FRAGMENT 3: Geographic & Scatter Analysis ---
@st.fragment
def render_map_section(data):
    c1, c2 = st.columns([3, 2])

    with c1:
        st.subheader("🗺️ Geographic Distribution")

        # LOCAL CONTROL for Map
        map_style = st.selectbox("Map Style", ["open-street-map", "carto-positron", "carto-darkmatter"], index=0)

        fig_map = px.scatter_mapbox(
            data.sample(min(2000, len(data))),  # Downsample for speed
            lat="Latitude", lon="Longitude",
            color="Region", size="Sales",
            color_continuous_scale=px.colors.cyclical.IceFire,
            zoom=1, height=500, mapbox_style=map_style
        )
        fig_map.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig_map, width='stretch')

    with c2:
        st.subheader("💹 Scatter Analysis")
        # Scatter is complex, so isolating it helps performance
        x_axis = st.selectbox("X-Axis", ["Sales", "Discount", "Rating"])

        fig_scatter = px.scatter(
            data.sample(min(1000, len(data))),
            x=x_axis, y="Profit",
            color="Category", size="Sales",
            template="plotly_dark", opacity=0.7
        )
        st.plotly_chart(fig_scatter, width='stretch')


render_map_section(filtered_df)