import json
import streamlit as st
import streamlit.components.v1 as components
from selenium_checker import check_power_status  # (kept if needed later)

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Power Outage Checker",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# 🎨 Custom Brand Theme + Provider Buttons (CSS)
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background-color: #0f172a;
        color: #e5e7eb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #020617;
    }

    section[data-testid="stSidebar"] button {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px;
        font-weight: 500;
    }

    section[data-testid="stSidebar"] button:hover {
        background-color: #1d4ed8;
    }

    /* Alerts */
    .stAlert {
        border-radius: 14px;
    }

    /* ---------------- Provider button styles ---------------- */
    .provider-link-btn a {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 18px;
        border-radius: 999px;
        color: #ffffff !important;
        text-decoration: none;
        font-weight: 600;
        font-size: 14px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.35);
        transition: all 0.25s ease;
    }

    /* Jemena - Green */
    .provider-jemena a {
        background: linear-gradient(90deg, #16a34a, #22c55e);
    }
    .provider-jemena a:hover {
        box-shadow: 0 8px 22px rgba(34,197,94,0.55);
        transform: translateY(-1px);
    }

    /* Powercor - Blue */
    .provider-powercor a {
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
    }
    .provider-powercor a:hover {
        box-shadow: 0 8px 22px rgba(37,99,235,0.55);
        transform: translateY(-1px);
    }

    /* AusNet - Purple */
    .provider-ausnet a {
        background: linear-gradient(90deg, #7c3aed, #9333ea);
    }
    .provider-ausnet a:hover {
        box-shadow: 0 8px 22px rgba(147,51,234,0.55);
        transform: translateY(-1px);
    }

    /* Default */
    .provider-default a {
        background: linear-gradient(90deg, #1f6feb, #2563eb);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Load sites database
# -------------------------------------------------
with open("sites.json", "r", encoding="utf-8") as f:
    SITES = json.load(f)

locations_list = list(SITES.keys())

# -------------------------------------------------
# Session state
# -------------------------------------------------
if "selected_location" not in st.session_state:
    st.session_state.selected_location = ""

# -------------------------------------------------
# Sidebar – Locations
# -------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ Locations")
    st.caption("Tap a location to auto-fill")

    for loc in locations_list:
        if st.button(loc.title(), use_container_width=True, key=f"loc_{loc}"):
            st.session_state.selected_location = loc
            st.rerun()

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown(
    """
    <div style="text-align:center;">
        <h1 style="margin-bottom:4px;">⚡ Power Outage Checker</h1>
        <p style="opacity:0.75;">
            Auto-check power status using live provider outage maps
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Location input
# -------------------------------------------------
location = st.text_input(
    "📍 Enter Location / Suburb",
    value=st.session_state.selected_location
)

# -------------------------------------------------
# Main view
# -------------------------------------------------
if location and location.lower() in SITES:
    site = SITES[location.lower()]
    address = site.get("address", "N/A")

    st.success(
        f"📍 **{site['site']}**\n\n"
        f"👤 **Customer:** {site.get('customer', 'N/A')}"
    )

    # -------------------------------------------------
    # Address (WHITE) + HTML Copy button (NO rerun)
    # -------------------------------------------------
    components.html(
        f"""
        <div style="
            display:flex;
            align-items:center;
            gap:12px;
            margin:10px 0;
        ">
            <div style="
                font-weight:600;
                color:#ffffff;
                font-size:16px;
            ">
                Address: {address}
            </div>

            <button
                style="
                    padding:6px 12px;
                    border-radius:8px;
                    border:none;
                    background:#2563eb;
                    color:white;
                    cursor:pointer;
                    font-weight:600;
                "
                onclick="
                    navigator.clipboard.writeText('{address}');
                    this.innerText='✓ Copied';
                    this.style.background='#16a34a';
                "
            >
                📋 Copy
            </button>
        </div>
        """,
        height=60,
    )

    # -------------------------------------------------
    # Provider
    # -------------------------------------------------
    st.write(f"**Provider:** {site['provider']}")

    # Provider-based color class
    provider_name = site["provider"].lower()
    if "jemena" in provider_name:
        provider_class = "provider-jemena"
    elif "powercor" in provider_name:
        provider_class = "provider-powercor"
    elif "ausnet" in provider_name:
        provider_class = "provider-ausnet"
    else:
        provider_class = "provider-default"

    # -------------------------------------------------
    # Styled Provider Outage Page button
    # -------------------------------------------------
    st.markdown(
        f"""
        <div class="provider-link-btn {provider_class}">
            <a href="{site['url']}" target="_blank">
                🔗 Open Provider Outage Page
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

elif location:
    st.error("❌ Location not found in database")
