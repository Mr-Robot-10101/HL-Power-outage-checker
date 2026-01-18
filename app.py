import json
import streamlit as st
import streamlit.components.v1 as components

# -------------------------------------------------
# 1. Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Power Outage Checker",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# 2. 🎨 ENHANCED GLOBAL CSS
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* ---------------- App Background ---------------- */
    .stApp {
        background: radial-gradient(circle at 50% 10%, #1e1b4b, #020617 60%);
        color: #e2e8f0;
    }

    /* ---------------- Sidebar Styling ---------------- */
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
        transition: all 0.3s ease;
        text-align: left;
        padding-left: 15px;
    }

    section[data-testid="stSidebar"] button:hover {
        background-color: #2563eb;
        color: white;
        border-color: #2563eb;
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }

    /* ---------------- Input Field Styling ---------------- */
    .stTextInput input {
        background-color: rgba(255, 255, 255, 0.05);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 10px;
    }
    .stTextInput input:focus {
        border-color: #facc15;
        box-shadow: 0 0 10px rgba(250, 204, 21, 0.2);
    }

    /* ---------------- Custom Result Card (Glassmorphism) ---------------- */
    .result-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 25px;
        margin-top: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        animation: fadeIn 0.6s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .info-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 4px;
    }

    .info-value {
        font-size: 1.2rem;
        font-weight: 600;
        color: #f8fafc;
        margin-bottom: 15px;
    }

    .status-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 99px;
        background: rgba(34, 197, 94, 0.2);
        color: #4ade80;
        font-size: 0.8rem;
        border: 1px solid rgba(34, 197, 94, 0.3);
        margin-bottom: 20px;
    }

    /* ---------------- Lightning Title ---------------- */
    .lightning {
        display: inline-block;
        animation: pulse 2s infinite;
        color: #facc15;
        text-shadow: 0 0 15px rgba(250, 204, 21, 0.5);
    }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.1); opacity: 1; text-shadow: 0 0 25px rgba(250, 204, 21, 0.8); }
        100% { transform: scale(1); opacity: 0.8; }
    }

    /* ---------------- Provider Button Global ---------------- */
    .provider-btn-container {
        margin-top: 20px;
        text-align: center;
    }
    .provider-btn-container a {
        text-decoration: none;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white !important;
        padding: 12px 30px;
        border-radius: 50px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.4);
        transition: all 0.3s ease;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    .provider-btn-container a:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6);
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    }

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
    st.error("⚠️ sites.json file not found!")

locations_list = list(SITES.keys())

# Session state
if "selected_location" not in st.session_state:
    st.session_state.selected_location = ""

# -------------------------------------------------
# 4. Sidebar
# -------------------------------------------------
with st.sidebar:
    st.markdown("### 🗺️ Locations")
    st.caption("Quick Select")
    
    # Add a little scrollable area styling if list is long
    for loc in locations_list:
        if st.button(loc.title(), use_container_width=True, key=f"loc_{loc}"):
            st.session_state.selected_location = loc
            st.rerun()

# -------------------------------------------------
# 5. Main Header
# -------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; padding: 20px 0 40px 0;">
        <h1 style="margin:0; font-size: 3rem;">
            <span class="lightning">⚡</span> Power Check
        </h1>
        <p style="color: #64748b; margin-top: 10px; font-size: 1.1rem;">
            Instant outage status by location
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# 6. Input Section
# -------------------------------------------------
col1, col2, col3 = st.columns([1, 6, 1])
with col2:
    location = st.text_input(
        "Search Location",
        placeholder="Type a suburb name...",
        value=st.session_state.selected_location,
        label_visibility="collapsed"
    )

# -------------------------------------------------
# 7. Results Display (The Beautiful Card)
# -------------------------------------------------
if location and location.lower() in SITES:
    site = SITES[location.lower()]
    address = site.get("address", "N/A")
    provider = site['provider']
    
    # Define color themes based on provider
    prov_lower = provider.lower()
    if "jemena" in prov_lower:
        prov_color = "#16a34a" # Green
    elif "powercor" in prov_lower:
        prov_color = "#2563eb" # Blue
    elif "ausnet" in prov_lower:
        prov_color = "#7c3aed" # Purple
    else:
        prov_color = "#0ea5e9" # Sky

    # Container for the result
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    # 1. Header of Card
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:start;">
            <div>
                <div class="status-badge">● Active Location</div>
                <h2 style="margin:0; color:white;">{site['site']}</h2>
            </div>
            <div style="text-align:right;">
                <div class="info-label">Customer</div>
                <div style="color:#e2e8f0; font-weight:500;">{site.get('customer', 'N/A')}</div>
            </div>
        </div>
        <hr style="border-color: rgba(255,255,255,0.1); margin: 20px 0;">
        """, 
        unsafe_allow_html=True
    )

    # 2. Address & Copy Button (Embedded HTML)
    # We use flexbox inside the HTML to align the address and button perfectly
    components.html(
        f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500&display=swap');
            body {{ margin: 0; font-family: 'Poppins', sans-serif; background: transparent; }}
            .addr-container {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                background: rgba(0,0,0,0.2);
                padding: 12px 16px;
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.05);
            }}
            .addr-text {{ color: #cbd5e1; font-size: 14px; margin-right: 10px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
            .copy-btn {{
                background: {prov_color};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 500;
                font-size: 13px;
                transition: all 0.2s;
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            .copy-btn:hover {{ filter: brightness(1.1); transform: scale(1.02); }}
            .copy-btn:active {{ transform: scale(0.98); }}
        </style>

        <div class="addr-container">
            <div class="addr-text">📍 {address}</div>
            <button class="copy-btn" onclick="copyToClip()">
                <span id="btn-text">Copy Address</span>
            </button>
        </div>

        <script>
        function copyToClip() {{
            navigator.clipboard.writeText('{address}');
            const btn = document.getElementById('btn-text');
            const original = btn.innerText;
            btn.innerText = '✓ Copied!';
            setTimeout(() => {{ btn.innerText = 'Copy Address'; }}, 2000);
        }}
        </script>
        """,
        height=70
    )

    # 3. Provider Section
    st.markdown(
        f"""
        <div style="margin-top: 10px; display:flex; align-items:center; gap:10px;">
            <div class="info-label" style="margin:0;">Network Provider:</div>
            <div style="font-weight:bold; color:{prov_color}; font-size:1.1rem;">{provider}</div>
        </div>
        
        <div class="provider-btn-container">
            <a href="{site['url']}" target="_blank" style="background: {prov_color};">
                Check {provider} Outage Map ➜
            </a>
        </div>
        </div> """,
        unsafe_allow_html=True
    )

elif location:
    st.markdown(
        """
        <div style="text-align:center; margin-top:40px; color:#ef4444; background:rgba(239,68,68,0.1); padding:20px; border-radius:12px; border:1px solid rgba(239,68,68,0.2);">
            <h3>❌ Location Not Found</h3>
            <p>Please check the suburb name or select from the sidebar.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------
# 8. Footer
# -------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; margin-top: 80px; opacity: 0.4; font-size: 0.8rem;">
        Power Outage Checker © 2024
    </div>
    """,
    unsafe_allow_html=True
)
