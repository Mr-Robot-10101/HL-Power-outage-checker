import json
import streamlit as st

# -------------------------------------------------
# 1. Page Config (පිටුවේ මූලික සැකසුම්)
# -------------------------------------------------
st.set_page_config(
    page_title="Power Check",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded" # Sidebar එක දිගහැරලා තියන්න
)

# -------------------------------------------------
# 2. 🎨 Modern CSS Styles
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* Google Font Import - Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Dark Background Gradient */
    .stApp {
        background: radial-gradient(125% 125% at 50% 10%, #020617 40%, #1e1b4b 100%);
        color: white;
    }

    /* --- Sidebar Styling --- */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Sidebar Buttons */
    section[data-testid="stSidebar"] button {
        background-color: transparent;
        color: #94a3b8;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
        margin-bottom: 6px;
        width: 100%;
        text-align: left;
        padding-left: 15px;
        transition: all 0.2s;
    }

    section[data-testid="stSidebar"] button:hover {
        background-color: #2563eb; /* Blue hover */
        color: white;
        border-color: #2563eb;
        transform: translateX(5px);
    }

    /* --- Main Search Box --- */
    .stTextInput input {
        background-color: rgba(255,255,255,0.08) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
    }
    .stTextInput input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3) !important;
    }

    /* --- Result Card Design --- */
    .result-header {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        backdrop-filter: blur(10px);
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        background-color: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid rgba(34, 197, 94, 0.3);
        margin-bottom: 15px;
    }

    .site-name {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(to bottom, #fff, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .customer-label {
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 8px;
    }

    /* Remove footer/menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# 3. Load Data & State Management
# -------------------------------------------------
try:
    with open("sites.json", "r", encoding="utf-8") as f:
        SITES = json.load(f)
except FileNotFoundError:
    SITES = {}
    st.error("⚠️ sites.json file not found!")

# Session State to handle sidebar clicks
if "selected_loc" not in st.session_state:
    st.session_state.selected_loc = ""

# -------------------------------------------------
# 4. Sidebar Section
# -------------------------------------------------
with st.sidebar:
    st.markdown("### 🗺️ Locations")
    st.caption("Select a site to check status")
    
    # Loop through sites to create buttons
    for loc in SITES.keys():
        # If button clicked, update state and rerun app
        if st.button(loc.title(), key=f"btn_{loc}"):
            st.session_state.selected_loc = loc
            st.rerun()

# -------------------------------------------------
# 5. Main Header
# -------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align:center; margin-bottom: 40px;">
        <h1 style="margin:0; font-size: 3rem;">⚡ Power Check</h1>
        <p style="color: #64748b; font-size: 1.1rem; margin-top:5px;">
            Real-time outage status by location
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# -------------------------------------------------
# 6. Search Area
# -------------------------------------------------
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # Check if a location is selected from sidebar
    default_val = st.session_state.selected_loc

    search_query = st.text_input(
        "Search Location", 
        value=default_val,
        placeholder="Type location or select from sidebar...", 
        label_visibility="collapsed"
    )

# -------------------------------------------------
# 7. Result Display Logic
# -------------------------------------------------
if search_query:
    location_key = search_query.lower().strip()
    
    if location_key in SITES:
        site = SITES[location_key]
        
        with col2:
            # --- A. Main Info Card ---
            st.markdown(
                f"""
                <div class="result-header">
                    <div class="status-badge">● Active Location</div>
                    <div class="site-name">{site['site']}</div>
                    <div class="customer-label">
                        👤 Customer: <span style="color:white; font-weight:600;">{site.get('customer', 'N/A')}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # --- B. Address Section (Clean & Native) ---
            st.caption("📍 SITE ADDRESS")
            # Using st.code ensures perfect alignment and a native copy button
            st.code(site.get("address", "Address unavailable"), language="text")

            # --- C. Provider Link Button ---
            st.write("") # Spacer
            provider_name = site['provider']
            
            st.link_button(
                label=f"Check {provider_name} Outage Map ➜",
                url=site['url'],
                use_container_width=True,
                type="primary" 
            )
        
    else:
        # --- Error Message ---
        with col2:
            st.markdown(
                """
                <div style="
                    margin-top: 20px;
                    padding: 20px;
                    background: rgba(239, 68, 68, 0.08);
                    border: 1px solid rgba(239, 68, 68, 0.2);
                    border-radius: 12px;
                    color: #f87171;
                    text-align: center;
                    font-weight: 500;
                ">
                    ❌ Location not found. Please try again.
                </div>
                """,
                unsafe_allow_html=True
            )

# -------------------------------------------------
# 8. Footer
# -------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; margin-top: 80px; opacity: 0.3; font-size: 0.8rem;">
        Power Check System © 2025
    </div>
    """,
    unsafe_allow_html=True
)
