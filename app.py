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
# 2. 🎨 CSS Styles & NEW ANIMATION
# -------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Make Streamlit Transparent */
    .stApp {
        background: transparent !important;
    }

    /* --- NEW BACKGROUND ANIMATION (Floating Orbs) --- */
    #bg-animation {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        background-color: #0b0f19; /* Deep Dark Background */
        overflow: hidden;
    }

    /* Glowing Orbs */
    .orb {
        position: absolute;
        border-radius: 50%;
        filter: blur(80px); /* This creates the glow effect */
        opacity: 0.6;
        animation: float ease-in-out infinite;
    }

    /* Orb 1 (Purple/Blue) */
    .orb-1 {
        width: 500px;
        height: 500px;
        background: linear-gradient(180deg, #4c1d95 0%, #2563eb 100%);
        top: -100px;
        left: -100px;
        animation-duration: 10s;
    }

    /* Orb 2 (Cyan/Green) */
    .orb-2 {
        width: 400px;
        height: 400px;
        background: linear-gradient(180deg, #0ea5e9 0%, #22c55e 100%);
        bottom: -50px;
        right: -50px;
        animation-duration: 12s;
        animation-delay: -2s;
    }

    /* Orb 3 (Accent Blue) */
    .orb-3 {
        width: 300px;
        height: 300px;
        background: #3b82f6;
        top: 40%;
        left: 40%;
        opacity: 0.4;
        animation-duration: 15s;
        animation-delay: -5s;
    }

    /* Movement Animation */
    @keyframes float {
        0% { transform: translate(0, 0) scale(1); }
        33% { transform: translate(30px, -50px) scale(1.1); }
        66% { transform: translate(-20px, 20px) scale(0.9); }
        100% { transform: translate(0, 0) scale(1); }
    }

    /* Grid Overlay (Tech Feel) */
    #bg-animation::after {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
    }

    /* --- SIDEBAR STYLING --- */
    section[data-testid="stSidebar"] {
        background-color: rgba(11, 15, 25, 0.85);
        border-right: 1px solid rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
    }

    section[data-testid="stSidebar"] h3 {
        color: #f1f5f9;
        font-size: 1.1rem;
        margin-bottom: 15px;
        padding-left: 5px;
    }

    /* Solid Sidebar Buttons */
    section[data-testid="stSidebar"] button {
        background-color: rgba(30, 41, 59, 0.9) !important;
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
        font-size: 0.95rem !important;
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

    /* --- MAIN CONTENT CARD --- */
    .result-header {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        backdrop-filter: blur(20px);
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    }

    .status-badge {
        display: inline-block;
        background-color: rgba(34, 197, 94, 0.2);
        color: #4ade80;
        padding: 6px 18px;
        border-radius: 99px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid rgba(34, 197, 94, 0.4);
        margin-bottom: 15px;
    }

    .site-name {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 10px 0 20px 0;
        background: linear-gradient(to bottom, #fff, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }

    .welcome-box {
        margin-top: 50px;
        padding: 40px;
        background: rgba(15, 23, 42, 0.6);
        border: 1px dashed rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        text-align: center;
        color: #cbd5e1;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    
    <div id="bg-animation">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
    </div>
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

# Title
st.markdown(
    """
    <div style="text-align:center; margin-bottom: 30px;">
        <h1 style="margin:0; font-size: 3.5rem; text-shadow: 0 4px 15px rgba(0,0,0,0.8);">
            ⚡ Honey Light Power Checker
        </h1>
        <p style="color: #cbd5e1; font-size: 1.1rem; margin-top:8px; text-shadow: 0 2px 5px rgba(0,0,0,0.8);">
            Real-time outage status by location
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Display Logic
if st.session_state.selected_location:
    location_key = st.session_state.selected_location.lower().strip()
    
    if location_key in SITES:
        site = SITES[location_key]
        
        # Info Card
        st.markdown(
            f"""
            <div class="result-header">
                <div class="status-badge">● Active Location</div>
                <div class="site-name">{site['site']}</div>
                <div style="color:#cbd5e1; font-size:1.1rem;">
                    👤 Customer: <span style="color:white; font-weight:600;">{site.get('customer', 'N/A')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Address
        st.caption("📍 SITE ADDRESS")
        st.code(site.get("address", "Address unavailable"), language="text")

        # Link Button
        st.write("") 
        provider_name = site['provider']
        
        st.link_button(
            label=f"Check {provider_name} Status ➜",
            url=site['url'],
            use_container_width=True,
            type="primary" 
        )
    else:
        st.error("Error: Location data not found.")
else:
    # Welcome Box
    st.markdown(
        """
        <div class="welcome-box">
            <h3>👈 Select a location</h3>
            <p>Click on any location in the sidebar to view details.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
