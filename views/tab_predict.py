import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from utils.helpers import get_image_base64

def init_session_state():
    if 'pred_button_color' not in st.session_state: st.session_state.pred_button_color = 'normal'
    if 'pred_ensemble_metric' not in st.session_state: st.session_state.pred_ensemble_metric = 'median'
    if 'last_selected_r_indices' not in st.session_state: st.session_state.last_selected_r_indices = []
    if 'last_selected_mb_indices' not in st.session_state: st.session_state.last_selected_mb_indices = []
    if 'pred_last_params' not in st.session_state: st.session_state.pred_last_params = None
    if 'pred_cached_img' not in st.session_state: st.session_state.pred_cached_img = None
    if 'plot_pred_clicked' not in st.session_state: st.session_state.plot_pred_clicked = False

def render_sidebar():
    with st.sidebar:
        with st.container(border=True):
            st.markdown("### Predictability Analysis Controls")
            
            # Predictability data is pre-calculated and loaded in app.py
            cache = st.session_state.pred_data
            r_values = cache['r_values']
            model_bias_values = cache['model_bias_values']

            ensemble_metric = st.selectbox(
                "Ensemble Metric", ["mean", "median", "mode"],
                index=["mean", "median", "mode"].index(st.session_state.pred_ensemble_metric),
                help="Metric used to represent ensemble predictions", key="ensemble_metric_pred"
            )

            def section_label(text): st.markdown(f"<p style='font-size: 16px; margin-bottom: 0px;'>{text}</p>", unsafe_allow_html=True)

            st.markdown(""); section_label("Select model parameter (r) values:") 
            selected_r_indices = []
            r_cols = st.columns(2, gap="small", vertical_alignment="center")
            for i, r in enumerate(r_values):
                with r_cols[i % 2]:
                    if st.checkbox(f"r = {r:.3f}", value=(i == 0), key=f"r_check_{i}"):
                        selected_r_indices.append(i)

            st.markdown(""); section_label("Select model bias (Δr) values:") 
            selected_mb_indices = []
            mb_cols = st.columns(2, gap="small", vertical_alignment="center")
            for j, mb in enumerate(model_bias_values):
                with mb_cols[j % 2]:
                    if st.checkbox(f"Δr = {mb:.1e}", value=(j == 0), key=f"mb_check_{j}"):
                        selected_mb_indices.append(j)

            st.markdown("") 

            pred_current_params = {
                'ensemble_metric': ensemble_metric,
                'r_indices': selected_r_indices,
                'mb_indices': selected_mb_indices
            }
            
            if st.session_state.get('pred_last_params') != pred_current_params:
                st.session_state.pred_button_color = 'normal'
                st.session_state.plot_pred_clicked = False
            
            pred_button_type = 'secondary' if st.session_state.pred_button_color == 'success' else 'primary'

            plot_button = st.button("▶️ Generate Plot", type=pred_button_type, width='stretch', key="pred_plot_button")

            st.session_state.selected_r_indices = selected_r_indices
            st.session_state.selected_mb_indices = selected_mb_indices

            if plot_button:
                st.session_state.plot_pred_clicked = True 
                st.session_state.pred_cached_img = None  
                st.session_state.pred_last_params = pred_current_params
                st.session_state.pred_button_color = 'success'
                st.rerun() 

