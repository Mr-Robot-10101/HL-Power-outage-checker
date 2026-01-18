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
# 2. 🎨 CSS Styles & BACKGROUND ANIMATION
# -------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        height: 100%;
        margin: 0;
        background-color: #020617;
        overflow: hidden;
    }

    /* --- BACKGROUND ANIMATION (CSS ONLY - Reliable) --- */
    .stApp {
        /* ගැඹුරු නිල්/දම් පැහැති Gradient එකක් */
        background: linear-gradient(135deg, #020617 0%, #0f172a 50%, #1e1b4b 100%);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite; /* සෙමින් චලනය වන Animation එක */
        position: relative;
        z-index: 0;
    }

    /* Gradient චලනය */
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* සියුම් තිත් රටාවක් (Dot Pattern) එකතු කිරීම */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(rgba(37, 99, 235, 0.1) 1px, transparent 1px),
            radial-gradient(rgba(37, 99, 235, 0.05) 1px, transparent 1px);
        background-size: 30px 30px, 15px 15px;
        background-position: 0 0, 15px 15px;
        z-index: -1;
        opacity: 0.6;
    }

    /* --- SIDEBAR STYLING (Solid & Centered) --- */
    section[data-testid="stSidebar"] {
        background-color: rgba(11, 15, 25, 0.9);
        border-right: 1px solid rgba(255,255,255,0.05);
        backdrop-filter: blur(8px);
    }

    section[data-testid="stSidebar"] h3 {
        color: #f1f5f9;
        font-size: 1.1rem;
        margin-bottom: 15px;
        padding-left: 5px;
    }

    /* Buttons Styling */
    section[data-testid="stSidebar"] button {
        background-color: rgba(30, 41, 59, 0.95) !important; /* Solid Box */
        color: #cbd5e1 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        margin-bottom: 8px !important;
        height: auto !important;
        padding: 12px 0 !important;
        
        /* Center Text */
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
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    /* --- MAIN CARD STYLING --- */
    .result-header {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        backdrop-filter: blur(20px);
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        animation: fadeIn 0.5s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
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
        text-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }

    /* Welcome Box */
    .welcome-box {
        margin-top: 40px;
        padding: 50px;
        background: rgba(15, 23, 42, 0.7);
        border: 1px dashed rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        text-align: center;
        color: #cbd5e1;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# 3. Load Data
# -------------------------------------------------
try:
    with open("sites.json", "r", encoding="utf-8") as f:
        SITES = json.load(f)
except FileNotFoundError:
    SITES = {}

locations_list = list(SITES.keys())

# Session State
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
    <div style="text-align:center; margin-bottom: 30px; position: relative; z-index: 1;">
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
