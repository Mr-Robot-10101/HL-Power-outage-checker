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
# 🌌 VANTA.RINGS BACKGROUND (FIXED FOR STREAMLIT CLOUD)
# -------------------------------------------------
components.html(
    """
    <div id="vanta-bg"></div>

    <style>
        /* VANTA background layer */
        #vanta-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -2;
            pointer-events: none;
        }

        /* Make Streamlit transparent so VANTA is visible */
        .stApp {
            background: transparent;
            color: #e5e7eb;
        }

        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: rgba(2, 6, 23, 0.95);
        }

        section[data-testid="stSidebar"] button {
            background-color: #2563eb;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 10px;
            font-weight: 500;
            transition: all 0.2s ease;
        }

        section[data-testid="stSidebar"] button:hover {
            background-color: #1d4ed8;
            transform: translateY(-1px);
        }

        /* Lightning pulse near title */
        .lightning {
            display: inline-block;
            margin-right: 6px;
            animation: lightningPulse 2.6s ease-in-out infinite;
            text-shadow:
                0 0 6px rgba(250,204,21,0.6),
                0 0 14px rgba(250,204,21,0.35);
        }

        @keyframes lightningPulse {
            0% { transform: scale(1); opacity: 0.9; }
            50% { transform: scale(1.18); opacity: 1; }
            100% { transform: scale(1); opacity: 0.9; }
        }

        /* Provider buttons */
        .provider-btn a {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 22px;
            border-radius: 999px;
            font-weight: 600;
            text-decoration: none;
            color: white !important;
            box-shadow: 0 8px 24px rgba(0,0,0,0.35);
            transition: all 0.25s ease;
        }

        .jemena a { background: linear-gradient(90deg,#16a34a,#22c55e); }
        .powercor a { background: linear-gradient(90deg,#2563eb,#1d4ed8); }
        .ausnet a { background: linear-gradient(90deg,#7c3aed,#9333ea); }
        .default a { background: linear-gradient(90deg,#1f6feb,#2563eb); }

        .provider-btn a:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(0,0,0,0.45);
        }
    </style>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.rings.min.js"></script>

    <script>
        if (!window._vantaEffect) {
            window._vantaEffect = VANTA.RINGS({
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
        }
    </script>
    """,
    height=300  # ⚠️ MUST NOT BE 0
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
# Main content
# -------------------------------------------------
if location and location.lower() in SITES:
    site = SITES[location.lower()]
    address = site.get("address", "N/A")

    st.success(
        f"📍 **{site['site']}**\n\n"
        f"👤 **Customer:** {site.get('customer', 'N/A')}"
    )

    # Address + copy (NO rerun)
    components.html(
        f"""
        <div style="display:flex; gap:12px; align-items:center; margin:10px 0;">
            <div style="font-weight:600; color:white;">
                Address: {address}
            </div>
            <button
                style="padding:6px 12px;border-radius:8px;border:none;
                       background:#2563eb;color:white;font-weight:600;cursor:pointer;"
                onclick="navigator.clipboard.writeText('{address}');
                         this.innerText='✓ Copied';
                         this.style.background='#16a34a';">
                📋 Copy
            </button>
        </div>
        """,
        height=60
    )

    st.write(f"**Provider:** {site['provider']}")

    p = site["provider"].lower()
    cls = (
        "jemena" if "jemena" in p
        else "powercor" if "powercor" in p
        else "ausnet" if "ausnet" in p
        else "default"
    )

    st.markdown(
        f"""
        <div class="provider-btn {cls}">
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
