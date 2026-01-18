import json
import streamlit as st
import streamlit.components.v1 as components

# -------------------------------------------------
# 1. Page Config (මූලික පිටු සැකසුම්)
# -------------------------------------------------
st.set_page_config(
    page_title="Power Check",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# 2. 🎨 CSS Styles (Animation සහ Solid Buttons සඳහා)
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* Google Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Vanta.js Animation එක පෙනෙන්න නම් 
       Streamlit Main Background එක විනිවිද පෙනෙන (Transparent) විය යුතුයි.
    */
    .stApp {
        background: transparent !important;
    }

    /* --- SIDEBAR STYLING --- */
    section[data-testid="stSidebar"] {
        background-color: rgba(11, 15, 25, 0.85); /* පොඩි විනිවිද පෙනෙන ගතියක් */
        border-right: 1px solid rgba(255,255,255,0.05);
        backdrop-filter: blur(10px); /* Sidebar එකට Blur එකක් */
    }

    section[data-testid="stSidebar"] h3 {
        color: #f1f5f9;
        font-size: 1.1rem;
        margin-bottom: 10px;
    }

    /* Sidebar Buttons - Solid Box & Centered Text (ඔබ ඉල්ලූ විදියට) */
    section[data-testid="stSidebar"] button {
        background-color: rgba(30, 41, 59, 0.95) !important; /* තද පසුබිමක් */
        color: #cbd5e1 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        margin-bottom: 6px !important;
        
        /* Force Centering */
        text-align: center !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        
        /* Font Settings */
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* Fix inner paragraph alignment */
    section[data-testid="stSidebar"] button p {
        text-align: center !important;
        width: 100%;
        margin: 0;
    }

    /* Hover Effect */
    section[data-testid="stSidebar"] button:hover {
        background-color: rgba(59, 130, 246, 0.4) !important;
        border-color: #3b82f6 !important;
        color: white !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    /* Active/Focus Effect */
    section[data-testid="stSidebar"] button:focus {
        border-color: #60a5fa !important;
        background-color: rgba(37, 99, 235, 0.6) !important;
        color: white !important;
    }

    /* --- MAIN CONTENT CARD STYLING --- */
    .result-header {
        background: rgba(15, 23, 42, 0.75); /* අඳුරු පසුබිමක් (Glass Effect) */
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        backdrop-filter: blur(20px); /* පසුබිම බොඳ කිරීම */
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
        font-size: 2.5rem;
        font-weight: 800;
        margin: 5px 0 15px 0;
        background: linear-gradient(to bottom, #fff, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }

    /* Welcome Box (කිසිවක් තෝරා නැති විට) */
    .welcome-box {
        margin-top: 40px;
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
    
    # Button List
    for loc in locations_list:
        if st.button(loc.title(), use_container_width=True, key=f"loc_{loc}"):
            st.session_state.selected_location = loc
            st.rerun()

# -------------------------------------------------
# 5. Main Content Area
# -------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

# Title Area (Z-Index added to stay above animation)
st.markdown(
    """
    <div style="text-align:center; margin-bottom: 30px; position: relative; z-index: 1;">
        <h1 style="margin:0; font-size: 3.2rem; text-shadow: 0 4px 10px rgba(0,0,0,0.8);">
            ⚡ Power Check
        </h1>
        <p style="color: #cbd5e1; font-size: 1.1rem; margin-top:8px; text-shadow: 0 2px 5px rgba(0,0,0,0.8);">
            Real-time outage status by location
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# --- RESULTS DISPLAY ---

if st.session_state.selected_location:
    location_key = st.session_state.selected_location.lower().strip()
    
    if location_key in SITES:
        site = SITES[location_key]
        
        # --- Info Card ---
        st.markdown(
            f"""
            <div class="result-header">
                <div class="status-badge">● Active Location</div>
                <div class="site-name">{site['site']}</div>
                <div style="color:#cbd5e1; font-size:1rem;">
                    👤 Customer: <span style="color:white; font-weight:600;">{site.get('customer', 'N/A')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # --- Address (Native Copy Button) ---
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
        st.error("Error: Location data not found.")

else:
    # කිසිවක් තෝරා නැති විට
    st.markdown(
        """
        <div class="welcome-box">
            <h3>👈 Select a location</h3>
            <p>Click on any location in the sidebar to view details.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------
# 6. ✨ VANTA.JS BACKGROUND ANIMATION ✨
# -------------------------------------------------
components.html(
    """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/vanta@latest/dist/vanta.rings.min.js"></script>
    
    <script>
        // Inject Vanta Effect into Streamlit Main Container
        var script = document.createElement("script");
        script.innerHTML = `
            if (!window.vantaEffect) {
                window.vantaEffect = VANTA.RINGS({
                    el: ".stApp",
                    mouseControls: true,
                    touchControls: true,
                    gyroControls: false,
                    minHeight: 200.00,
                    minWidth: 200.00,
                    scale: 1.00,
                    scaleMobile: 1.00,
                    backgroundColor: 0x020617, // Dark Background
                    color: 0x2563eb            // Blue Rings
                })
            }
        `;
        window.parent.document.body.appendChild(script);
    </script>
    """,
    height=0,
)
