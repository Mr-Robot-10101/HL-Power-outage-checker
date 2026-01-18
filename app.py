import json
import streamlit as st

# -------------------------------------------------
# 1. Page Config (පිටුවේ මූලික සැකසුම්)
# -------------------------------------------------
st.set_page_config(
    page_title="Power Check",
    page_icon="⚡",
    layout="centered"
)

# -------------------------------------------------
# 2. 🎨 CSS Styles (ලස්සන කිරීම සඳහා)
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* Google Font Import - Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Background Gradient (පසුබිම) */
    .stApp {
        background: radial-gradient(125% 125% at 50% 10%, #020617 40%, #1e1b4b 100%);
        color: white;
    }

    /* Search Box Styling */
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

    /* Result Card Styling */
    .result-header {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* Active Status Badge */
    .status-badge {
        display: inline-block;
        background-color: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        padding: 5px 15px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid rgba(34, 197, 94, 0.3);
        margin-bottom: 10px;
    }

    /* Site Title */
    .site-name {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(to bottom, #fff, #cbd5e1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Customer Name */
    .customer-label {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 5px;
    }

    /* Hide default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# 3. Load Data (දත්ත ලබා ගැනීම)
# -------------------------------------------------
try:
    with open("sites.json", "r", encoding="utf-8") as f:
        SITES = json.load(f)
except FileNotFoundError:
    SITES = {}
    st.error("⚠️ sites.json file not found!")

# -------------------------------------------------
# 4. App Header
# -------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True) # Top spacing
st.markdown(
    """
    <div style="text-align:center; margin-bottom: 40px;">
        <h1 style="margin:0; font-size: 3rem;">⚡ Power Check</h1>
        <p style="color: #64748b; font-size: 1.1rem; margin-top:5px;">Check outage status instantly</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# -------------------------------------------------
# 5. Search Area
# -------------------------------------------------
# මැදට වෙන්න Input box එක තියන්න Columns පාවිච්චි කරමු
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    search_query = st.text_input(
        "Search Location", 
        placeholder="Enter suburb name (e.g., Claremont)...", 
        label_visibility="collapsed"
    )

# -------------------------------------------------
# 6. Result Display logic
# -------------------------------------------------
if search_query:
    location_key = search_query.lower().strip()
    
    if location_key in SITES:
        site = SITES[location_key]
        
        # --- A. Header Card (Name & Status) ---
        with col2:
            st.markdown(
                f"""
                <div class="result-header">
                    <div class="status-badge">● Active Location</div>
                    <div class="site-name">{site['site']}</div>
                    <div class="customer-label">👤 Customer: <span style="color:white">{site.get('customer', 'N/A')}</span></div>
                </div>
                """,
                unsafe_allow_html=True
            )

            # --- B. Address Section (Clean Code Block) ---
            st.caption("📍 SITE ADDRESS")
            # st.code එකෙන් ඉබේම Copy Button එකක් ලැබෙන නිසා මෙය හරිම පිළිවෙලයි
            st.code(site.get("address", "Address unavailable"), language="text")

            # --- C. Provider Link Button ---
            st.write("") # පොඩි ඉඩක් (Spacer)
            
            provider_name = site['provider']
            # ලස්සන ලොකු Button එකක්
            st.link_button(
                label=f"Check {provider_name} Outage Map ➜",
                url=site['url'],
                use_container_width=True,
                type="primary" 
            )
        
    else:
        # සොයාගත නොහැකි වූ විට
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
                ">
                    ❌ Location not found in database.
                </div>
                """,
                unsafe_allow_html=True
            )

# -------------------------------------------------
# 7. Simple Footer
# -------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; margin-top: 80px; opacity: 0.3; font-size: 0.8rem;">
        Power Check System © 2025
    </div>
    """,
    unsafe_allow_html=True
)
