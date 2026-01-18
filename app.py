import json
import streamlit as st
import streamlit.components.v1 as components
from selenium_checker import check_power_status

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
# Theme
# -------------------------------------------------
st.markdown(
    """
    <style>
    .stApp { background-color:#0f172a; color:#e5e7eb; }
    section[data-testid="stSidebar"] { background-color:#020617; }

    section[data-testid="stSidebar"] button {
        background:#2563eb; color:white; border:none;
        border-radius:10px; padding:10px; font-weight:500;
    }

    .stButton>button {
        background:linear-gradient(90deg,#2563eb,#1d4ed8);
        color:white; border-radius:12px; border:none;
        padding:10px 16px; font-weight:600;
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

locations_list = list(SITES.keys())

# -------------------------------------------------
# Session state
# -------------------------------------------------
if "selected_location" not in st.session_state:
    st.session_state.selected_location = ""

if "copy_trigger" not in st.session_state:
    st.session_state.copy_trigger = False

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ Locations")
    st.caption("Tap a location to auto-fill")

    for loc in locations_list:
        if st.button(loc.title(), use_container_width=True):
            st.session_state.selected_location = loc
            st.rerun()

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown(
    """
    <div style="text-align:center;">
        <h1>⚡ Power Outage Checker</h1>
        <p style="opacity:.7">
            Auto-check power status using live provider outage maps
        </p>
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
# MAIN VIEW (stable)
# -------------------------------------------------
if location and location.lower() in SITES:
    site = SITES[location.lower()]
    address = site.get("address", "N/A")

    st.success(
        f"📍 **{site['site']}**\n\n"
        f"👤 **Customer:** {site.get('customer','N/A')}"
    )

    # ---------------- Address row (ALWAYS visible)
    col1, col2 = st.columns([6,1])

    with col1:
        st.write(f"**Address:** {address}")

    with col2:
        st.button(
            "📋 Copy",
            key="copy_btn",
            on_click=lambda: st.session_state.update(
                {"copy_trigger": True}
            )
        )

    # ---------------- Clipboard JS (isolated + stable)
    if st.session_state.copy_trigger:
        components.html(
            f"""
            <script>
                navigator.clipboard.writeText("{address}");
            </script>
            """,
            height=0
        )
        st.toast("📍 Address copied!", icon="✅")
        st.session_state.copy_trigger = False

    st.write(f"**Provider:** {site['provider']}")
    st.link_button("🔗 Open Provider Outage Page", site["url"])

    if st.button("🔍 Auto-Check Power Status", use_container_width=True):
        with st.spinner("Checking live outage map..."):
            result = check_power_status(
                site["url"],
                address,
                site.get("search"),
                site.get("provider","")
            )

        if not result["found"]:
            st.warning("⚠️ Could not auto-detect location.")
        elif result["status"] in ["OUTAGE","OUTAGES"]:
            st.error(f"⚡ {result['status']} ({result['type']})")
        else:
            st.success("✅ No confirmed outage detected")
