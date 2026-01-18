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
# 🎨 GLOBAL CSS (Animated background + Lightning pulse)
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* ---------------- App background animation ---------------- */
    .stApp {
        background: linear-gradient(
            -45deg,
            #020617,
            #0f172a,
            #020617,
            #111827
        );
        background-size: 400% 400%;
        animation: gradientMove 18s ease infinite;
        color: #e5e7eb;
    }

    @keyframes gradientMove {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ---------------- Sidebar ---------------- */
    section[data-testid="stSidebar"] {
        background-color: #020617;
    }

    section[data-testid="stSidebar"] button {
        background-color: #2563eb;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] button:hover {
        background-color: #1d4ed8;
        transform: translateY(-1px);
    }

    /* ---------------- Lightning pulse ---------------- */
    .lightning {
        display: inline-block;
        margin-right: 6px;
        animation: lightningPulse 2.8s ease-in-out infinite;
        text-shadow:
            0 0 6px rgba(250,204,21,0.6),
            0 0 14px rgba(250,204,21,0.35);
    }

    @keyframes lightningPulse {
        0% {
            transform: scale(1);
            opacity: 0.9;
        }
        50% {
            transform: scale(1.15);
            opacity: 1;
            text-shadow:
                0 0 10px rgba(250,204,21,0.9),
                0 0 24px rgba(250,204,21,0.55);
        }
        100% {
            transform: scale(1);
            opacity: 0.9;
        }
    }

    /* ---------------- Provider buttons ---------------- */
    .provider-link-btn a {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 12px 22px;
        border-radius: 999px;
        color: #ffffff !important;
        text-decoration: none;
        font-weight: 600;
        font-size: 14px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.35);
        transition: all 0.25s ease;
    }

    .provider-jemena a {
        background: linear-gradient(90deg, #16a34a, #22c55e);
    }

    .provider-powercor a {
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
    }

    .provider-ausnet a {
        background: linear-gradient(90deg, #7c3aed, #9333ea);
    }

    .provider-default a {
        background: linear-gradient(90deg, #1f6feb, #2563eb);
    }

    .provider-link-btn a:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 26px rgba(0,0,0,0.45);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Load sites database
# -------------------------------------------------
with open("sites.json", "r", encoding="utf-8") as f:
    SITES = json.load(f)

locations_list = list(SITES.keys())

# -------------------------------------------------
# Session state
# -------------------------------------------------
if "selected_location" not in st.session_state:
    st.session_state.selected_location = ""

# -------------------------------------------------
# Sidebar – Locations
# -------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ Locations")
    st.caption("Tap a location to auto-fill")

    for loc in locations_list:
        if st.button(loc.title(), use_container_width=True, key=f"loc_{loc}"):
            st.session_state.selected_location = loc
            st.rerun()

# -------------------------------------------------
# Header with lightning pulse
# -------------------------------------------------
st.markdown(
    """
    <div style="text-align:center; margin-bottom:20px;">
        <h1>
            <span class="lightning">⚡</span> Power Outage Checker
        </h1>
        <p style="opacity:0.75;">
            Auto-check power status using live provider outage maps
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Location input
# -------------------------------------------------
location = st.text_input(
    "📍 Enter Location / Suburb",
    value=st.session_state.selected_location
)

# -------------------------------------------------
# Main content
# -------------------------------------------------
if location and location.lower() in SITES:
    site = SITES[location.lower()]
    address = site.get("address", "N/A")

    st.success(
        f"📍 **{site['site']}**\n\n"
        f"👤 **Customer:** {site.get('customer', 'N/A')}"
    )

    # ---------------- Address + copy (NO rerun) ----------------
    components.html(
        f"""
        <div style="display:flex; align-items:center; gap:12px; margin:10px 0;">
            <div style="font-weight:600; color:#ffffff; font-size:16px;">
                Address: {address}
            </div>
            <button
                style="
                    padding:6px 12px;
                    border-radius:8px;
                    border:none;
                    background:#2563eb;
                    color:white;
                    cursor:pointer;
                    font-weight:600;
                "
                onclick="
                    navigator.clipboard.writeText('{address}');
                    this.innerText='✓ Copied';
                    this.style.background='#16a34a';
                "
            >
                📋 Copy
            </button>
        </div>
        """,
        height=60,
    )

    st.write(f"**Provider:** {site['provider']}")

    provider_name = site["provider"].lower()
    if "jemena" in provider_name:
        provider_class = "provider-jemena"
    elif "powercor" in provider_name:
        provider_class = "provider-powercor"
    elif "ausnet" in provider_name:
        provider_class = "provider-ausnet"
    else:
        provider_class = "provider-default"

    st.markdown(
        f"""
        <div class="provider-link-btn {provider_class}">
            <a href="{site['url']}" target="_blank">
                🔗 Open Provider Outage Page
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

elif location:
    st.error("❌ Location not found in database")
