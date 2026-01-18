import json
import streamlit as st
import pyperclip
from selenium_checker import check_power_status

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Power Outage Checker",
    page_icon="⚡",
    layout="centered"
)

# -------------------------------------------------
# Load sites database
# -------------------------------------------------
with open("sites.json", "r", encoding="utf-8") as f:
    SITES = json.load(f)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown(
    """
    <div style="text-align:center;">
        <h1 style="white-space: nowrap; margin-bottom: 5px;">
            ⚡ Power Outage Checker
        </h1>
        <p style="opacity: 0.7; margin-top: 0;">
            Auto-check power status using live provider outage maps
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Location input
# -------------------------------------------------
location = st.text_input("📍 Enter Location / Suburb")

# -------------------------------------------------
# Main logic
# -------------------------------------------------
if location:
    key = location.lower().strip()

    if key in SITES:
        site = SITES[key]

        # Success box
        st.success(
            f"📍 **{site['site']}**\n\n"
            f"👤 **Customer:** {site.get('customer', 'N/A')}"
        )

        # -------------------------------------------------
        # Address + Copy button + Toast
        # -------------------------------------------------
        address = site.get("address", "N/A")

        col1, col2 = st.columns([6, 1])

        with col1:
            st.write(f"**Address:** {address}")

        with col2:
            if st.button("📋 Copy"):
                pyperclip.copy(address)
                st.toast("📍 Address copied!", icon="✅")

        # -------------------------------------------------
        # Provider
        # -------------------------------------------------
        st.write(f"**Provider:** {site['provider']}")

        # -------------------------------------------------
        # Provider link
        # -------------------------------------------------
        st.link_button(
            "🔗 Open Provider Outage Page",
            site["url"]
        )

        # -------------------------------------------------
        # Auto-check power status
        # -------------------------------------------------
        if st.button("🔍 Auto-Check Power Status"):
            with st.spinner("Checking live outage map..."):
                result = check_power_status(
                    site["url"],
                    site["address"],
                    site.get("search"),
                    site.get("provider", "")
                )

            if not result["found"]:
                st.warning(
                    "⚠️ Could not auto-detect location. "
                    "Please verify manually on the outage map."
                )
            else:
                if result["status"] == "OUTAGE":
                    st.error(f"⚡ POWER OUTAGE ({result['type']})")

                elif result["status"] == "OUTAGES":
                    st.error(f"⚡ MULTIPLE POWER OUTAGES ({result['type']})")

                else:
                    st.success("✅ No confirmed outage detected")

    else:
        st.error("❌ Location not found in database")
