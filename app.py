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
# 🎨 Brand Theme (CSS)
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

    .stButton > button {
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 16px;
        font-weight: 600;
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
# Locations list
# -------------------------------------------------
locations_list = [
    "Claremont", "Shepparton", "Knoxfield", "Glen Iris", "Brisbane",
    "Broadmeadows", "Kilsyth", "Hastings", "Mornington", "Balwyn",
    "Greensborough", "Elsternwick", "Glen Waverley", "St Kilda Road",
    "RRC", "Clunes", "Chum Creek", "Mallana", "Lochend", "Indooroopilly"
]

# -------------------------------------------------
# Session state
# -------------------------------------------------
if "selected_location" not in st.session_state:
    st.session_state.selected_location = ""

# -------------------------------------------------
# Sidebar – Highlight selected
# -------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ Locations")
    st.caption("Tap a location to auto-fill")

    for loc in locations_list:
        if st.session_state.selected_location.lower() == loc.lower():
            st.markdown(
                f"""
                <div style="
                    padding:12px;
                    margin-bottom:8px;
                    border-radius:12px;
                    background:linear-gradient(90deg,#2563eb,#1d4ed8);
                    color:white;
                    font-weight:700;
                    text-align:center;
                ">
                    ⚡ {loc}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            if st.button(loc, use_container_width=True, key=f"loc_{loc}"):
                st.session_state.selected_location = loc.lower()
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
    value=st.session_state.selected_location,
    key="location_input"
)

# -------------------------------------------------
# Main logic
# -------------------------------------------------
if location:
    key = location.lower().strip()

    if key in SITES:
        site = SITES[key]

        st.success(
            f"📍 **{site['site']}**\n\n"
            f"👤 **Customer:** {site.get('customer', 'N/A')}"
        )

        # -------------------------------------------------
        # Address + Copy (FINAL FIX)
        # -------------------------------------------------
        address = site.get("address", "N/A")

        col1, col2 = st.columns([6, 1])

        with col1:
            st.write(f"**Address:** {address}")

        with col2:
            if st.button("📋 Copy", key="copy_address_btn"):
                st.toast("📍 Address copied!", icon="✅")

                components.html(
                    f"""
                    <script>
                        navigator.clipboard.writeText("{address}");
                    </script>
                    """,
                    height=0,
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
                    site["address"],
                    site.get("search"),
                    site.get("provider", "")
                )

            if not result["found"]:
                st.warning("⚠️ Could not auto-detect location. Verify manually.")
            else:
                if result["status"] == "OUTAGE":
                    st.error(f"⚡ POWER OUTAGE ({result['type']})")
                elif result["status"] == "OUTAGES":
                    st.error(f"⚡ MULTIPLE POWER OUTAGES ({result['type']})")
                else:
                    st.success("✅ No confirmed outage detected")
    else:
        st.error("❌ Location not found in database")
