import json
import streamlit as st
import streamlit.components.v1 as components

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
# 🌌 VANTA.RINGS BACKGROUND (Three.js)
# -------------------------------------------------
components.html(
    """
    <div id="vanta-bg"></div>

    <style>
        #vanta-bg {
            position: fixed;
            inset: 0;
            z-index: -1;
        }

        /* Keep content readable */
        .stApp {
            background: transparent;
            color: #e5e7eb;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: rgba(2, 6, 23, 0.95);
        }

        section[data-testid="stSidebar"] button {
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px;
            font-weight: 500;
            transition: all 0.2s ease;
        }

        section[data-testid="stSidebar"] button:hover {
            background-color: #1d4ed8;
            transform: translateY(-1px);
        }

        /* Lightning pulse */
        .lightning {
            display: inline-block;
            margin-right: 6px;
            animation: lightningPulse 2.8s ease-in-out infinite;
            text-shadow:
                0 0 6px rgba(250,204,21,0.6),
                0 0 14px rgba(250,204,21,0.35);
        }

        @keyframes lightningPulse {
            0% { transform: scale(1); opacity: 0.9; }
            50% { transform: scale(1.15); opacity: 1; }
            100% { transform: scale(1); opacity: 0.9; }
        }

        /* Provider buttons */
        .provider-link-btn a {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 22px;
            border-radius: 999px;
            color: #ffffff !important;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            box-shadow: 0 6px 18px rgba(0,0,0,0.35);
            transition: all 0.25s ease;
        }

        .provider-jemena a {
            background: linear-gradient(90deg, #16a34a, #22c55e);
        }

        .provider-powercor a {
            background: linear-gradient(90deg, #2563eb, #1d4ed8);
        }

        .provider-ausnet a {
            background: linear-gradient(90deg, #7c3aed, #9333ea);
        }

        .provider-default a {
            background: linear-gradient(90deg, #1f6feb, #2563eb);
        }

        .provider-link-btn a:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 26px rgba(0,0,0,0.45);
        }
    </style>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.rings.min.js"></script>

    <script>
        VANTA.RINGS({
            el: "#vanta-bg",
            mouseControls: true,
            touchControls: true,
            gyroControls: false,
            minHeight: 200.00,
            minWidth: 200.00,
            scale: 1.0,
            scaleMobile: 1.0,
            backgroundColor: 0x020617,
            color: 0x2563eb
        });
    </script>
    """,
    height=0
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
    <div style="text-align:center; margin-bottom:20px;">
        <h1>
            <span class="lightning">⚡</span> Power Outage Checker
        </h1>
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

    # Address + Copy (no rerun)
    components.html(
        f"""
        <div style="display:flex; align-items:center; gap:12px; margin:10px 0;">
            <div style="font-weight:600; color:#ffffff; font-size:16px;">
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
        height=60
    )

    st.write(f"**Provider:** {site['provider']}")

    provider_name = site["provider"].lower()
    if "jemena" in provider_name:
        provider_class = "provider-jemena"
    elif "powercor" in provider_name:
        provider_class = "provider-powercor"
    elif "ausnet" in provider_name:
        provider_class = "provider-ausnet"
    else:
        provider_class = "provider-default"

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
else:
    st.info("👈 Select a location from the sidebar")
