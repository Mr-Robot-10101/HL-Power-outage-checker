
import json
import streamlit as st
from selenium_checker import check_power_status

st.set_page_config(page_title="Power Outage Checker", page_icon="⚡")

with open("sites.json", "r", encoding="utf-8") as f:
    SITES = json.load(f)

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

location = st.text_input("📍 Enter Location / Suburb")

if location:
    key = location.lower().strip()

    if key in SITES:
        site = SITES[key]

        st.success(
            f"📍 **{site['site']}**\n\n👤 **Customer:** {site.get('customer', 'N/A')}"
        )

        st.write(f"**Address:** {site.get('address', 'N/A')}")
        st.write(f"**Provider:** {site['provider']}")

        st.link_button("🔗 Open Provider Outage Page", site["url"])

        if st.button("🔍 Auto-Check Power Status"):
            with st.spinner("Checking live outage map..."):
                result = check_power_status(
                    site["url"],
                    site["address"],  # ✅ CORRECT
                    site["search"],
                    site.get("provider", "")
                )

            if not result["found"]:
                st.warning("⚠️ Could not auto-detect location. Please verify manually on map.")
            else:
                if result["status"] == "OUTAGE":
                    st.error(f"⚡ POWER OUTAGE ({result['type']})")

                elif result["status"] == "OUTAGES":
                    st.error(f"⚡ MULTIPLE POWER OUTAGES ({result['type']})")

                else:
                    st.success("✅ No confirmed outage detected")


    else:
        st.error("❌ Location not found in database")
