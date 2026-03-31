import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from utils.helpers import get_image_base64

def init_session_state():
    if 'fig4_ran' not in st.session_state: st.session_state.fig4_ran = False
    if 'fig4_data' not in st.session_state: st.session_state.fig4_data = None
    if 'fig4_cached_img' not in st.session_state: st.session_state.fig4_cached_img = None
    if 'fig4_last_params' not in st.session_state: st.session_state.fig4_last_params = None
    if 'sb_y_limit_norm' not in st.session_state: st.session_state.sb_y_limit_norm = 3
    if 'sb_y_limit_abs' not in st.session_state: st.session_state.sb_y_limit_abs = -10

def clear_fig4_cache():
    st.session_state.fig4_cached_img = None

def reset_fig4_ylimits():
    st.session_state.sb_y_limit_norm = 3 
    st.session_state.sb_y_limit_abs = -10
    st.session_state.fig4_cached_img = None 

def render_sidebar(simulator):
    with st.sidebar:
        with st.container(border=True):
            st.markdown("### System Parameter")
            r_ref_val = st.slider("Reference r", min_value=3.6, max_value=4.0, value=3.7, step=0.01, key="sb_r_ref")

        with st.container(border=True):
            st.markdown("### Reference (Base) Scenario")
            bias_options = [1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5]
            mod_bias_options = [0.0] + bias_options
            ref_mod_bias = st.select_slider("Reference Model Error (Δr)", options=mod_bias_options, value=1e-6, key="sb_ref_mod", format_func=lambda x: f"{x:.0e}" if x > 0 else "0.0")
            ref_ic_bias = st.select_slider("Reference Initial Error (Δx₀)", options=bias_options, value=1e-6, key="sb_ref_ic", format_func=lambda x: f"{x:.0e}")

        with st.container(border=True):
            st.markdown("### Additional Scenarios")
            num_additional = st.selectbox("Number of Additional Scenarios", [1, 2, 3, 4, 5], index=2, key="sb_num_samples")
            
            h1, h2 = st.columns(2)
            with h1: st.markdown("<div style='font-size:14px; font-weight:600'>Model Err. (Δr)</div>", unsafe_allow_html=True)
            with h2: st.markdown("<div style='font-size:14px; font-weight:600'>Initial Err. (Δx₀)</div>", unsafe_allow_html=True)

            scenario_inputs = []
            scenario_inputs.append({'mod': ref_mod_bias, 'ic': ref_ic_bias, 'color': 'black'})
            
            additional_defaults = [(2.5e-5, 1e-6), (7.5e-5, 1e-6), (7.5e-5, 5e-5), (1e-4, 1e-4), (1e-4, 1e-4)]
            colors_additional = ['purple', 'green', 'orange', '#1f77b4', '#d62728']
            
            for i in range(num_additional):
                c1, c2 = st.columns(2)
                def_mod, def_ic = additional_defaults[i] if i < len(additional_defaults) else (1e-4, 1e-4)
                
                with c1: s_mod = st.text_input(f"add_mod_hidden_{i}", value=f"{def_mod:.1e}", key=f"scen_mod_{i}", label_visibility="collapsed")
                with c2: s_ic = st.text_input(f"add_ic_hidden_{i}", value=f"{def_ic:.1e}", key=f"scen_ic_{i}", label_visibility="collapsed")
                
                scenario_inputs.append({'mod': float(s_mod), 'ic': float(s_ic), 'color': colors_additional[i % len(colors_additional)]})

        with st.container(border=True):
            st.markdown("### Ensemble Metric to Plot")
            fig4_metric = st.selectbox("Metric", ["Median", "Mean", "Mode"], index=0, key="sb_fig4_metric", label_visibility="collapsed")

        with st.container(border=True):
            st.markdown("### Plot Settings")
            st.markdown("#### Plot Type")
            fig4_plot_type = st.radio("Plot Type", ["Normalized Error", "Absolute Error"], index=0, key="sb_fig4_plot_type", on_change=reset_fig4_ylimits, label_visibility="collapsed")
            
            st.markdown("#### Plot Limits")
            col_ax1, col_ax2 = st.columns(2)
            with col_ax1:
                x_limit = st.number_input("X-Axis Limit (Steps)", min_value=20, max_value=500, value=60, step=10, key="sb_x_limit", on_change=clear_fig4_cache)
            with col_ax2:
                if fig4_plot_type == "Normalized Error":
                    y_limit_exp = st.number_input("Y-Axis Max (10^x)", min_value=0, max_value=5, step=1, key="sb_y_limit_norm", help="Set the upper limit exponent", on_change=clear_fig4_cache)
                else:
                    y_limit_exp = st.number_input("Y-Axis Min (10^x)", min_value=-16, max_value=-1, step=1, key="sb_y_limit_abs", help="Set the lower limit exponent", on_change=clear_fig4_cache)
            
        scen_tuple = tuple([(s['mod'], s['ic']) for s in scenario_inputs])
        current_fig4_params = {'r': r_ref_val, 'scenarios': scen_tuple, 'xlim': x_limit, 'metric': fig4_metric}
        
        if st.session_state.fig4_last_params != current_fig4_params:
            st.session_state.fig4_btn_color = 'primary'
        
        btn_type = 'secondary' if st.session_state.get('fig4_btn_color') == 'success' else 'primary'

        if st.button("▶️ Run Comparative Analysis", type=btn_type, width='stretch', on_click=reset_fig4_ylimits):
            progress_bar = st.progress(0, text="Initializing simulation...")
            st.session_state.fig4_cached_img = None 
            
            r_base = r_ref_val
            steps = x_limit 
            ens_n = 25 
            thresh = 0.1
            ic_list = np.linspace(0.2, 0.8, 5) 
            
            sim_results = []; scenarios_to_plot = []; ref_res = None
            total_steps = len(scenario_inputs) * len(ic_list)
            current_step_count = 0
            
            for i, s in enumerate(scenario_inputs):
                accum_stat = np.zeros(steps); accum_p10 = np.zeros(steps); accum_p90 = np.zeros(steps)
                
                for x_start in ic_list:
                    current_step_count += 1
                    progress_bar.progress(int(current_step_count / total_steps * 100), text=f"Simulating Scenario {i+1}/{len(scenario_inputs)} (IC={x_start:.2f})")
                    
                    res = simulator.run_simulation(
                        r_true=r_base, x0_true=x_start, r_model=r_base + s['mod'], x0_model=x_start + s['ic'],
                        num_steps=steps, pred_thresh=thresh, ensemble_enabled=True, ensemble_size=ens_n,
                        init_val_pert=s['ic'], param_pert=0.0, ensemble_stat=fig4_metric
                    )
                    
                    accum_stat += res['x_absdiff_stat'][:steps]
                    accum_p10 += res.get('x_absdiff_p10', np.zeros(steps))[:steps]
                    accum_p90 += res.get('x_absdiff_p90', np.zeros(steps))[:steps]

                avg_res = {'x_absdiff_stat': accum_stat / len(ic_list), 'x_absdiff_p10': accum_p10 / len(ic_list), 'x_absdiff_p90': accum_p90 / len(ic_list)}

                if i == 0: ref_res = avg_res
                sim_results.append(avg_res)
                scenarios_to_plot.append({'ic': s['ic'], 'mod': s['mod'], 'color': s['color'], 'label': f"IC={s['ic']:.1e}, Δr={s['mod']:.1e}"})

            progress_bar.empty()

            st.session_state.fig4_data = {'ref': ref_res, 'scenarios': scenarios_to_plot, 'results': sim_results, 'params': current_fig4_params, 'timestamp': datetime.now()}
            st.session_state.fig4_ran = True
            st.session_state.fig4_last_params = current_fig4_params
            st.session_state.fig4_btn_color = 'success'
            st.rerun()

