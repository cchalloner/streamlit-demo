import streamlit as st
import pandas as pd
import numpy as np 


# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Uber Pickups – NYC",
    page_icon="🚖",
    layout="wide",
)

# ── Title & intro ─────────────────────────────────────────────────────────────
st.title("🚖 Uber Pickups in New York City")
st.markdown(
    "Exploring **April 2014** Uber pickup data. "
    "Use the controls in the sidebar to filter by hour of day."
)

# ── Load data ─────────────────────────────────────────────────────────────────
DATE_COL = "date/time"
DATA_URL = (
    "https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
)

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.rename(columns=lambda x: x.strip().lower(), inplace=True)
    data["date/time"] = pd.to_datetime(data["date/time"])
    return data

with st.spinner("Loading data…"):
    data = load_data(20000)

# ── Sidebar controls ──────────────────────────────────────────────────────────
st.sidebar.header("Filter Options")
hour = st.sidebar.slider("Hour of day", 0, 23, 17)
show_raw = st.sidebar.checkbox("Show raw data", value=False)

# ── Filter ────────────────────────────────────────────────────────────────────
filtered = data[data["date/time"].dt.hour == hour]

# ── Metrics row ───────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Total pickups (dataset)", f"{len(data):,}")
col2.metric(f"Pickups at hour {hour}:00", f"{len(filtered):,}")
col3.metric("% of total", f"{len(filtered)/len(data)*100:.1f}%")

st.divider()

# ── Map ───────────────────────────────────────────────────────────────────────
st.subheader(f"📍 Pickup locations at {hour}:00")
st.map(filtered.rename(columns={"lat": "latitude", "lon": "longitude"}))

st.divider()

# ── Bar chart ─────────────────────────────────────────────────────────────────
st.subheader("📊 Pickups by hour (full dataset)")

hist = (
    data["date/time"]
    .dt.hour.value_counts()
    .sort_index()
    .reset_index()
)
hist.columns = ["Hour", "Pickups"]

st.bar_chart(hist.set_index("Hour"))

# ── Raw data ──────────────────────────────────────────────────────────────────
if show_raw:
    st.subheader("Raw data (first 500 rows)")
    st.dataframe(data.head(500), use_container_width=True)

st.caption("Data: Uber TLC FOIL response · Streamlit demo dataset")
