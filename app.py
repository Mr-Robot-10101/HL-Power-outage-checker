import json
import streamlit as st

# -------------------------------------------------
# 1. Page Config (පිටුවේ මූලික සැකසුම්)
# -------------------------------------------------
st.set_page_config(
    page_title="Power Check",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# 2. 🎨 CSS Styles (සම්පූර්ණ Design එක)
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* Google Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Background */
    .stApp {
        background: radial-gradient(125% 125% at 50% 10%, #020617 40%, #1e1b4b 100%);
        color: white;
    }

    /* --- SIDEBAR STYLING (1st Image Look) --- */
    
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Sidebar Header Text */
    section[data-testid="stSidebar"] h3 {
        color: #f1f5f9;
        font-size: 1.1rem;
        margin-bottom: 10px;
    }

    /* Sidebar Buttons - Solid Box & Centered Text */
    section[data-testid="stSidebar"] button {
        background-color: rgba(30, 41, 59, 0.8) !important; /* Solid Dark Background */
        color: #cbd5e1 !important;
        
        /* Box Styling */
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        width: 100% !important;
        margin-bottom: 8px !important;
        padding: 15px 5 !important;
        
        /* Text Alignment - Center Everything */
        text-align: center !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        
        /* Font Styling */
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* Ensure text inside button is centered */
    section[data-testid="stSidebar"] button p {
        text-align: center !important;
        width: 100%;
        margin: 0;
    }

    /* Hover Effect */
    section[data-testid="stSidebar"] button:hover {
        background-color: rgba(59, 130, 246, 0.2) !important; /* Blue tint */
        border-color: #3b82f6 !important;
        color: white !important;
        transform: translateY(-1px);
    }

    /* Active/Focus Effect */
    section[data-testid="stSidebar"] button:focus {
        border-color: #60a5fa !important;
        background-color: rgba(37, 99, 235, 0.3) !important;
    }

    /* --- MAIN CONTENT STYLING --- */
    
    /* Input Field */
    .stTextInput input {
        background-color: rgba(255,255,255,0.08) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        padding: 14px 15px !important;
        font-size: 1rem !important;
    }
    .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3) !important;
    }

    /* Result Card */
    .result-header {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
        box-shadow: 0 4px 25px rgba(0,0,0,0.4);
    }

    /* Status Badge */
    .status-badge {
        display: inline-block;
        background-color: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        padding: 6px 18px;
        border-radius: 99px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid rgba(34, 197, 94, 0.3);
        margin-bottom: 15px;
    }

    /* Site Name Typography */
    .site-name {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 5px 0 15px 0;
        background: linear-gradient(to bottom, #fff, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Remove Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
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
    st.error("⚠️ sites.json file not found!")

# Session State
if "selected_loc" not in st.session_state:
    st.session_state.selected_loc = ""

# -------------------------------------------------
# 4. SIDEBAR (Buttons)
# -------------------------------------------------
with st.sidebar:
    st.markdown("### 🗺️ Locations")
    st.markdown("<div style='margin-bottom:15px; color:#64748b; font-size:0.9rem;'>Quick Select</div>", unsafe_allow_html=True)
    
    # Loop to create buttons
    for loc in SITES.keys():
        if st.button(loc.title(), key=f"btn_{loc}"):
            st.session_state.selected_loc = loc
            st.rerun()

# -------------------------------------------------
# 5. MAIN CONTENT
# -------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

# Main Title
st.markdown(
    """
    <div style="text-align:center; margin-bottom: 40px;">
        <h1 style="margin:0; font-size: 3.2rem;">⚡ Power Check</h1>
        <p style="color: #64748b; font-size: 1.1rem; margin-top:8px;">
            Real-time outage status by location
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Search Input (Full Width - No Columns)
search_query = st.text_input(
    "Search Location", 
    value=st.session_state.selected_loc,
    placeholder="Select from sidebar or type...", 
    label_visibility="collapsed"
)

# Results Display
if search_query:
    location_key = search_query.lower().strip()
    
    if location_key in SITES:
        site = SITES[location_key]
        
        st.write("") # Spacer

        # --- Info Card ---
        st.markdown(
            f"""
            <div class="result-header">
                <div class="status-badge">● Active Location</div>
                <div class="site-name">{site['site']}</div>
                <div style="color:#94a3b8; font-size:1rem;">
                    👤 Customer: <span style="color:white; font-weight:600;">{site.get('customer', 'N/A')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # --- Address ---
        st.caption("📍 SITE ADDRESS")
        st.code(site.get("address", "Address unavailable"), language="text")

        # --- Link Button ---
        st.write("") 
        provider_name = site['provider']
        
        st.link_button(
            label=f"Check {provider_name} Status ➜",
            url=site['url'],
            use_container_width=True,
            type="primary" 
        )
    
    else:
        # Error Message
        st.markdown(
            """
            <div style="
                margin-top: 30px;
                padding: 20px;
                background: rgba(239, 68, 68, 0.1);
                border: 1px solid rgba(239, 68, 68, 0.2);
                border-radius: 12px;
                color: #fca5a5;
                text-align: center;
                font-weight: 500;
            ">
                ❌ Location not found. Please try again.
            </div>
            """,
            unsafe_allow_html=True
        )
