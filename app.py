import json
import streamlit as st

# -------------------------------------------------
# 1. Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Power Check",
    page_icon="⚡",
    layout="centered"
)

# -------------------------------------------------
# 2. 🎨 CLEAN CSS (පිරිසිදු පෙනුම සඳහා)
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* Google Font Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Background */
    .stApp {
        background: radial-gradient(125% 125% at 50% 10%, #020617 40%, #1e1b4b 100%);
        color: white;
    }

    /* Input Field Styling */
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

    /* Custom Card Styling */
    .site-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        margin-top: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }

    /* Badge Styling */
    .status-badge {
        display: inline-flex;
        align-items: center;
        background-color: rgba(34, 197, 94, 0.2);
        color: #4ade80;
        padding: 4px 12px;
        border-radius: 99px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid rgba(34, 197, 94, 0.3);
        margin-bottom: 10px;
    }

    /* Typography */
    .site-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(to right, #fff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 5px 0 5px 0;
    }

    .customer-text {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Hide Streamlit Main Menu & Footer for cleaner look */
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

# -------------------------------------------------
# 4. Header
# -------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True) # Top spacing
st.markdown(
    """
    <div style="text-align:center; margin-bottom: 30px;">
        <h1 style="margin:0; font-size: 2.5rem;">⚡ Power Check</h1>
        <p style="color: #64748b; font-size: 1rem;">Check outage status instantly</p>
    </div>
    """, 
    unsafe_allow_html=True
)

# -------------------------------------------------
# 5. Search Input
# -------------------------------------------------
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    search_query = st.text_input(
        "Location", 
        placeholder="Enter suburb name...", 
        label_visibility="collapsed"
    )

# -------------------------------------------------
# 6. Display Results (Clean & Native)
# -------------------------------------------------
if search_query:
    location_key = search_query.lower().strip()
    
    if location_key in SITES:
        site = SITES[location_key]
        
        # --- START OF CARD UI ---
        # අපි CSS Card එකක් ඇතුලේ Streamlit elements දාන්න බෑ.
        # ඒ නිසා අපි Markdown වලින් Structure එක හදලා, 
        # Native Elements (Code block, Button) ඊට යටින් පෙන්වමු.
        
        # 1. Title & Metadata Area
        st.markdown(
            f"""
            <div class="site-card">
                <div class="status-badge">● Active Location</div>
                <div class="site-title">{site['site']}</div>
                <div class="customer-text">
                    <span>👤 Customer:</span>
                    <span style="color:white;">{site.get('customer', 'N/A')}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # 2. Address (Using Streamlit's Native Code Block for Perfect Copy Button)
        st.markdown("###### 📍 Site Address")
        st.code(site.get("address", "Address not available"), language="text")

        # 3. Provider Button (Native Link Button)
        st.write("") # Spacer
        provider_name = site['provider']
        
        # Provider URL
        st.link_button(
            label=f"Check {provider_name} Status ➜",
            url=site['url'],
            use_container_width=True,
            type="primary"  # This makes it stand out
        )
        
    else:
        # Error Message
        st.markdown(
            """
            <div style="
                margin-top: 20px;
                padding: 15px;
                background: rgba(239, 68, 68, 0.1);
                border: 1px solid rgba(239, 68, 68, 0.2);
                border-radius: 12px;
                color: #fca5a5;
                text-align: center;
            ">
                ❌ Location not found. Please check spelling.
            </div>
            """,
            unsafe_allow_html=True
        )
