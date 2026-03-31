import streamlit as st
from core.simulator import LogisticMapSimulator
from core.sim_data import PRECALC_DATA
from utils.helpers import init_viewport_width, is_mobile_layout
from utils.ui import inject_custom_css, inject_sidebar_button_css, render_header, show_mobile_warning

# Import our modular views
from views import tab_bifurcation, tab_dynamics, tab_predict, tab_compare, tab_info

# === PAGE CONFIGURATION ===
st.set_page_config(
    page_title="Chaos & Predictability: Logistic Map Simulator | Altug Aksoy",
    page_icon="🦋", layout="wide", initial_sidebar_state="expanded",
    menu_items={
        'Report a bug': "mailto:aaksoy@miami.edu",
        'Get help': "https://github.com/hailcloud-um/logistic_map/tree/main",
        'About': "### Logistic Map Simulator\n**Interactive Research Tool for Chaos & Predictability**"
    }
)

# === GLOBAL STATE INITIALIZATION ===
if 'selected_tab_index' not in st.session_state: st.session_state.selected_tab_index = 0
if 'simulation_ran' not in st.session_state: st.session_state.simulation_ran = False
if 'info_sub_tab' not in st.session_state: st.session_state.info_sub_tab = "about" 
if 'pred_data' not in st.session_state: st.session_state.pred_data = PRECALC_DATA.copy()
if 'pred_ensemble_metric' not in st.session_state: st.session_state.pred_ensemble_metric = 'median'

# Initialize session states for all tabs explicitly
tab_bifurcation.init_session_state()
tab_dynamics.init_session_state()
tab_predict.init_session_state()
tab_compare.init_session_state()
tab_info.init_session_state()

# === UI INJECTION ===
inject_custom_css()
init_viewport_width()
if is_mobile_layout() and 'mobile_warning_acknowledged' not in st.session_state:
    show_mobile_warning()

inject_sidebar_button_css(st.session_state.selected_tab_index)

@st.cache_resource
def get_simulator():
    return LogisticMapSimulator()

simulator = get_simulator()
current_tab = st.session_state.selected_tab_index

# =====================================================================
# === 1. PROCESS SIDEBAR LOGIC (Triggers reruns BEFORE UI draws) ======
# =====================================================================
if current_tab == 0:
    tab_bifurcation.render_sidebar(simulator)
elif current_tab == 1:
    tab_dynamics.render_sidebar(simulator)
elif current_tab == 2:
    tab_predict.render_sidebar()
elif current_tab == 3:
    tab_compare.render_sidebar(simulator)
elif current_tab == 4:
    tab_info.render_sidebar()

# =====================================================================
# === 2. RENDER HEADER & TABS =========================================
# =====================================================================
render_header()
tab_col_space1, tab_col1, tab_col2, tab_col3, tab_col4, tab_col5, tab_col_space2 = st.columns([0.05, 1, 1, 1, 1, 1, 0.05])

def switch_tab(index):
    if st.session_state.selected_tab_index != index:
        st.session_state.selected_tab_index = index
        st.rerun()

with tab_col1:
    if st.button("Bifurcation", type="primary" if current_tab == 0 else "secondary", width='stretch', key="tab_btn_0"): switch_tab(0)
with tab_col2:
    if st.button("Dynamics", type="primary" if current_tab == 1 else "secondary", width='stretch', key="tab_btn_1"): switch_tab(1)
with tab_col3:
    if st.button("Predictability", type="primary" if current_tab == 2 else "secondary", width='stretch', key="tab_btn_2"): switch_tab(2)
with tab_col4:
    if st.button("Comparative Error Growth", type="primary" if current_tab == 3 else "secondary", width='stretch', key="tab_btn_3"): switch_tab(3)
with tab_col5:
    if st.button("Info", type="primary" if current_tab == 4 else "secondary", width='stretch', key="tab_btn_4"): switch_tab(4)

# =====================================================================
# === 3. RENDER MAIN TAB CONTENT ======================================
# =====================================================================
if current_tab == 0:
    tab_bifurcation.render_main()
elif current_tab == 1:
    tab_dynamics.render_main()
elif current_tab == 2:
    tab_predict.render_main()
elif current_tab == 3:
    tab_compare.render_main()
elif current_tab == 4:
    tab_info.render_main()
    