def render_main():
    if st.session_state.get('fig4_ran', False) and 'fig4_data' in st.session_state:
        if st.session_state.fig4_cached_img is not None:
            img_base64 = st.session_state.fig4_cached_img
            st.markdown(f'<img src="data:image/png;base64,{img_base64}" style="width:100%"/>', unsafe_allow_html=True)
        else:
            data = st.session_state.fig4_data
            plot_type = st.session_state.get("sb_fig4_plot_type", "Normalized Error")
            r_used = data['params']['r']
            metric_used = data['params'].get('metric', 'Median')
            user_xlim = data['params'].get('xlim', 60)
            user_ylim_exp = st.session_state.get("sb_y_limit_norm", 3) if plot_type == "Normalized Error" else st.session_state.get("sb_y_limit_abs", -10)
            
            fig4, ax4 = plt.subplots(figsize=(10, 6))
            steps = user_xlim 
            time_axis = np.arange(1, steps + 1)
            thresh = 0.1
            
            ref_curve = np.maximum(data['ref']['x_absdiff_stat'][:steps], 1e-16)
            
            if plot_type == "Normalized Error":
                ax4.plot(time_axis, thresh / ref_curve, 'k--', linewidth=1.5, label='Error Threshold', alpha=0.8)
                for i, s in enumerate(data['scenarios']):
                    res = data['results'][i]
                    norm_curve = res['x_absdiff_stat'][:steps] / ref_curve
                    ax4.plot(time_axis, norm_curve, color=s['color'], linewidth=2.0, alpha=0.8, label=s['label'])
                    
                    if 'x_absdiff_p10' in res:
                        ax4.plot(time_axis, (res['x_absdiff_p10'][:steps]) / ref_curve, color=s['color'], linewidth=0.5, alpha=0.4)
                        ax4.plot(time_axis, (res['x_absdiff_p90'][:steps]) / ref_curve, color=s['color'], linewidth=0.5, alpha=0.4)
                
                ax4.set_ylabel(rf"Normalized Error ({metric_used}, $\Delta / \Delta_{{ref}}$)", fontsize=12, fontweight='bold')
                ax4.set_title(f"Comparative Error Growth | r={r_used:.2f}", fontweight='bold')
                ax4.set_ylim(bottom=0.01, top=10**user_ylim_exp)
                legend_loc = 'upper right'
            else:
                ax4.axhline(thresh, color='k', linestyle='--', linewidth=1.5, label='Threshold (0.1)')
                for i, s in enumerate(data['scenarios']):
                    res = data['results'][i]
                    ax4.plot(time_axis, res['x_absdiff_stat'][:steps], color=s['color'], linewidth=2.0, alpha=0.8, label=s['label'])
                    if 'x_absdiff_p10' in res:
                        ax4.plot(time_axis, res['x_absdiff_p10'][:steps], color=s['color'], linewidth=0.5, alpha=0.4)
                        ax4.plot(time_axis, res['x_absdiff_p90'][:steps], color=s['color'], linewidth=0.5, alpha=0.4)

                ax4.set_ylabel(f"Absolute Error ({metric_used})", fontsize=12, fontweight='bold')
                ax4.set_title(f"Absolute Error Growth Comparison | r={r_used:.2f}", fontweight='bold')
                ax4.set_ylim(bottom=10**user_ylim_exp, top=2.0)
                legend_loc = 'lower right'

            ax4.set_yscale('log'); ax4.set_xlabel("Iteration Step", fontsize=12, fontweight='bold')
            ax4.grid(True, which="both", alpha=0.3); ax4.set_xlim(1, steps)
            ax4.plot([], [], color='k', linewidth=0.5, label='10th/90th Percentiles')
            ax4.legend(loc=legend_loc, fontsize=9, framealpha=0.9)
            cp_x, cp_ha = (0.99, 'right') if plot_type == "Normalized Error" else (0.02, 'left')
            ax4.text(cp_x, 0.02, f'© {datetime.now().year} Altug Aksoy', transform=ax4.transAxes, fontsize=8, ha=cp_ha, va='bottom', style='italic', color='gray', bbox=dict(facecolor='white', alpha=0.5, edgecolor='none'))
            
            img_base64 = get_image_base64(fig4)
            st.session_state.fig4_cached_img = img_base64
            st.markdown(f'<img src="data:image/png;base64,{img_base64}" style="width:100%"/>', unsafe_allow_html=True)
    else:
        st.info("Configure settings in the sidebar and click **▶️ Run Comparative Analysis**")

def render(simulator):
    init_session_state()
    render_sidebar(simulator)
    render_main()