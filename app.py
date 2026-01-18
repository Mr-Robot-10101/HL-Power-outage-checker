import json
import streamlit as st

# -------------------------------------------------
# 1. Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Power Check",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# 2. 🎨 CSS Styles (Background + Sidebar + Electric Card)
# -------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');
    
    /* General Settings */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Transparent App for Background Layer */
    .stApp {
        background: transparent !important;
    }

    /* --- FIXED BACKGROUND ANIMATION (CSS) --- */
    #bg-animation {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        background: linear-gradient(135deg, #020617 0%, #0f172a 50%, #1e1b4b 100%);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* --- SIDEBAR STYLING --- */
    section[data-testid="stSidebar"] {
        background-color: rgba(11, 15, 25, 0.9);
        border-right: 1px solid rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #f1f5f9;
        font-size: 1.1rem;
        margin-bottom: 10px;
    }

    section[data-testid="stSidebar"] button {
        background-color: rgba(30, 41, 59, 0.95) !important;
        color: #cbd5e1 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        margin-bottom: 8px !important;
        padding: 12px 0 !important;
        width: 100%;
        text-align: center !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        font-weight: 500 !important;
        transition: all 0.2s ease-in-out !important;
    }

    section[data-testid="stSidebar"] button p {
        text-align: center !important;
        width: 100%;
        margin: 0;
    }
    
    section[data-testid="stSidebar"] button:hover {
        background-color: rgba(59, 130, 246, 0.3) !important;
        border-color: #3b82f6 !important;
        color: white !important;
        transform: translateY(-2px);
    }

    /* -------------------------------------------------------
       ⚡ ELECTRIC BORDER CARD STYLES (Converted for Streamlit)
       ------------------------------------------------------- */
    
    :root {
      --electric-border-color: #dd8448;
      --electric-light-color: #fbd38d; 
      --color-neutral-900: #1a202c;
    }

    /* Card Container */
    .electric-card-container {
        position: relative;
        width: 100%;
        max-width: 500px; /* Card Width Limit */
        margin: 20px auto;
        padding: 2px;
        border-radius: 24px;
        background: linear-gradient(-30deg, rgba(221, 132, 72, 0.4), transparent, rgba(221, 132, 72, 0.4)),
                    linear-gradient(to bottom, rgba(26, 32, 44, 0.8), rgba(26, 32, 44, 0.8));
    }

    .inner-container {
        position: relative;
        height: 100%;
        border-radius: 24px;
        /* Ensure content is clickable */
        z-index: 1; 
    }

    /* Border Animation Layers */
    .border-outer {
        border: 2px solid rgba(221, 132, 72, 0.5);
        border-radius: 24px;
        padding-right: 4px;
        padding-bottom: 4px;
        position: absolute;
        inset: 0;
        pointer-events: none;
    }

    .main-card {
        width: 100%;
        height: 100%;
        border-radius: 24px;
        border: 2px solid var(--electric-border-color);
        margin-top: -4px;
        margin-left: -4px;
        filter: url(#turbulent-displace); /* SVG Filter */
        pointer-events: none;
    }

    /* Glows */
    .glow-layer-1 {
        border: 2px solid rgba(221, 132, 72, 0.6);
        border-radius: 24px;
        position: absolute; inset: 0;
        filter: blur(1px); pointer-events: none;
    }

    .glow-layer-2 {
        border: 2px solid var(--electric-light-color);
        border-radius: 24px;
        position: absolute; inset: 0;
        filter: blur(4px); pointer-events: none;
    }

    .background-glow {
        position: absolute; inset: 0;
        border-radius: 24px;
        filter: blur(32px);
        transform: scale(1.1);
        opacity: 0.3;
        z-index: -1;
        background: linear-gradient(-30deg, var(--electric-light-color), transparent, var(--electric-border-color));
        pointer-events: none;
    }

    /* Overlays */
    .overlay-1, .overlay-2 {
        position: absolute; inset: 0;
        border-radius: 24px;
        mix-blend-mode: overlay;
        transform: scale(1.05);
        filter: blur(16px);
        background: linear-gradient(-30deg, white, transparent 30%, transparent 70%, white);
        pointer-events: none;
    }
    .overlay-1 { opacity: 0.8; }
    .overlay-2 { opacity: 0.5; }

    /* Content Layout */
    .content-container {
        position: relative; /* Changed to relative for flow */
        padding: 40px;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        z-index: 10;
        min-height: 350px;
    }

    /* Badge (Scrollbar glass) */
    .scrollbar-glass {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 14px;
        padding: 6px 16px;
        text-transform: uppercase;
        font-weight: bold;
        font-size: 12px;
        color: #4ade80;
        margin-bottom: 20px;
        display: inline-block;
    }

    /* Typography */
    .card-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(to bottom, #fff, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .customer-info {
        color: #94a3b8;
        font-size: 1rem;
        margin-top: 10px;
    }
    
    .address-text {
        font-family: monospace;
        color: #cbd5e1;
        background: rgba(0,0,0,0.3);
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 0.85rem;
        margin-top: 15px;
        display: inline-block;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .divider {
        border: none;
        height: 1px;
        background: rgba(255,255,255,0.15);
        margin: 25px 0;
        width: 100%;
    }

    /* Button */
    .custom-link-btn {
        display: inline-block;
        background: linear-gradient(135deg, #dd8448 0%, #b45309 100%);
        color: white !important;
        padding: 12px 28px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 600;
        transition: transform 0.2s;
        box-shadow: 0 4px 15px rgba(221, 132, 72, 0.4);
    }
    .custom-link-btn:hover {
        transform: translateY(-2px);
        filter: brightness(1.1);
    }

    /* Welcome Box */
    .welcome-box {
        margin-top: 50px;
        padding: 40px;
        background: rgba(15, 23, 42, 0.6);
        border: 1px dashed rgba(255,255,255,0.2);
        border-radius: 16px;
        text-align: center;
        color: #cbd5e1;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    
    <div id="bg-animation"></div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# 3. Load Data & State
# -------------------------------------------------
try:
    with open("sites.json", "r", encoding="utf-8") as f:
        SITES = json.load(f)
except FileNotFoundError:
    SITES = {}

locations_list = list(SITES.keys())

if "selected_location" not in st.session_state:
    st.session_state.selected_location = None

# -------------------------------------------------
# 4. Sidebar Logic
# -------------------------------------------------
with st.sidebar:
    st.markdown("### 🗺️ Locations")
    st.caption("Quick Select")
    
    for loc in locations_list:
        if st.button(loc.title(), use_container_width=True, key=f"loc_{loc}"):
            st.session_state.selected_location = loc
            st.rerun()

# -------------------------------------------------
# 5. Main Content Area
# -------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

# Main Title
st.markdown(
    """
    <div style="text-align:center; margin-bottom: 40px;">
        <h1 style="margin:0; font-size: 3.5rem; text-shadow: 0 4px 15px rgba(0,0,0,0.8);">
            ⚡ Power Check
        </h1>
        <p style="color: #cbd5e1; font-size: 1.1rem; margin-top:8px; text-shadow: 0 2px 5px rgba(0,0,0,0.8);">
            Real-time outage status by location
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- Display Logic ---
if st.session_state.selected_location:
    location_key = st.session_state.selected_location.lower().strip()
    
    if location_key in SITES:
        site = SITES[location_key]
        
        # --- HTML FOR ELECTRIC BORDER CARD ---
        electric_card_html = f"""
        <svg style="position: absolute; width: 0; height: 0; overflow: hidden;">
          <defs>
            <filter id="turbulent-displace" x="-20%" y="-20%" width="140%" height="140%">
              <feTurbulence type="turbulence" baseFrequency="0.02" numOctaves="10" result="noise1" seed="1" />
              <feOffset in="noise1" dx="0" dy="0" result="offsetNoise1">
                <animate attributeName="dy" values="700; 0" dur="6s" repeatCount="indefinite" calcMode="linear" />
              </feOffset>
              <feTurbulence type="turbulence" baseFrequency="0.02" numOctaves="10" result="noise2" seed="1" />
              <feOffset in="noise2" dx="0" dy="0" result="offsetNoise2">
                <animate attributeName="dy" values="0; -700" dur="6s" repeatCount="indefinite" calcMode="linear" />
              </feOffset>
              <feComposite in="offsetNoise1" in2="offsetNoise2" result="part1" />
              <feDisplacementMap in="SourceGraphic" in2="part1" scale="30" xChannelSelector="R" yChannelSelector="B" />
            </filter>
          </defs>
        </svg>

        <div class="electric-card-container">
          <div class="inner-container">
            
            <div class="border-outer">
              <div class="main-card"></div>
            </div>
            <div class="glow-layer-1"></div>
            <div class="glow-layer-2"></div>
            <div class="background-glow"></div>
            <div class="overlay-1"></div>
            <div class="overlay-2"></div>

            <div class="content-container">
                <div class="scrollbar-glass">
                  ● Active Location
                </div>
                
                <p class="card-title">{site['site']}</p>
                
                <p class="customer-info">
                   👤 Customer: <span style="color:white; font-weight:600;">{site.get('customer', 'N/A')}</span>
                </p>
                
                <div class="address-text">
                    📍 {site.get('address', 'N/A')}
                </div>

                <hr class="divider" />

                <div style="width:100%;">
                    <p style="color:#cbd5e1; margin-bottom:15px; font-size:0.9rem;">
                        Provider: <strong>{site['provider']}</strong>
                    </p>
                    <a href="{site['url']}" target="_blank" class="custom-link-btn">
                        Check Status ➜
                    </a>
                </div>
            </div>
            
          </div>
        </div>
        """
        
        st.markdown(electric_card_html, unsafe_allow_html=True)
        
    else:
        st.error("Error: Location data not found.")
else:
    # Welcome Message
    st.markdown(
        """
        <div class="welcome-box">
            <h3>👈 Select a location</h3>
            <p>Click on any location in the sidebar to view details.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
