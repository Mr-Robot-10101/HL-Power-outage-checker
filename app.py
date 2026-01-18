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
# 2. 🎨 Styles (සම්පූර්ණ CSS එක)
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* Google Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Background */
    .stApp {
        background: radial-gradient(125% 125% at 50% 10%, #020617 40%, #1e1b4b 100%);
        color: white;
    }

    /* --- SIDEBAR STYLING START --- */
    
    /* Sidebar Background Color */
    section[data-testid="stSidebar"] {
        background-color: #0b0f19;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Sidebar Text Color */
    section[data-testid="stSidebar"] .stMarkdown {
        color: #94a3b8;
    }

    /* Sidebar Buttons Design (To match your screenshot) */
    section[data-testid="stSidebar"] button {
        background-color: transparent;      /* විනිවිද පෙනෙන */
        color: #cbd5e1;                     /* අකුරු පාට */
        border: 1px solid rgba(255,255,255,0.12); /* වටේට රාමුව */
        border-radius: 8px;
        margin-bottom: 8px;
        width: 100%;
        padding: 12px 15px;
        text-align: center;                 /* මැදට */
        transition: all 0.2s ease;
        font-weight: 500;
        font-size: 0.95rem;
    }

    /* Button Hover Effect */
    section[data-testid="stSidebar"] button:hover {
        background-color: rgba(59, 130, 246, 0.15); /* නිල් පාට පසුබිමක් */
        color: #60a5fa;                             /* අකුරු නිල් පාට */
        border-color: #3b82f6;                      /* රාමුව නිල් පාට */
        transform: translateY(-2px);
    }

    /* --- SIDEBAR STYLING END --- */

    /* Input Field Styling */
    .stTextInput input {
        background-color: rgba(255,255,255,0.08) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
    }
    
    /* Result Card Styling */
    .result-header {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    
    /* Badge Styling */
    .status-badge {
        display: inline-block;
        background-color: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid rgba(34, 197, 94, 0.3);
        margin-bottom: 15px;
    }

    /* Site Name Typography */
    .site-name {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
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
# 3. Load Data & Session State
# -------------------------------------------------
try:
    with open("sites.json", "r", encoding="utf-8") as f:
        SITES = json.load(f)
except FileNotFoundError:
    SITES = {}
    # Error එකක් නොපෙන්වා නිකන්ම හිස්ව තියමු, නැත්නම් UI එක කැත වෙනවා

# Session State Initialisation
if "selected_loc" not in st.session_state:
    st.session_state.selected_loc = ""

# -------------------------------------------------
# 4. SIDEBAR LOGIC
# -------------------------------------------------
with st.sidebar:
    st.markdown("### 🗺️ Locations")
    st.markdown("<div style='margin-bottom:15px; color:#64748b; font-size:0.9rem;'>Quick Select</div>", unsafe_allow_html=True)
    
    # Button List Creation
    for loc in SITES.keys():
        # Button එක Click කළොත් State එක Update කර Rerun කරන්න
        if st.button(loc.title(), key=f"btn_{loc}"):
            st.session_state.selected_loc = loc
            st.rerun()

# -------------------------------------------------
# 5. MAIN CONTENT
# -------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

# Title Area
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

# Layout Columns
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # Search Input (Value එක Session State එකෙන් ගනී)
    search_query = st.text_input(
        "Search Location", 
        value=st.session_state.selected_loc,
        placeholder="Select from sidebar or type...", 
        label_visibility="collapsed"
    )

    # -------------------------------------------------
    # 6. RESULT LOGIC
    # -------------------------------------------------
    if search_query:
        location_key = search_query.lower().strip()
        
        if location_key in SITES:
            site = SITES[location_key]
            
            # --- Result Card ---
            st.markdown(
                f"""
                <div class="result-header">
                    <div class="status-badge">● Active Location</div>
                    <div class="site-name">{site['site']}</div>
                    <div style="color:#94a3b8; margin-top:8px; font-size:0.95rem;">
                        👤 Customer: <span style="color:white; font-weight:600;">{site.get('customer', 'N/A')}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # --- Address Section (Native Streamlit Code Block) ---
            st.caption("📍 SITE ADDRESS")
            # st.code එකෙන් පිරිසිදු Copy Button එකක් ලැබේ
            st.code(site.get("address", "Address unavailable"), language="text")

            # --- Provider Button ---
            st.write("") # පොඩි ඉඩක්
            provider_name = site['provider']
            
            st.link_button(
                label=f"Check {provider_name} Status ➜",
                url=site['url'],
                use_container_width=True,
                type="primary" 
            )
        
        else:
            # --- Not Found Error ---
            st.markdown(
                """
                <div style="
                    margin-top: 20px;
                    padding: 20px;
                    background: rgba(239, 68, 68, 0.08);
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