def render_main():
    if st.session_state.get('plot_pred_clicked', False):
        if st.session_state.pred_cached_img is not None:
            img_base64 = st.session_state.pred_cached_img
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
            st.markdown(f'<a href="data:image/png;base64,{img_base64}" download="predictability_limit_{timestamp}.png"><img src="data:image/png;base64,{img_base64}" style="width:100%"/></a>', unsafe_allow_html=True)
        else:
            selected_r_indices = st.session_state.get('selected_r_indices', [0])
            selected_mb_indices = st.session_state.get('selected_mb_indices', [0])
            y_min, y_max = st.session_state.get('pred_y_range', (0, 120))
            metric = st.session_state.get('pred_ensemble_metric', 'median')
            
            pred_data = st.session_state.pred_data
            r_vals = pred_data['r_values']
            ic_vals = pred_data['ic_bias_values']
            dr_vals = pred_data['model_bias_values']
            
            surf = pred_data['surface'][metric] if isinstance(pred_data['surface'], dict) else pred_data['surface']
            
            if selected_r_indices and selected_mb_indices:
                fig, ax = plt.subplots(figsize=(12, 6))
                
                num_dr = len(selected_mb_indices)
                if num_dr == 1: colors = ['#1f77b4']
                elif num_dr == 2: colors = ['#1f77b4', '#ff7f0e']
                elif num_dr == 3: colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
                elif num_dr == 4: colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
                elif num_dr == 5: colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
                else: colors = plt.cm.tab20(np.linspace(0, 1, num_dr))
                
                line_styles = ['-', '--', '-.', ':', (0, (3, 1, 1, 1))]

                for j_dr, i_dr in enumerate(selected_mb_indices):
                    for k_r, i_r in enumerate(selected_r_indices):
                        pred_limits = surf[i_r, i_dr, :]
                        pred_limits_reversed = pred_limits[::-1]
                        
                        linestyle = line_styles[k_r % len(line_styles)]
                        color = colors[j_dr] if isinstance(colors, list) else colors[j_dr]
                        
                        ax.plot(range(len(ic_vals)), pred_limits_reversed, linewidth=2.5, color=color, linestyle=linestyle)
                
                ax.set_xlabel('Initial Condition Uncertainty', fontsize=12, fontweight='bold')
                ax.set_ylabel('Predictability Limit', fontsize=12, fontweight='bold')
                ax.set_title(f'Predictability Limits (Ensemble Metric: {metric.capitalize()})', fontsize=14, fontweight='bold')
                ax.set_ylim(y_min, y_max)
                ax.grid(True, alpha=0.3)
                
                ax.set_xticks(range(0, len(ic_vals), max(1, len(ic_vals)//10)))
                tick_indices = ax.get_xticks().astype(int)
                ax.set_xticklabels([f'{ic_vals[len(ic_vals)-1-i]:.1e}' if i < len(ic_vals) else '' for i in tick_indices], rotation=45, ha='right')
                
                left_legend_handles = []
                for k_r, i_r in enumerate(selected_r_indices):
                    left_legend_handles.append(plt.Line2D([0], [0], color='gray', linewidth=2.5, linestyle=line_styles[k_r % len(line_styles)], label=f'r = {r_vals[i_r]:.2f}'))
                
                right_legend_handles = []
                for j_dr, i_dr in enumerate(selected_mb_indices):
                    color = colors[j_dr] if isinstance(colors, list) else colors[j_dr]
                    right_legend_handles.append(plt.Line2D([0], [0], color=color, linewidth=2.5, linestyle='-', label=f'Δr = {dr_vals[i_dr]:.1e}'))
                
                left_legend = ax.legend(handles=left_legend_handles, loc='upper left', fontsize=10, title='r Values', title_fontsize=10, frameon=True)
                left_legend.get_title().set_fontweight('bold')
                ax.add_artist(left_legend)
                
                right_legend = ax.legend(handles=right_legend_handles, loc='upper left', fontsize=10, title='Δr Values', title_fontsize=10, frameon=True, bbox_to_anchor=(0.125, 1.0))
                right_legend.get_title().set_fontweight('bold')
                
                ax.text(0.99, 0.02, f'© {datetime.now().year} Altug Aksoy', transform=ax.transAxes, fontsize=8, ha='right', va='bottom', style='italic', color='gray', bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))

                img_base64 = get_image_base64(fig)
                st.session_state.pred_cached_img = img_base64
                
                timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
                st.markdown(f'<a href="data:image/png;base64,{img_base64}" download="predictability_limit_{timestamp}.png"><img src="data:image/png;base64,{img_base64}" style="width:100%"/></a>', unsafe_allow_html=True)
            else:
                st.warning("⚠️ Please select at least one r/Δr combination in the sidebar.")
    else:
        st.info("""**Configure parameters in the sidebar and click "▶️ Generate Plot"**""")

def render():
    init_session_state()
    render_sidebar()
    render_main()