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
# 🎨 CLEAN MODERN THEME (Light cards on dark bg)
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* ---------- App Background ---------- */
    .stApp {
        background: linear-gradient(180deg, #0b1220, #111827);
        color: #e5e7eb;
    }

    /* ---------- Sidebar ---------- */
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
        font-weight: 500;
    }

    section[data-testid="stSidebar"] button:hover {
        background: #2563eb;
        border-color: #2563eb;
        color: white;
    }

    /* ---------- Header ---------- */
    .title {
        font-size: 38px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 4px;
    }

    .subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 14px;
        margin-bottom: 24px;
    }

    /* ---------- Input ---------- */
    input {
        background: #020617 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-size: 15px !important;
    }

    /* ---------- Main Card ---------- */
    .card {
        background: #ffffff;
        color: #111827;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.35);
        max-width: 900px;
        margin: auto;
    }

    /* ---------- Info rows ---------- */
    .row {
        margin-top: 14px;
        font-size: 15px;
    }

    .label {
        font-weight: 600;
        color: #111827;
    }

    /* ---------- Address + Copy ---------- */
    .address {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-top: 12px;
        font-size: 15px;
        font-weight: 500;
        color: #111827;
        flex-wrap: wrap;
    }

    .copy-btn {
        padding: 5px 12px;
        border-radius: 8px;
        border: 1px solid #2563eb;
        background: #2563eb;
        color: white;
        font-size: 13px;
        cursor: pointer;
        font-weight: 600;
    }

    .copy-btn:hover {
        background: #1d4ed8;
    }

    /* ---------- Provider Button ---------- */
    .provider-btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 18px;
        border-radius: 10px;
        font-weight: 600;
        text-decoration: none;
        color: white !important;
        margin-top: 18px;
    }

    .jemena { background: #16a34a; }
    .powercor { background: #2563eb; }
    .ausnet { background: #7c3aed; }
    .default { background: #374151; }

    .provider-btn:hover {
        opacity: 0.9;
    }

    @media (max-width: 768px) {
        .card {
            margin: 0 8px;
        }
        .provider-btn {
            width: 100%;
            justify-content: center;
        }
    }
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
# Session state
# -------------------------------------------------
if "selected_location" not in st.session_state:
    st.session_state.selected_location = ""

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ Locations")
    st.caption("Select a location")

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
        <div class="address">
            <span><b>Address:</b> {address}</span>
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
        height=60
    )

    st.markdown(f"<div class='row'><span class='label'>Provider:</span> {site['provider']}</div>",
                unsafe_allow_html=True)

    if "jemena" in provider:
        cls = "jemena"
    elif "powercor" in provider:
        cls = "powercor"
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
