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
# 🌈 VANTA.RINGS BACKGROUND (OFFICIAL DEMO STYLE)
# -------------------------------------------------
components.html(
    """
<div id="vanta-bg"></div>

<style>
    /* VANTA background */
    #vanta-bg {
        position: fixed;
        inset: 0;
        width: 100vw;
        height: 100vh;
        z-index: -5;
        pointer-events: none;
    }

    /* Transparent Streamlit app */
    .stApp {
        background: transparent;
        color: #e5e7eb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.92);
    }

    section[data-testid="stSidebar"] button {
        background-color: rgba(255,255,255,0.08);
        color: white;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 10px;
        padding: 10px;
        font-weight: 500;
    }

    section[data-testid="stSidebar"] button:hover {
        background-color: rgba(255,255,255,0.16);
        transform: translateY(-1px);
    }

    /* Lightning pulse */
    .lightning {
        display: inline-block;
        margin-right: 6px;
        animation: pulse 2.6s ease-in-out infinite;
        text-shadow: 0 0 12px rgba(255,255,255,0.8);
    }

    @keyframes pulse {
        0%,100% { transform: scale(1); opacity: .9; }
        50% { transform: scale(1.18); opacity: 1; }
    }

    /* Provider button */
    .provider-btn a {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 12px 22px;
        border-radius: 999px;
        font-weight: 600;
        text-decoration: none;
        color: white !important;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.18);
        backdrop-filter: blur(8px);
    }

    .provider-btn a:hover {
        background: rgba(255,255,255,0.22);
        transform: translateY(-2px);
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
        minHeight: 200.0,
        minWidth: 200.0,
        scale: 1.0,
        scaleMobile: 1.0,
        backgroundColor: 0x202428,
        backgroundAlpha: 1.0
    });
}
</script>
""",
    height=400  # MUST be > 0
)

# -------------------------------------------------
# Load sites
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
<div style="text-align:center; margin-bottom:20px;">
    <h1><span class="lightning">⚡</span> Power Outage Checker</h1>
    <p style="opacity:0.8;">
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
# Main content
# -------------------------------------------------
if location and location.lower() in SITES:
    site = SITES[location.lower()]
    address = site.get("address", "N/A")

    st.success(
        f"📍 **{site['site']}**\n\n"
        f"👤 **Customer:** {site.get('customer','N/A')}"
    )

    components.html(
        f"""
<div style="display:flex; gap:12px; align-items:center; margin:10px 0;">
    <div style="font-weight:600; color:white;">
        Address: {address}
    </div>
    <button
        style="padding:6px 12px;border-radius:8px;border:none;
               background:rgba(255,255,255,0.15);
               color:white;font-weight:600;cursor:pointer;"
        onclick="navigator.clipboard.writeText('{address}');
                 this.innerText='✓ Copied';
                 this.style.background='rgba(34,197,94,0.9)';">
        📋 Copy
    </button>
</div>
""",
        height=60
    )

    st.write(f"**Provider:** {site['provider']}")

    st.markdown(
        f"""
<div class="provider-btn">
    <a href="{site['url']}" target="_blank">
        🔗 Open Provider Outage Page
    </a>
</div>
""",
        unsafe_allow_html=True
    )

elif location:
    st.error("❌ Location not found")
else:
    st.info("👈 Select a location from the sidebar")
