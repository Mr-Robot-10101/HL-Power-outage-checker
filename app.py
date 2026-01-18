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
# 2. 🎨 CSS Styles (MORE REALISTIC WISPY CLOUDS)
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
        /* Deep Night Sky Gradient */
        background: linear-gradient(to bottom, #020617 0%, #0f172a 50%, #1e293b 100%);
        overflow: hidden;
    }

    /* --- REALISTIC WISPY CLOUD CSS --- */
    
    /* Cloud Base Style - Using Gradients for Realism */
    .cloud {
        position: absolute;
        /* වෙනස්කම 1: Solid color වෙනුවට Radial Gradient භාවිතය.
           මැද සුදු පැහැය වැඩි අතර, දාර වලට යද්දී විනිවිද පෙනේ. */
        background: radial-gradient(closest-side at 50% 50%, rgba(255, 255, 255, 0.12), transparent);
        /* හැඩය වඩාත් ස්වභාවික කිරීමට border-radius වෙනස් කිරීම */
        border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        /* තාත්වික බව සඳහා සුදුසු Blur ප්‍රමාණයක් */
        filter: blur(20px);
        opacity: 0.9;
        z-index: 0;
        transform-origin: center;
    }

    /* Cloud Layer 1 (Top, Slow, Very Wispy) */
    .c1 {
        width: 800px; height: 250px;
        top: -5%;
        left: -800px;
        animation: drift 60s linear infinite;
        opacity: 0.7;
        filter: blur(30px); /* ඈතින් ඇති නිසා වැඩිපුර Blur */
    }

    /* Cloud Layer 2 (Middle, Main Body, Brighter) */
    .c2 {
        width: 900px; height: 300px;
        top: 30%;
        left: -900px;
        animation: drift 45s linear infinite;
        animation-delay: -15s;
        /* මැද කොටස මදක් දීප්තිමත් */
        background: radial-gradient(closest-side at 50% 50%, rgba(255, 255, 255, 0.18), transparent);
        filter: blur(25px);
    }

    /* Cloud Layer 3 (Bottom, Fast, Thinner Mist) */
    .c3 {
        width: 600px; height: 180px;
        top: 65%;
        left: -600px;
        animation: drift 35s linear infinite;
        animation-delay: -5s;
        opacity: 0.6;
        filter: blur(15px);
         /* වඩාත් දිගටි හැඩයක් */
        transform: scaleY(0.7);
    }
    
    /* Cloud Layer 4 (Filler fog) */
    .c4 {
        width: 500px; height: 200px;
        top: 20%;
        left: -500px;
        animation: drift 55s linear infinite;
        animation-delay: -30s;
        opacity: 0.5;
        filter: blur(35px);
    }

    @keyframes drift {
        0% { transform: translateX(0) scale(1); }
        50% { transform: translateX(70vw) scale(1.05); } /* මදක් විශාල වීම */
        100% { transform: translateX(140vw) scale(1); }
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
