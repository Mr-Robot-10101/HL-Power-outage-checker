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
# Vanta.js Animated Background (RINGS - full screen)
# -------------------------------------------------
vanta_background = """
<div id="vanta-bg"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.rings.min.js"></script>

<script>
  let vantaEffect;
  try {
    vantaEffect = VANTA.RINGS({
      el: "#vanta-bg",
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200.00,
      minWidth: 200.00,
      scale: 1.00,
      scaleMobile: 1.00,
      
      // Colors matching your screenshot / electric theme
      color: 0x88ff00,              // bright green rings
      backgroundColor: 0x202428,    // very dark navy/black
      backgroundAlpha: 0.92,        // almost opaque but still lets some overlay work
      amplitude: 1.4,
      ringSize: 1.15,
      showDots: true
    });
  } catch(e) {
    console.error("Vanta failed to initialize:", e);
  }

  // Clean up on page change / reload to prevent memory issues
  window.addEventListener('beforeunload', () => {
    if (vantaEffect) vantaEffect.destroy();
  });
</script>

<style>
  #vanta-bg {
    position: fixed !important;
    inset: 0 !important;
    width: 100% !important;
    height: 100% !important;
    z-index: -999 !important;
    pointer-events: none !important;
  }

  /* Semi-transparent overlay so text/buttons remain readable */
  .stApp > div:first-child > div,
  .block-container {
    background: rgba(2, 6, 23, 0.68) !important;
    backdrop-filter: blur(5px) !important;
    -webkit-backdrop-filter: blur(5px) !important;
    border-radius: 16px !important;
    padding: 1.8rem !important;
    margin: 1rem auto !important;
    max-width: 1100px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
  }

  /* Make sidebar semi-transparent too */
  section[data-testid="stSidebar"] {
    background: rgba(2, 6, 23, 0.82) !important;
    backdrop-filter: blur(8px) !important;
  }

  /* Fix header & other elements visibility */
  .st-emotion-cache-1y4p8pa {
    background: transparent !important;
  }
</style>
"""

# Inject Vanta once (height=0 hides the empty component frame)
st.components.v1.html(vanta_background, height=0)

# -------------------------------------------------
# Existing GLOBAL CSS (Animated gradient + Lightning pulse + buttons)
# -------------------------------------------------
st.markdown(
    """
    <style>
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
        50% { transform: scale(1.15); opacity: 1;
              text-shadow: 0 0 10px rgba(250,204,21,0.9), 0 0 24px rgba(250,204,21,0.55); }
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
    .provider-jemena a    { background: linear-gradient(90deg, #16a34a, #22c55e); }
    .provider-powercor a  { background: linear-gradient(90deg, #2563eb, #1d4ed8); }
    .provider-ausnet a    { background: linear-gradient(90deg, #7c3aed, #9333ea); }
    .provider-default a   { background: linear-gradient(90deg, #1f6feb, #2563eb); }

    .provider-link-btn a:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 26px rgba(0,0,0,0.45);
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
# Header with lightning pulse
# -------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; margin-bottom:20px;">
        <h1>
            <span class="lightning">⚡</span> Power Outage Checker
        </h1>
        <p style="opacity:0.85;">
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

    # Address + copy button
    components.html(
        f"""
        <div style="display:flex; align-items:center; gap:12px; margin:16px 0;">
            <div style="font-weight:600; color:#e5e7eb; font-size:16px;">
                Address: {address}
            </div>
            <button
                style="
                    padding:8px 16px;
                    border-radius:10px;
                    border:none;
                    background:#2563eb;
                    color:white;
                    cursor:pointer;
                    font-weight:600;
                    transition: all 0.2s;
                "
                onmouseover="this.style.background='#1d4ed8'"
                onmouseout="this.style.background='#2563eb'"
                onclick="
                    navigator.clipboard.writeText('{address}');
                    this.innerText='✓ Copied!';
                    this.style.background='#16a34a';
                    setTimeout(() => {{
                        this.innerText='📋 Copy';
                        this.style.background='#2563eb';
                    }}, 2000);
                "
            >
                📋 Copy
            </button>
        </div>
        """,
        height=70,
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
        <div class="provider-link-btn {provider_class}" style="text-align:center; margin:24px 0;">
            <a href="{site['url']}" target="_blank">
                🔗 Open Provider Outage Page
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

elif location:
    st.error("❌ Location not found in database")
