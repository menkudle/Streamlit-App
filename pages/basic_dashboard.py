import streamlit as st
import pandas as pd
import numpy as np
from utils.auth import require_auth

require_auth()

st.title("📊 Interactive Dashboard")

# Generate Dummy Data
data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['Sales', 'Profit', 'Traffic']
)

# Filters
col1, col2 = st.columns(2)
with col1:
    filter_val = st.slider("Filter minimal value", -2.0, 2.0, 0.0)

filtered_data = data[data['Sales'] > filter_val]

# Visuals
st.subheader("Sales vs Profit Metrics")
st.line_chart(filtered_data)

st.subheader("Raw Data View")
st.dataframe(filtered_data, width='stretch')