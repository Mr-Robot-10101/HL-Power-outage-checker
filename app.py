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
# 2. 🎨 CSS Styles (MORE VISIBLE FLOATING CLOUDS)
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

    /* --- SKY BACKGROUND CONTAINER --- */
    #bg-animation {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        /* Night Sky Gradient - Slightly brighter near horizon for contrast */
        background: linear-gradient(to bottom, #020617 0%, #0f172a 50%, #1e293b 100%);
        overflow: hidden;
    }

    /* --- MODIFIED CLOUD ANIMATION CSS (More Visible) --- */
    
    /* Cloud Shape Base - Increased Visibility */
    .cloud {
        position: absolute;
        /* Increased white opacity (from 0.08 to 0.15) */
        background: rgba(255, 255, 255, 0.15); 
        border-radius: 100px;
        /* Reduced blur slightly (from 30px to 20px) for better definition */
        filter: blur(20px); 
        z-index: 0;
        /* Increased overall opacity */
        opacity: 0.9;
    }

    /* Cloud Layer 1 (Top, Slow, Long) */
    .c1 {
        width: 600px; height: 140px;
        top: 5%;
        left: -600px;
        animation: drift 50s linear infinite;
    }

    /* Cloud Layer 2 (Middle, Big chunk) */
    .c2 {
        width: 800px; height: 200px;
        top: 35%;
        left: -800px;
        animation: drift 40s linear infinite;
        animation-delay: -10s;
        /* A bit brighter than base */
        background: rgba(255, 255, 255, 0.18);
    }

    /* Cloud Layer 3 (Bottom, Fast, Brighter puff) */
    .c3 {
        width: 450px; height: 120px;
        top: 65%;
        left: -450px;
        animation: drift 28s linear infinite;
        animation-delay: -5s;
        /* Brightest cloud chunk */
        background: rgba(255, 255, 255, 0.22);
        filter: blur(15px); /* Less blurred */
    }
    
    /* Cloud Layer 4 (Background Detail) */
    .c4 {
        width: 350px; height: 90px;
        top: 25%;
        left: -350px;
        animation: drift 55s linear infinite;
        animation-delay: -25s;
        filter: blur(25px); /* More blurred for depth */
        opacity: 0.7;
    }

    @keyframes drift {
        0% { transform: translateX(0); }
        100% { transform: translateX(130vw); }
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
        margin-bottom: 15px;
        padding-left: 5px;
    }

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
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        backdrop-filter: blur(15px);
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
        <div class="cloud c1"></div>
        <div class="cloud c2"></div>
        <div class="cloud c3"></div>
        <div class="cloud c4"></div>
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
