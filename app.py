import json
import streamlit as st
import streamlit.components.v1 as components

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Power Outage Checker",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# 🎨 SAAS DASHBOARD THEME (LIGHT)
# -------------------------------------------------
st.markdown("""
<style>
/* App background */
.stApp {
    background-color: #f5f7fb;
    color: #111827;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e5e7eb;
}

section[data-testid="stSidebar"] h2 {
    color: #111827;
}

section[data-testid="stSidebar"] button {
    background-color: #ffffff;
    color: #111827;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 6px;
    font-size: 14px;
    text-align: left;
}

section[data-testid="stSidebar"] button:hover {
    background-color: #2563eb;
    border-color: #2563eb;
    color: #ffffff;
}

/* Header */
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
}

.header-title {
    font-size: 28px;
    font-weight: 700;
}

.header-subtitle {
    font-size: 14px;
    color: #6b7280;
}

/* Input */
input {
    background-color: #ffffff !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 10px !important;
    padding: 10px !important;
}

/* Card */
.card {
    background-color: #ffffff;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    max-width: 900px;
}

/* Labels */
.label {
    font-size: 13px;
    color: #6b7280;
    margin-bottom: 4px;
}

.value {
    font-size: 15px;
    font-weight: 600;
    color: #111827;
}

/* Address row */
.address-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 12px;
    flex-wrap: wrap;
}

.copy-btn {
    padding: 4px 10px;
    border-radius: 6px;
    border: 1px solid #2563eb;
    background-color: #2563eb;
    color: white;
    font-size: 12px;
    cursor: pointer;
}

/* Provider button */
.provider-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    margin-top: 18px;
    padding: 10px 16px;
    border-radius: 10px;
    background-color: #2563eb;
    color: white !important;
    font-weight: 600;
    text-decoration: none;
}

.provider-btn:hover {
    background-color: #1d4ed8;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Load data
# -------------------------------------------------
with open("sites.json", "r", encoding="utf-8") as f:
    SITES = json.load(f)

locations = list(SITES.keys())

# -------------------------------------------------
# Session state
# -------------------------------------------------
if "selected_location" not in st.session_state:
    st.session_state.selected_location = ""

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ Locations")
    for loc in locations:
        if st.button(loc.title(), use_container_width=True):
            st.session_state.selected_location = loc
            st.rerun()

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown("""
<div class="header">
    <div>
        <div class="header-title">⚡ Power Outage Checker</div>
        <div class="header-subtitle">
            Quickly access provider outage pages for each site
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Input
# -------------------------------------------------
location = st.text_input(
    "Enter Location / Suburb",
    value=st.session_state.selected_location,
    placeholder="Search by suburb name"
)

# -------------------------------------------------
# Main content
# -------------------------------------------------
if location and location.lower() in SITES:
    site = SITES[location.lower()]
    address = site.get("address", "N/A")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(f"### 📍 {site['site']}")
    st.markdown(f"<div class='label'>Customer</div><div class='value'>{site.get('customer','N/A')}</div>", unsafe_allow_html=True)

    components.html(f"""
        <div class="address-row">
            <div>
                <div class="label">Address</div>
                <div class="value">{address}</div>
            </div>
            <button class="copy-btn"
                onclick="
                    navigator.clipboard.writeText('{address}');
                    this.innerText='Copied';
                    setTimeout(()=>this.innerText='Copy',1500);
                ">
                Copy
            </button>
        </div>
    """, height=60)

    st.markdown(f"<div class='label'>Provider</div><div class='value'>{site['provider']}</div>", unsafe_allow_html=True)

    st.markdown(f"""
        <a class="provider-btn" href="{site['url']}" target="_blank">
            🔗 Open Provider Outage Page
        </a>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif location:
    st.error("Location not found")
else:
    st.info("Select a location from the sidebar")
