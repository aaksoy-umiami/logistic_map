import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
            .block-container { padding-top: 3rem !important; padding-bottom: 1rem !important; }
            div[data-testid="column"] button {
                width: 100%; border-radius: 8px; padding: 10px; font-weight: 600; font-size: 14px;
                transition: all 0.3s ease; border: 2px solid #000000 !important;
            }
            div[data-testid="column"] button[kind="secondary"] { background-color: rgba(255, 255, 255, 0.05); color: rgba(255, 255, 255, 0.7); }
            div[data-testid="column"] button[kind="primary"] { background: linear-gradient(135deg, #32b8c6 0%, #1d7480 100%); color: white; box-shadow: 0 4px 12px rgba(50, 184, 198, 0.3); }
            div[data-testid="column"] button:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(50, 184, 198, 0.4); }
            [data-testid="stHorizontalBlock"]:has(button[kind="primary"], button[kind="secondary"]) { border-bottom: 2px solid #000000; padding-bottom: 0px; margin-bottom: 0px; }
            [data-testid="stSidebar"] { display: block !important; min-width: 320px !important; }
            @media (max-width: 768px) {
                [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] button[key^="tab_btn_"] { margin-bottom: 0.35rem; }
                section.main > div { padding-left: 0.5rem !important; padding-right: 0.5rem !important; }
                html, body { font-size: 16px !important; }
            }
            [data-testid="stSidebar"] label, [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { font-size: 16px !important; }
            [data-testid="stSidebar"] [data-testid="stTooltipIcon"] { margin-top: 4px; }
        </style>
    """, unsafe_allow_html=True)

def inject_sidebar_button_css(current_tab):
    if current_tab in [0, 1, 2, 3]:
        st.markdown("""
        <style>
            [data-testid="stSidebar"] button[kind="primary"] { background-color: #ffffff !important; color: #ff4b4b !important; border: 3px solid #ff4b4b !important; font-weight: 600; }
            [data-testid="stSidebar"] button[kind="secondary"] { background-color: #228B22 !important; color: white !important; border: 3px solid #228B22 !important; font-weight: 600; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            [data-testid="stSidebar"] button[kind="primary"] { background-color: #ffffff !important; color: #000000 !important; border: 3px solid #000000 !important; font-weight: 600; }
            [data-testid="stSidebar"] button[kind="secondary"] { background-color: #000000 !important; color: white !important; border: 3px solid #000000 !important; font-weight: 600; }
        </style>
        """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
    <div style='text-align: center; margin-bottom: 10px;'>
        <h3 style='color: #32b8c6; margin: 0; padding: 0; font-size: 32px;'>🦋 Logistic Map Simulator</h3>
        <p style='font-size: 14px; color: #666; margin: 0;'>Exploration of chaos & predictability | <span style='font-style: italic;'>Aksoy (2024) Chaos, 34, 011102</span></p>
    </div>
    <hr style='margin-top: 5px; margin-bottom: 15px;'>
    """, unsafe_allow_html=True)

@st.dialog("📱 Mobile Device Detected")
def show_mobile_warning():
    st.write("This simulation involves complex visualizations that are best viewed on a **Desktop or Laptop**.")
    st.write("You may experience layout issues or slow performance on smaller screens.")
    if st.button("I Understand"):
        st.session_state.mobile_warning_acknowledged = True
        st.rerun()