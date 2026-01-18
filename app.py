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
# 🌈 VANTA.RINGS – OFFICIAL DEMO LOOK (FIXED)
# -------------------------------------------------
components.html(
    """
    <div id="vanta-bg"></div>

    <style>
        /* Fullscreen VANTA background */
        #vanta-bg {
            position: fixed;
            inset: 0;
            width: 100vw;
            height: 100vh;
            z-index: -5;
            pointer-events: none;
        }

        /* Make Streamlit transparent */
        .stApp {
            background: transparent;
            color: #e5e7eb;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.92);
        }

        section[data-testid="stSidebar"] button {
            background-color: rgba(255,255,255,0.08);
            color: white;
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 10px;
            padding: 10px;
            font-weight: 500;
            transition: all 0.2s ease;
        }

        section[data-testid="stSidebar"] button:hover {
            background-color: rgba(255,255,255,0.16);
            transform: translateY(-1px);
        }

        /* Lightning pulse */
        .lightning {
            display: inline-block;
            margin-right: 6px;
            animation: pulse 2.6s ease-in-out infinite;
            text-shadow: 0 0 12px rgba(255,255,255,0.8);
        }

        @keyframes pulse {
            0%,100% { transform: scale(1); opacity: .9; }
            50% { transform: scale(1.18); opacity: 1; }
        }

        /* Provider button */
        .provider-btn a {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 22px;
            border-radius: 999px;
            font-weight: 600;
            text-decoration: none;
            color: white !important;
            background: rgba(255,255,255,0.12);
            border: 1px solid rgba(255,255,255,0.18);
            backdrop-filter: blur(8px);
            transition: all 0.25s ease;
        }

        .provider-btn a:hover {
            background: rgba(255,255,255,0.22);
            transform: translateY(-2px);
        }
    </style>

    <!-- VANTA scripts -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r134/three.min.js"></script>
    <script
