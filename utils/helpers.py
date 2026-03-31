import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from io import BytesIO
import base64
from streamlit_js_eval import streamlit_js_eval

def is_mobile_layout():
    vw = st.session_state.get("viewport_width", None)
    if vw is None: return False
    return vw < 768

def get_plot_figsize():
    return (5, 4) if is_mobile_layout() else (7, 6)

def get_bif_figsize():
    return (6, 4.5) if is_mobile_layout() else (10, 6)

def create_white_based_colormap(base_cmap_name):
    base_cmap = plt.get_cmap(base_cmap_name)
    n_colors = 256
    base_colors = base_cmap(np.linspace(0, 1, n_colors))
    new_colors = np.ones((n_colors, 4))
    transition_idx = int(n_colors * 0.1)
    
    for i in range(transition_idx):
        alpha = i / transition_idx
        new_colors[i] = (1 - alpha) * np.array([1, 1, 1, 1]) + alpha * base_colors[0]
    
    new_colors[transition_idx:] = base_colors[:(n_colors - transition_idx)]
    return LinearSegmentedColormap.from_list(f'white_{base_cmap_name}', new_colors)

def get_image_base64(fig):
    buffer = BytesIO()
    fig.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode()
    plt.close(fig) 
    return img_str

def init_viewport_width():
    if 'viewport_width' not in st.session_state:
        try:
            vw = streamlit_js_eval(js_expressions="window.innerWidth", key="viewport_width_js", want_output=True)
            if vw is not None: st.session_state.viewport_width = vw
        except Exception:
            st.session_state.viewport_width = None