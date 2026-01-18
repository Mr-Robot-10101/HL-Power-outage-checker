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
# 🎨 PREMIUM UX/UI THEME
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* ---------- Global ---------- */
    .stApp {
        background: radial-gradient(circle at top, #0f172a, #020617);
        color: #e5e7eb;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617, #020617);
    }

    section[data-testid="stSidebar"] button {
        background: #020617;
        color: #e5e7eb;
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 12px;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] button:hover {
        background: #1f6feb;
        color: white;
        border-color: #1f6feb;
        transform: translateY(-1px);
    }

    /* ---------- Card ---------- */
    .card {
        background: rgba(2, 6, 23, 0.75);
        border: 1px solid #1f2937;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }

    /* ---------- Provider Button ---------- */
    .provider-link-btn a {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 12px 22px;
        border-radius: 999px;
        color: #fff !important;
        font-weight: 600;
        text-decoration: none;
        box-shadow: 0 8px 24px rgba(0,0,0,.45);
        transition: all .25s ease;
    }

    .provider-link-btn a:hover {
        transform: translateY(-2px) scale(1.02);
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

    /* ---------- Mobile ---------- */
    @media (max-width: 768px) {
        .provider-link-btn a {
            width: 100%;
            justify-content: center;
        }
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
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.markdown("## ⚡ Locations")
    st.caption("📌 Select a site to view details")

    for loc in locations_list:
        if st.button(loc.title(), use_container_width=True, key=f"loc_{loc}"):
            st.session_state.selected_location = loc
            st.rerun()

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown(
    """
    <div style="text-align:center;margin-bottom:16px;">
        <h1>⚡ Power Outage Checker</h1>
        <p style="opacity:.75">
            Quickly access provider outage pages for each site
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
# Empty state
# -------------------------------------------------
if not location:
    st.info("👈 Select a location from the sidebar to begin")

# -------------------------------------------------
# Main view
# -------------------------------------------------
if location and location.lower() in SITES:
    site = SITES[location.lower()]
    address = site.get("address", "N/A")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.success(
        f"📍 **{site['site']}**\n\n"
        f"👤 **Customer:** {site.get('customer', 'N/A')}"
    )

    # Address + Copy (NO rerun, browser-only)
    components.html(
        f"""
        <div style="
            display:flex;
            align-items:center;
            gap:12px;
            margin:12px 0;
        ">
            <div style="
                font-weight:600;
                color:#ffffff;
                font-size:16px;
            ">
                Address: {address}
            </div>

            <button
                style="
                    padding:6px 14px;
                    border-radius:8px;
                    border:none;
                    background:#2563eb;
                    color:white;
                    cursor:pointer;
                    font-weight:600;
                "
                onclick="
                    navigator.clipboard.writeText('{address}');
                    this.innerText='✔ Copied';
                    setTimeout(()=>this.innerText='📋 Copy',1500);
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

    st.markdown('</div>', unsafe_allow_html=True)

elif location:
    st.error("❌ Location not found in database")
