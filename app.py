import json
import streamlit as st
import streamlit.components.v1 as components

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Power Outage Checker",
    page_icon="⚡",
    layout="wide",              # Changed to wide → better for full backgrounds
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Vanta.js Animated Background (RINGS) - FIXED VERSION
# -------------------------------------------------
vanta_background = """
<!DOCTYPE html>
<html style="height:100%; width:100%; margin:0; padding:0; overflow:hidden;">
<head>
  <meta charset="UTF-8">
  <style>
    html, body {
      height: 100%;
      width: 100%;
      margin: 0;
      padding: 0;
      background: transparent !important;
      overflow: hidden !important;
    }
    #vanta-bg {
      position: fixed;
      inset: 0;
      width: 100%;
      height: 100%;
      z-index: -9999;
      pointer-events: none;
    }
  </style>
</head>
<body style="background:transparent !important;">

<div id="vanta-bg"></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.rings.min.js"></script>

<script>
  let vantaEffect = null;
  function initVanta() {
    try {
      vantaEffect = VANTA.RINGS({
        el: "#vanta-bg",
        THREE: THREE,  // explicit pass (sometimes helps)
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.00,
        minWidth: 200.00,
        scale: 1.00,
        scaleMobile: 1.00,
        
        // Your screenshot-like colors
        color: 0x88ff00,           // green rings
        backgroundColor: 0x0a0e17, // darker navy/black
        backgroundAlpha: 0.9,
        amplitude: 1.5,
        ringSize: 1.3,
        showDots: true
      });
      console.log("Vanta initialized");
    } catch(e) {
      console.error("Vanta init failed:", e);
    }
  }

  // Run immediately + on resize (Streamlit sometimes needs it)
  initVanta();
  window.addEventListener('resize', () => {
    if (vantaEffect) vantaEffect.resize();
  });

  // Cleanup
  window.addEventListener('beforeunload', () => {
    if (vantaEffect) vantaEffect.destroy();
  });
</script>

</body>
</html>
"""

# Inject with height=0 (no space taken)
components.html(vanta_background, height=0, scrolling=False)

# -------------------------------------------------
# Global CSS - Overlay for readability + remove forced backgrounds
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* Force main app & blocks transparent so Vanta shows through */
    .stApp, .stApp > div:first-child, .block-container {
        background: rgba(10, 14, 23, 0.62) !important;  /* semi-dark overlay - adjust 0.62 → 0.5 if too dark */
        backdrop-filter: blur(4px) !important;
        -webkit-backdrop-filter: blur(4px) !important;
        color: #e5e7eb !important;
    }

    /* Sidebar semi-transparent */
    section[data-testid="stSidebar"] {
        background: rgba(10, 14, 23, 0.78) !important;
        backdrop-filter: blur(6px) !important;
    }

    /* Remove any forced white/gray from iframes or containers */
    iframe {
        background: transparent !important;
    }

    /* Lightning pulse */
    .lightning {
        display: inline-block;
        margin-right: 8px;
        animation: lightningPulse 2.6s ease-in-out infinite;
        text-shadow: 0 0 8px #facc15, 0 0 16px #facc15aa;
    }
    @keyframes lightningPulse {
        0%, 100% { transform: scale(1); opacity: 0.92; }
        50%      { transform: scale(1.14); opacity: 1;   }
    }

    /* Provider buttons */
    .provider-link-btn a {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 12px 24px;
        border-radius: 999px;
        color: white !important;
        text-decoration: none;
        font-weight: 600;
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
        transition: all 0.25s;
    }
    .provider-jemena a    { background: linear-gradient(90deg, #16a34a, #22c55e); }
    .provider-powercor a  { background: linear-gradient(90deg, #2563eb, #1d4ed8); }
    .provider-ausnet a    { background: linear-gradient(90deg, #7c3aed, #9333ea); }
    .provider-default a   { background: linear-gradient(90deg, #3b82f6, #2563eb); }

    .provider-link-btn a:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.5);
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
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ Locations")
    st.caption("Tap to auto-fill")
    for loc in locations_list:
        if st.button(loc.title(), use_container_width=True, key=f"loc_{loc}"):
            st.session_state.selected_location = loc
            st.rerun()

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; margin: 0 0 24px 0;">
        <h1><span class="lightning">⚡</span> Power Outage Checker</h1>
        <p style="opacity:0.9; font-size:1.1rem;">
            Check power status using live provider outage maps
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Input
# -------------------------------------------------
location = st.text_input("📍 Enter Location / Suburb", value=st.session_state.selected_location)

# -------------------------------------------------
# Main content
# -------------------------------------------------
if location and location.lower() in SITES:
    site = SITES[location.lower()]
    address = site.get("address", "N/A")

    st.success(f"📍 **{site['site']}**  \n👤 **Customer:** {site.get('customer', 'N/A')}")

    # Address copy
    components.html(
        f"""
        <div style="display:flex; align-items:center; gap:12px; margin:16px 0;">
            <span style="font-weight:600; font-size:16px; color:#e5e7eb;">
                Address: {address}
            </span>
            <button style="padding:8px 16px; border-radius:10px; border:none; background:#2563eb; color:white; cursor:pointer; font-weight:600;"
                    onclick="navigator.clipboard.writeText('{address}'); this.innerText='✓ Copied'; this.style.background='#16a34a'; setTimeout(()=>{{this.innerText='📋 Copy';this.style.background='#2563eb';}},1800);">
                📋 Copy
            </button>
        </div>
        """,
        height=60
    )

    st.markdown(f"**Provider:** {site['provider']}")

    provider_name = site["provider"].lower()
    provider_class = (
        "provider-jemena" if "jemena" in provider_name else
        "provider-powercor" if "powercor" in provider_name else
        "provider-ausnet" if "ausnet" in provider_name else
        "provider-default"
    )

    st.markdown(
        f"""
        <div class="provider-link-btn {provider_class}" style="text-align:center; margin:28px 0;">
            <a href="{site['url']}" target="_blank">🔗 Open Provider Outage Page</a>
        </div>
        """,
        unsafe_allow_html=True
    )

elif location:
    st.error("❌ Location not found")
