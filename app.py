import json
import streamlit as st

# -------------------------------------------------
# 1. Page Config (මූලික සැකසුම්)
# -------------------------------------------------
st.set_page_config(
    page_title="Power Check",
    page_icon="⚡",
    layout="centered", # මැදට වෙන්න ලස්සනට පෙන්වීමට
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# 2. 🎨 CSS Styles (සම්පූර්ණ මෝස්තරය)
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* Google Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Background Gradient */
    .stApp {
        background: radial-gradient(125% 125% at 50% 10%, #020617 40%, #1e1b4b 100%);
        color: white;
    }

    /* --- SIDEBAR STYLING --- */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Sidebar Buttons Design */
    section[data-testid="stSidebar"] button {
        background-color: transparent;
        color: #cbd5e1;
        border: 1px solid rgba(255,255,255,0.12); /* සිහින් රාමුව */
        border-radius: 8px;
        margin-bottom: 8px;
        width: 100%; /* Sidebar එක පුරාම විහිදෙන්න */
        padding: 10px 15px;
        text-align: center;
        transition: all 0.2s ease;
        font-weight: 500;
        font-size: 0.95rem;
    }

    /* Sidebar Hover Effect */
    section[data-testid="stSidebar"] button:hover {
        background-color: rgba(59, 130, 246, 0.15);
        color: #60a5fa;
        border-color: #3b82f6;
        transform: translateY(-2px);
    }

    /* --- MAIN CONTENT STYLING --- */
    
    /* Input Field - Full Width & Modern */
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

    /* Result Card Styling */
    .result-header {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 30px; /* ඇතුලත ඉඩ වැඩි කළා */
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

    /* Typography */
    .site-name {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 5px 0 15px 0;
        background: linear-gradient(to bottom, #fff, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Remove Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# 3. Load Data & Session State
# -------------------------------------------------
try:
    with open("sites.json", "r", encoding="utf-8") as f:
        SITES = json.load(f)
except FileNotFoundError:
    SITES = {}

# Session State Initialisation
if "selected_loc" not in st.session_state:
    st.session_state.selected_loc = ""

# -------------------------------------------------
# 4. SIDEBAR LOGIC (Quick Select Buttons)
# -------------------------------------------------
with st.sidebar:
    st.markdown("### 🗺️ Locations")
    st.markdown("<div style='margin-bottom:15px; color:#64748b; font-size:0.9rem;'>Quick Select</div>", unsafe_allow_html=True)
    
    # Create buttons for each site
    for loc in SITES.keys():
        if st.button(loc.title(), key=f"btn_{loc}"):
            st.session_state.selected_loc = loc
            st.rerun()

# -------------------------------------------------
# 5. MAIN CONTENT AREA
# -------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

# Title
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

# --- SEARCH INPUT (Full Width - No Columns) ---
# අපි මෙතන Columns භාවිතා නොකරන නිසා මෙය Screen එකේ මැද හරියටම පිරෙන්න එනවා.
search_query = st.text_input(
    "Search Location", 
    value=st.session_state.selected_loc,
    placeholder="Select from sidebar or type...", 
    label_visibility="collapsed"
)

# --- RESULTS DISPLAY ---
if search_query:
    location_key = search_query.lower().strip()
    
    if location_key in SITES:
        site = SITES[location_key]
        
        # Spacer
        st.write("") 

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

        # --- Address (Native Code Block for easy copy) ---
        st.caption("📍 SITE ADDRESS")
        st.code(site.get("address", "Address unavailable"), language="text")

        # --- Provider Link Button ---
        st.write("") 
        provider_name = site['provider']
        
        # 'use_container_width=True' මගින් Button එක සම්පූර්ණ පළලටම විහිදේ
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
