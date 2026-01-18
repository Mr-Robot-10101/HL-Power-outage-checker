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
# 🎨 CLEAN & READABLE DARK THEME
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* Background */
    .stApp {
        background: linear-gradient(180deg, #020617, #020617);
        color: #e5e7eb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid #1f2937;
    }

    section[data-testid="stSidebar"] button {
        background: #020617;
        color: #e5e7eb;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 10px;
    }

    section[data-testid="stSidebar"] button:hover {
        background: #2563eb;
        border-color: #2563eb;
        color: white;
    }

    /* Header */
    .title {
        font-size: 36px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 6px;
    }

    .subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* Input */
    input {
        background: #020617 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        padding: 12px !important;
    }

    /* Card */
    .card {
        background: #020617;
        border: 1px solid #1f2937;
        border-radius: 14px;
        padding: 20px;
        max-width: 900px;
        margin: 20px auto;
    }

    /* Address row */
    .address-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 12px;
        color: #ffffff;
        font-size: 15px;
        flex-wrap: wrap;
    }

    .copy-btn {
        padding: 5px 12px;
        border-radius: 8px;
        border: none;
        background: #2563eb;
        color: white;
        font-size: 13px;
        cursor: pointer;
    }

    .copy-btn:hover {
        background: #1d4ed8;
    }

    /* Provider button */
    .provider-btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 18px;
        border-radius: 10px;
        font-weight: 600;
        text-decoration: none;
        color: white !important;
        margin-top: 16px;
    }

    .powercor { background: #2563eb; }
    .jemena { background: #16a34a; }
    .ausnet { background: #7c3aed; }
    .default { background: #374151; }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Load data
# -------------------------------------------------
with open("sites.json", "r", encoding="utf-8") as f:
    SITES = json.load(f)

locations = list(SITES.keys())

# -------------------------------------------------
# Session
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
st.markdown(
    """
    <div class="title">⚡ Power Outage Checker</div>
    <div class="subtitle">
        Quickly access provider outage pages for each site
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Input
# -------------------------------------------------
location = st.text_input(
    "📍 Enter Location / Suburb",
    value=st.session_state.selected_location
)

# -------------------------------------------------
# Main
# -------------------------------------------------
if location and location.lower() in SITES:
    site = SITES[location.lower()]
    address = site.get("address", "N/A")
    provider = site.get("provider", "").lower()

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(f"### 📍 {site['site']}")
    st.markdown(f"**Customer:** {site.get('customer','N/A')}")

    components.html(
        f"""
        <div class="address-row">
            <b>Address:</b> {address}
            <button class="copy-btn"
                onclick="
                    navigator.clipboard.writeText('{address}');
                    this.innerText='Copied';
                    setTimeout(()=>this.innerText='Copy',1500);
                ">
                Copy
            </button>
        </div>
        """,
        height=45
    )

    st.markdown(f"**Provider:** {site['provider']}")

    if "powercor" in provider:
        cls = "powercor"
    elif "jemena" in provider:
        cls = "jemena"
    elif "ausnet" in provider:
        cls = "ausnet"
    else:
        cls = "default"

    st.markdown(
        f"""
        <a class="provider-btn {cls}" href="{site['url']}" target="_blank">
            🔗 Open Provider Outage Page
        </a>
        """,
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

elif location:
    st.error("❌ Location not found")
else:
    st.info("👈 Select a location from the sidebar")
