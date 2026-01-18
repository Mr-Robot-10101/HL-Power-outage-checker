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
# 🎨 Custom Brand Theme (CSS)
# -------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0f172a;
        color: #e5e7eb;
    }

    section[data-testid="stSidebar"] {
        background-color: #020617;
    }

    section[data-testid="stSidebar"] button {
        background-color: #020617;
        color: #e5e7eb;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 10px;
        font-weight: 500;
    }

    section[data-testid="stSidebar"] button:hover {
        background-color: #1f6feb;
        color: white;
        border-color: #1f6feb;
    }

    .stButton > button {
        background: linear-gradient(90deg, #1f6feb, #2563eb);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 16px;
        font-weight: 600;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
    }

    .stAlert {
        border-radius: 14px;
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

# -------------------------------------------------
# Locations list (from DB keys)
# -------------------------------------------------
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
# Main logic
# -------------------------------------------------
if location and location.lower() in SITES:
    site = SITES[location.lower()]
    address = site.get("address", "N/A")

    st.success(
        f"📍 **{site['site']}**\n\n"
        f"👤 **Customer:** {site.get('customer', 'N/A')}"
    )

    # -------------------------------------------------
    # Address (WHITE text) + HTML Copy button (NO RERUN)
    # -------------------------------------------------
    components.html(
        f"""
        <div style="
            display:flex;
            align-items:center;
            gap:12px;
            margin: 10px 0 6px 0;
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

    st.link_button(
        "🔗 Open Provider Outage Page",
        site["url"]
    )

    # -------------------------------------------------
    # Auto-check power status
    # -------------------------------------------------
    if st.button("🔍 Auto-Check Power Status", use_container_width=True):
        with st.spinner("Checking live outage map..."):
            result = check_power_status(
                site["url"],
                address,
                site.get("search"),
                site.get("provider", "")
            )

        if not result["found"]:
            st.warning("⚠️ Could not auto-detect location. Verify manually.")
        else:
            if result["status"] in ["OUTAGE", "OUTAGES"]:
                st.error(f"⚡ {result['status']} ({result['type']})")
            else:
                st.success("✅ No confirmed outage detected")
else:
    if location:
        st.error("❌ Location not found in database")
