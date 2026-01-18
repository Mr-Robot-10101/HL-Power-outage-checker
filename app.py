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
# 2. 🎨 CSS Styles (Electric Border Added)
# -------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Transparent Background for Animation */
    .stApp {
        background: transparent !important;
    }

    /* --- BACKGROUND ANIMATION (Keep Flowing Energy) --- */
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
        background-color: #0b0f19;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #f1f5f9;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 10px;
    }

    /* Sidebar Buttons - Solid Box & Centered Text */
    section[data-testid="stSidebar"] button {
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
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
        box-shadow: 0 1px 2px rgba(0,0,0,0.2);
    }

    section[data-testid="stSidebar"] button p {
        text-align: center !important;
        width: 100%;
        margin: 0;
    }

    section[data-testid="stSidebar"] button:hover {
        background-color: #3b82f6 !important;
        border-color: #3b82f6 !important;
        color: white !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }

    section[data-testid="stSidebar"] button:focus {
        background-color: #2563eb !important;
        border-color: #60a5fa !important;
        color: white !important;
    }

    /* --- ELECTRIC CARD STYLING --- */
    .result-header {
        /* Darker glass background for contrast */
        background: rgba(10, 15, 30, 0.85); 
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        backdrop-filter: blur(20px);
        margin-bottom: 20px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        animation: fadeIn 0.5s ease-out;

        /* ✨ THE ELECTRIC BORDER EFFECT ✨ */
        /* Base orange border */
        border: 2px solid rgba(255, 165, 0, 0.6); 
        /* Multi-layered glowing shadows */
        box-shadow: 
            0 0 10px rgba(255, 165, 0, 0.8),  /* Inner bright glow */
            0 0 20px rgba(255, 140, 0, 0.6),  /* Middle orange glow */
            0 0 40px rgba(255, 100, 0, 0.4),  /* Outer softer glow */
            inset 0 0 15px rgba(255, 165, 0, 0.3); /* Inner glow on the card itself */
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .status-badge {
        display: inline-block;
        background-color: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        padding: 6px 16px;
        border-radius: 99px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid rgba(34, 197, 94, 0.3);
        margin-bottom: 15px;
    }

    .site-name {
        font-size: 2.8rem;
        font-weight: 800;
        margin: 10px 0 20px 0;
        background: linear-gradient(to bottom, #fff, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        /* Optional: Add a subtle text glow to match */
        text-shadow: 0 0 10px rgba(255, 165, 0, 0.3);
    }
    
    .customer-row {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }

    /* Address Box */
    .address-box {
        background: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 165, 0, 0.2); /* Subtle orange border for address too */
        padding: 15px;
        border-radius: 12px;
        font-family: monospace;
        color: #cbd5e1;
        font-size: 0.95rem;
        margin-top: 20px;
        margin-bottom: 30px;
    }

    .welcome-box {
        margin-top: 60px;
        padding: 50px;
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
        
        # --- CLEAN CARD DESIGN WITH ELECTRIC BORDER ---
        
        st.markdown(
            f"""
            <div class="result-header">
                <div class="status-badge">● Active Location</div>
                <div class="site-name">{site['site']}</div>
                
                <div class="customer-row">
                    👤 Customer: <span style="color:white; font-weight:600;">{site.get('customer', 'N/A')}</span>
                </div>
                
                <div class="address-box">
                    📍 {site.get('address', 'N/A')}
                </div>

                <div style="margin-top:20px;"></div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Provider Button
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
