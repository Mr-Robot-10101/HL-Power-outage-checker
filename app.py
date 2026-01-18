import json
import streamlit as st
import streamlit.components.v1 as components

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Power Outage Checker",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# 🎨 MESH BACKGROUND + LIGHTNING PULSE
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* ---------- Base ---------- */
    .stApp {
        background-color: #020617;
        color: #e5e7eb;
        overflow: hidden;
    }

    /* ---------- Mesh blobs ---------- */
    .mesh-bg {
        position: fixed;
        inset: 0;
        z-index: -1;
        overflow: hidden;
    }

    .blob {
        position: absolute;
        width: 480px;
        height: 480px;
        border-radius: 50%;
        filter: blur(120px);
        opacity: 0.45;
        animation: float 22s infinite alternate ease-in-out;
    }

    .blob.blue {
        background: #2563eb;
        top: -120px;
        left: -120px;
        animation-delay: 0s;
    }

    .blob.purple {
        background: #7c3aed;
        top: 30%;
        right: -150px;
        animation-delay: 4s;
    }

    .blob.green {
        background: #16a34a;
        bottom: -160px;
        left: 25%;
        animation-delay: 8s;
    }

    @keyframes float {
        0% {
            transform: translateY(0px) translateX(0px) scale(1);
        }
        50% {
            transform: translateY(-60px) translateX(40px) scale(1.15);
        }
        100% {
            transform: translateY(40px) translateX(-30px) scale(0.95);
        }
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background-color: #020617;
    }

    section[data-testid="stSidebar"] button {
        background-color: #2563eb;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] button:hover {
        background-color: #1d4ed8;
        transform: translateY(-1px);
    }

    /* ---------- Lightning pulse ---------- */
    .lightning {
        display: inline-block;
        animation: pulse 2.6s ease-in-out infinite;
        text-shadow: 0 0 14px rgba(250,204,21,0.8);
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.9; }
        50% { transform: scale(1.18); opacity: 1; }
    }

    /* ---------- Provider buttons ---------- */
    .provider-btn a {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 12px 22px;
        border-radius: 999px;
        font-weight: 600;
        text-decoration: none;
        color: white !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        transition: all 0.25s ease;
    }

    .jemena a { background: linear-gradient(90deg,#16a34a,#22c55e); }
    .powercor a { background: linear-gradient(90deg,#2563eb,#1d4ed8); }
    .ausnet a { background: linear-gradient(90deg,#7c3aed,#9333ea); }
    .default a { background: linear-gradient(90deg,#1f6feb,#2563eb); }

    .provider-btn a:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.45);
    }
    </style>

    <!-- Mesh background HTML -->
    <div class="mesh-bg">
        <div class="blob blue"></div>
        <div class="blob purple"></div>
        <div class="blob green"></div>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Load sites
# -------------------------------------------------
with open("sites.json", "r", encoding="utf-8") as f:
    SITES = json.load(f)

locations_list = list(SITES.keys())

# -------------------------------------------------
# Session
# -------------------------------------------------
if "selected_location" not in st.session_state:
    st.session_state.selected_location = ""

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ Locations")
    st.caption("Tap to auto-fill")

    for loc in locations_list:
        if st.button(loc.title(), use_container_width=True):
            st.session_state.selected_location = loc
            st.rerun()

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; margin-bottom:20px;">
        <h1><span class="lightning">⚡</span> Power Outage Checker</h1>
        <p style="opacity:0.75;">
            Auto-check power status using live provider outage maps
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Input
# -------------------------------------------------
location = st.text_input(
    "📍 Enter Location / Suburb",
    value=st.session_state.selected_location
)

# -------------------------------------------------
# Main
# -------------------------------------------------
if location and location.lower() in SITES:
    site = SITES[location.lower()]
    address = site.get("address", "N/A")

    st.success(
        f"📍 **{site['site']}**\n\n"
        f"👤 **Customer:** {site.get('customer','N/A')}"
    )

    components.html(
        f"""
        <div style="display:flex; gap:12px; align-items:center;">
            <div style="font-weight:600; color:white;">
                Address: {address}
            </div>
            <button
                style="padding:6px 12px;border-radius:8px;border:none;
                       background:#2563eb;color:white;font-weight:600;"
                onclick="navigator.clipboard.writeText('{address}');
                         this.innerText='✓ Copied';
                         this.style.background='#16a34a';">
                📋 Copy
            </button>
        </div>
        """,
        height=60
    )

    st.write(f"**Provider:** {site['provider']}")

    p = site["provider"].lower()
    cls = "jemena" if "jemena" in p else "powercor" if "powercor" in p else "ausnet" if "ausnet" in p else "default"

    st.markdown(
        f"""
        <div class="provider-btn {cls}">
            <a href="{site['url']}" target="_blank">🔗 Open Provider Outage Page</a>
        </div>
        """,
        unsafe_allow_html=True
    )

elif location:
    st.error("❌ Location not found")
