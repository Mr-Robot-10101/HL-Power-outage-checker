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
# 🎨 MODERN UI THEME (Glass + Soft Glow)
# -------------------------------------------------
st.markdown(
    """
    <style>
    /* ---------- Background ---------- */
    .stApp {
        background: radial-gradient(circle at top, #0f172a, #020617);
        color: #e5e7eb;
    }

    /* ---------- Header ---------- */
    .app-title {
        font-size: 44px;
        font-weight: 800;
        letter-spacing: -0.5px;
        text-align: center;
        margin-bottom: 4px;
    }

    .app-subtitle {
        text-align: center;
        opacity: 0.75;
        font-size: 15px;
        margin-bottom: 28px;
    }

    /* ---------- Input (glass) ---------- */
    input {
        background: rgba(15, 23, 42, 0.75) !important;
        border-radius: 14px !important;
        border: 1px solid #1f2937 !important;
        padding: 14px !important;
        font-size: 15px !important;
    }

    /* ---------- Card ---------- */
    .card {
        background: rgba(2, 6, 23, 0.7);
        border: 1px solid #1f2937;
        border-radius: 18px;
        padding: 22px;
        margin-top: 20px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.45);
        backdrop-filter: blur(6px);
    }

    /* ---------- Address row ---------- */
    .address-row {
        display: flex;
        align-items: center;
        gap: 14px;
        margin: 14px 0;
        font-size: 16px;
        font-weight: 600;
        color: #ffffff;
    }

    .copy-btn {
        padding: 6px 14px;
        border-radius: 999px;
        border: none;
        background: linear-gradient(90deg, #2563eb, #1d4ed8);
        color: white;
        cursor: pointer;
        font-weight: 600;
        transition: all 0.25s ease;
    }

    .copy-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(37,99,235,0.45);
    }

    /* ---------- Provider Button ---------- */
    .provider-btn {
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

    .provider-btn:hover {
        transform: translateY(-2px);
    }

    .jemena { background: linear-gradient(90deg, #16a34a, #22c55e); }
    .powercor { background: linear-gradient(90deg, #2563eb, #1d4ed8); }
    .ausnet { background: linear-gradient(90deg, #7c3aed, #9333ea); }
    .default { background: linear-gradient(90deg, #1f6feb, #2563eb); }

    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Load data
# -------------------------------------------------
with open("sites.json", "r", encoding="utf-8") as f:
    SITES = json.load(f)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.markdown(
    """
    <div class="app-title">⚡ Power Outage Checker</div>
    <div class="app-subtitle">
        Quickly access provider outage pages for each site
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# Input
# -------------------------------------------------
location = st.text_input(
    "📍 Enter Location / Suburb"
)

# -------------------------------------------------
# Main content
# -------------------------------------------------
if location and location.lower() in SITES:
    site = SITES[location.lower()]
    address = site.get("address", "N/A")
    provider = site.get("provider", "").lower()

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.success(
        f"📍 **{site['site']}**\n\n"
        f"👤 **Customer:** {site.get('customer', 'N/A')}"
    )

    # Address + Copy (browser-only, no rerun)
    components.html(
        f"""
        <div class="address-row">
            Address: {address}
            <button class="copy-btn"
                onclick="
                    navigator.clipboard.writeText('{address}');
                    this.innerText='✓ Copied';
                    setTimeout(()=>this.innerText='📋 Copy',1500);
                ">
                📋 Copy
            </button>
        </div>
        """,
        height=60
    )

    st.write(f"**Provider:** {site['provider']}")

    # Provider color
    if "jemena" in provider:
        cls = "jemena"
    elif "powercor" in provider:
        cls = "powercor"
    elif "ausnet" in provider:
        cls = "ausnet"
    else:
        cls = "default"

    st.markdown(
        f"""
        <a class="provider-btn {cls}" href="{site['url']}" target="_blank">
            🔗 Open Provider Outage Page
        </a>
        """,
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

elif location:
    st.error("❌ Location not found in database")
