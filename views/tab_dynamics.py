import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from datetime import datetime
from utils.helpers import get_plot_figsize, is_mobile_layout

def init_session_state():
    if 'button_color' not in st.session_state: st.session_state.button_color = 'normal'
    if 'simulation_ran' not in st.session_state: st.session_state.simulation_ran = False
    if 'results' not in st.session_state: st.session_state.results = None
    if 'last_sim_params' not in st.session_state: st.session_state.last_sim_params = None
    if 'iter_diff_value' not in st.session_state: st.session_state.iter_diff_value = 1
    if 'viz_show_mean' not in st.session_state: st.session_state.viz_show_mean = True
    if 'viz_show_median' not in st.session_state: st.session_state.viz_show_median = False
    if 'viz_show_mode' not in st.session_state: st.session_state.viz_show_mode = False
    if 'last_central_stat' not in st.session_state: st.session_state.last_central_stat = "Mean"
    if 'ens_spread_type' not in st.session_state: st.session_state.ens_spread_type = "10th-90th Percentiles"

def render_sidebar(simulator):
    with st.sidebar:
        with st.container(border=True):
            st.markdown("### Dynamical Regime Constraint for Parameter r")
            regime = st.selectbox(
                "Dynamical Regime",
                ["Chaotic", "Deterministic (Single-Valued)", "Deterministic (Periodic)"],
                help="Select the dynamical regime to explore", label_visibility="collapsed"
            )
            defaults = simulator.REGIME_DEFAULTS[regime]
        
        with st.container(border=True):
            st.markdown("### System Parameters (Truth and Modeled)")
            plus_style = "<div style='text-align: center; font-size: 20px; font-weight: bold; margin-top: -8px;'>+</div>"
            def param_label(text): st.markdown(f"<div style='font-size: 16px; padding-bottom: 12px;'>{text}</div>", unsafe_allow_html=True)
            
            param_label("r (truth)")
            col_r1, col_r2, col_r3 = st.columns([0.55, 0.10, 0.35], gap="small", vertical_alignment="center")
            with col_r1: r_true_slider = st.slider("r_truth_hidden", float(defaults['param_slider_limits'][0]), float(defaults['param_slider_limits'][1]), float(defaults['param_slider_value']), 0.01, key="r_true_slider", label_visibility="collapsed")
            with col_r2: st.markdown(plus_style, unsafe_allow_html=True)
            with col_r3: r_true_adj = st.number_input("adj", 0.0, format="%.2e", step=0.0, key="r_true_adj", label_visibility="collapsed")
            r_true = r_true_slider + r_true_adj
            
            param_label("x₀ (truth)")
            col_x1, col_x2, col_x3 = st.columns([0.55, 0.10, 0.35], gap="small", vertical_alignment="center")
            with col_x1: x0_true_slider = st.slider("x0_truth_hidden", float(defaults['init_slider_limits'][0]), float(defaults['init_slider_limits'][1]), float(defaults['init_slider_value']), 0.01, key="x0_true_slider", label_visibility="collapsed")
            with col_x2: st.markdown(plus_style, unsafe_allow_html=True)
            with col_x3: x0_true_adj = st.number_input("adj", 0.0, format="%.2e", step=0.0, key="x0_true_adj", label_visibility="collapsed")
            x0_true = x0_true_slider + x0_true_adj
            
            param_label("r (model)")
            col_rm1, col_rm2, col_rm3 = st.columns([0.55, 0.10, 0.35], gap="small", vertical_alignment="center")
            with col_rm1: r_model_slider = st.slider("r_model_hidden", float(defaults['param_slider_limits'][0]), float(defaults['param_slider_limits'][1]), float(defaults['param_slider_value']), 0.01, key="r_model_slider", label_visibility="collapsed")
            with col_rm2: st.markdown(plus_style, unsafe_allow_html=True)
            with col_rm3: r_model_adj = st.number_input("adj", 0.0, format="%.2e", step=0.0, key="r_model_adj", label_visibility="collapsed")
            r_model = r_model_slider + r_model_adj
            
            param_label("x₀ (model)")
            col_xm1, col_xm2, col_xm3 = st.columns([0.55, 0.10, 0.35], gap="small", vertical_alignment="center")
            with col_xm1: x0_model_slider = st.slider("x0_model_hidden", float(defaults['init_slider_limits'][0]), float(defaults['init_slider_limits'][1]), float(defaults['init_slider_value']), 0.01, key="x0_model_slider", label_visibility="collapsed")
            with col_xm2: st.markdown(plus_style, unsafe_allow_html=True)
            with col_xm3: x0_model_adj = st.number_input("adj", 1e-5, format="%.2e", step=0.0, key="x0_model_adj", label_visibility="collapsed")
            x0_model = x0_model_slider + x0_model_adj
            
            st.markdown("") 
            num_steps = st.number_input("Number of Simulation Iterations/Steps (n)", 10, 1000, 100, 10)
        
        with st.container(border=True):
            st.markdown("### Predictability Limit")
            col_pt1, col_pt2, col_pt3 = st.columns([0.34, 0.12, 0.34], gap="small", vertical_alignment="center")
            with col_pt1: pred_mantissa = st.number_input("Assumed Limit", 1.0, 9.999, 1.0, 0.1, format="%.3f", key="pred_mantissa")
            with col_pt2: st.markdown("<div style='padding-top: 8px; text-align: center; font-size: 15px; font-weight: bold; '>x 10^</div>", unsafe_allow_html=True)
            with col_pt3: 
                st.markdown("<div style='padding-top: 25px;'></div>", unsafe_allow_html=True)
                pred_exponent = st.number_input("Exponent", -6, 0, -1, 1, key="pred_exponent", label_visibility="collapsed")
            pred_thresh = pred_mantissa * (10 ** pred_exponent)

        with st.container(border=True):
            st.markdown("### Ensemble Settings")
            use_ensemble = st.toggle("Enable Ensemble Simulation", value=False)
            
            if use_ensemble:
                ens_size = st.number_input("Ensemble Size", 2, 500, 50, 1)
                central_stat = st.selectbox("Primary Statistic (for Main Plots)", ["Mean", "Median", "Mode"], index=0)

                st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
                ens_spread_type = st.radio("Ensemble Range Display", ["10th-90th Percentiles", "Min-Max Range"], index=0, key="ens_spread_type")

                # Force Active Metric to True
                if central_stat == 'Mean': st.session_state.viz_show_mean = True
                elif central_stat == 'Median': st.session_state.viz_show_median = True
                elif central_stat == 'Mode': st.session_state.viz_show_mode = True

                initval_pert = st.number_input("Initial Value Perturbation", 1e-10, 0.1, 1e-4, format="%.2e")
                param_pert = st.number_input("Parameter Perturbation", 0.0, 0.1, 0.0, format="%.2e")
                
                st.markdown("---")
                st.markdown("**Detailed Analysis Settings**")
                st.markdown("<span style='font-size: 14px;'>Select Time Steps for Histograms:</span>", unsafe_allow_html=True)
                max_steps = num_steps 
                hist_t1 = st.slider("First Time Step Displayed", 1, max_steps, min(5, max_steps), key="hist_t1")
                hist_t2 = st.slider("Second Time Step Displayed", 1, max_steps, min(20, max_steps), key="hist_t2")
                hist_t3 = st.slider("Third Time Step Displayed", 1, max_steps, min(60, max_steps), key="hist_t3")

                st.markdown("<span style='font-size: 14px;'>Metrics to Overlay/Compare:</span>", unsafe_allow_html=True)
                col_m1, col_m2 = st.columns([0.35, 0.65])
                with col_m1:
                    show_ens_mean = st.checkbox("Ens. Mean", key="viz_show_mean", disabled=(central_stat == 'Mean'))
                    show_ens_median = st.checkbox("Ens. Median", key="viz_show_median", disabled=(central_stat == 'Median'))
                    show_ens_mode = st.checkbox("Ens. Mode", key="viz_show_mode", disabled=(central_stat == 'Mode'))
                with col_m2:
                    show_traj_mean = st.checkbox("Det. Traj. from Init. Mean", value=True, key="viz_show_traj_mean")
                    show_traj_median = st.checkbox("Det. Traj. from Init. Median", value=False, key="viz_show_traj_median")
                    show_traj_mode = st.checkbox("Det. Traj. from Init. Mode", value=False, key="viz_show_traj_mode")

                st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
                st.markdown("<span style='font-size: 14px;'>Plot the Kernel Density Estimate?</span>", unsafe_allow_html=True)
                show_kde_option = st.radio("Show KDE", ["Yes", "No"], index=0, horizontal=True, label_visibility="collapsed", key="viz_show_kde")

            else:
                ens_size = 1; initval_pert = 0.0; param_pert = 0.0; central_stat = "Mean"
                hist_t1, hist_t2, hist_t3 = 10, 30, 60
        
        with st.container(border=True):
            st.markdown("#### State-Space Settings")
            iter_diff = st.number_input("Lag Parameter", 1, 50, 1, 1)

        sim_params = {
            'r_true': r_true, 'r_model': r_model, 'x0_true': x0_true, 'x0_model': x0_model,
            'num_steps': num_steps, 'use_ensemble': use_ensemble, 'ens_size': ens_size,
            'init_val_pert': initval_pert if use_ensemble else 0.0,
            'param_pert': param_pert if use_ensemble else 0.0
        }
        
        if st.session_state.last_sim_params != sim_params:
            st.session_state.button_color = 'normal'
        
        button_type = 'secondary' if st.session_state.button_color == 'success' else 'primary'
        run_button = st.button("▶️ Run Simulation", type=button_type, width='stretch', key="run_sim_main")
        
        if run_button:
            with st.spinner('Running simulation...'):
                st.session_state.results = simulator.run_simulation(
                    r_true=r_true, x0_true=x0_true, r_model=r_model, x0_model=x0_model,
                    num_steps=num_steps, pred_thresh=pred_thresh, ensemble_enabled=use_ensemble,
                    ensemble_size=ens_size, init_val_pert=initval_pert, param_pert=param_pert,
                    ensemble_stat=central_stat
                )
                st.session_state.simulation_ran = True
                st.session_state.last_sim_params = sim_params
                st.session_state.dyn_runtime_vars = {
                    'use_ensemble': use_ensemble, 'central_stat': central_stat,
                    'pred_thresh': pred_thresh, 'iter_diff': iter_diff,
                    'r_true': r_true, 'r_model': r_model
                }
                st.session_state.button_color = 'success'
                st.session_state.figure_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.rerun()

def render_main():
    if st.session_state.simulation_ran and st.session_state.results is not None:
        results = st.session_state.results
        vars = st.session_state.dyn_runtime_vars
        use_ensemble = vars['use_ensemble']
        central_stat = vars['central_stat']
        pred_thresh = vars['pred_thresh']
        iter_diff = vars['iter_diff']
        r_true = vars['r_true']
        r_model = vars['r_model']

        if use_ensemble:
            stat_key = f'ensemble_{central_stat.lower()}'
            if stat_key not in results and 'x_model_full' in results:
                full_data = results['x_model_full']
                if central_stat == 'Median': results['ensemble_median'] = np.median(full_data, axis=0)
                elif central_stat == 'Mean': results['ensemble_mean'] = np.mean(full_data, axis=0)
            
            x_model_dynamic = results[stat_key] if stat_key in results else results['x_model_stat']
            if central_stat == 'Mode' and stat_key not in results:
                st.warning("⚠️ 'Mode' statistic not available in cached data. Please click 'Run Simulation' to compute it.")
        else:
            x_model_dynamic = results['x_model_det']
            
        abs_diff_dynamic = np.abs(x_model_dynamic - results['x_true'])
        exceeds_dynamic = np.where(abs_diff_dynamic > pred_thresh)[0]
        pred_idx_dynamic = exceeds_dynamic[0] if len(exceeds_dynamic) > 0 else len(results['x_true'])

        if is_mobile_layout():
            col_single, = st.columns(1)
            cols = [col_single, col_single, col_single, col_single]
        else:
            row1, = st.columns(1)
            row2, = st.columns(1)
            col3, col4 = st.columns(2)
            cols = [row1, row2, col3, col4]

        col_idx = 0
        time = np.arange(1, len(results['x_true']) + 1)
        
        # --- 1. TIME SERIES ---
        with cols[col_idx]:
            figsize_ts = (12, 4) if not is_mobile_layout() else get_plot_figsize()
            fig_ts, ax_ts = plt.subplots(figsize=figsize_ts, constrained_layout=True)

            if use_ensemble:
                if st.session_state.get('ens_spread_type', "10th-90th Percentiles") == "10th-90th Percentiles" and 'x_model_p10' in results:
                    ax_ts.fill_between(time, results['x_model_p10'], results['x_model_p90'], alpha=0.2, color='gray', label='Ens. Range (10-90%)')
                else:
                    ax_ts.fill_between(time, results.get('x_model_min', results['x_model_stat']), results.get('x_model_max', results['x_model_stat']), alpha=0.2, color='gray', label='Ens. Range (Min-Max)')
            
            if 0 < pred_idx_dynamic < len(time):
                ax_ts.axvline(x=pred_idx_dynamic + 1, color='k', linestyle='--', linewidth=1.0, label=f'Pred Limit (t={pred_idx_dynamic + 1})', alpha=0.7)
                
            ax_ts.plot(time, results['x_true'], 'b-', linewidth=1.0, label='Truth', alpha=0.8)
            label_main = f'Model ({central_stat})' if use_ensemble else 'Model (Single)'
            ax_ts.plot(time, x_model_dynamic, color='orange', linewidth=1.0, label=label_main, alpha=0.8)
            
            ax_ts.set_xlabel('Time Step (i)', fontsize=10, fontweight='bold')
            ax_ts.set_title(f'State Time Series', fontsize=11, fontweight='bold')
            ax_ts.set_ylim([-0.05, 1.3])
            ax_ts.grid(True, alpha=0.3)
            ax_ts.legend(fontsize=9, ncol=2)
            st.pyplot(fig_ts)
            plt.close(fig_ts) 
            col_idx += 1
        
        # --- 2. TIME SERIES DIFF ---
        with cols[col_idx]:
            figsize_ts = (12, 4) if not is_mobile_layout() else get_plot_figsize()
            fig_tsd, ax_tsd = plt.subplots(figsize=figsize_ts, constrained_layout=True)

            if use_ensemble:
                if st.session_state.get('ens_spread_type', "10th-90th Percentiles") == "10th-90th Percentiles" and 'x_absdiff_p10' in results:
                    ax_tsd.fill_between(time, np.maximum(results['x_absdiff_p10'], 1e-16), np.maximum(results['x_absdiff_p90'], 1e-16), alpha=0.2, color='gray', label='Ens. Range (10-90%)')
                else:
                    ax_tsd.fill_between(time, np.maximum(results.get('x_absdiff_min', 1e-16), 1e-16), np.maximum(results.get('x_absdiff_max', 1e-16), 1e-16), alpha=0.2, color='gray', label='Ens. Range (Min-Max)')
            
            ax_tsd.axhline(y=pred_thresh, color='b', linestyle='--', linewidth=1.0, label=' Error Threshold', alpha=0.7)
            if 0 < pred_idx_dynamic < len(time):
                ax_tsd.axvline(x=pred_idx_dynamic + 1, color='k', linestyle='--', linewidth=1.0, label=f'Predictability Limit (t={pred_idx_dynamic + 1})', alpha=0.7)
                
            if pred_idx_dynamic > 0: ax_tsd.semilogy(time[:pred_idx_dynamic+1], abs_diff_dynamic[:pred_idx_dynamic+1], 'g-', linewidth=1.0, label='Good Predictability', alpha=0.8)
            if pred_idx_dynamic < len(time) - 1: ax_tsd.semilogy(time[pred_idx_dynamic:], abs_diff_dynamic[pred_idx_dynamic:], 'r-', linewidth=1.0, label='Poor Predictability', alpha=0.8)
            
            ax_tsd.set_xlabel('Time Step (i)', fontsize=10, fontweight='bold')
            ax_tsd.set_title('Absolute Error (Model-Truth)', fontsize=11, fontweight='bold')
            ax_tsd.grid(True, alpha=0.3, which='both')
            ax_tsd.legend(fontsize=9, ncol=2)
            st.pyplot(fig_tsd)
            plt.close(fig_tsd) 
            col_idx += 1
        
        # --- 3. STATE-SPACE ---
        with cols[col_idx]:
            fig_ss, ax_ss = plt.subplots(figsize=get_plot_figsize(), constrained_layout=True)
            xpara = np.linspace(0, 1, 200)
            ypara_truth = xpara.copy()
            ypara_model = xpara.copy()
            for _ in range(iter_diff):
                ypara_truth = r_true * ypara_truth * (1 - ypara_truth)
                ypara_model = r_model * ypara_model * (1 - ypara_model)
                
            ax_ss.plot([0, 1], [0, 1], 'k--', alpha=0.3, zorder=1)
            ax_ss.plot(xpara, ypara_truth, 'b-', alpha=0.5, linewidth=1, label=f"Truth (r={r_true:.2f})", zorder=1)
            ax_ss.plot(xpara, ypara_model, color='orange', linestyle='--', alpha=0.6, linewidth=1, label=f"Model (r={r_model:.2f})", zorder=1)

            x_n = x_model_dynamic[:-iter_diff]
            x_n1 = x_model_dynamic[iter_diff:]
            colors = np.arange(len(x_n))
            scatter = ax_ss.scatter(x_n, x_n1, c=colors, cmap='turbo', s=25, alpha=0.7, edgecolors='black', label=f'Ens. Metric: {central_stat}', zorder=2)
            plt.colorbar(scatter, ax=ax_ss).set_label('Iteration Number', fontsize=10)

            if use_ensemble:
                if st.session_state.get('viz_show_mean', False) and central_stat != 'Mean': ax_ss.plot(results.get('ensemble_mean', results['x_model_stat'])[:-iter_diff], results.get('ensemble_mean', results['x_model_stat'])[iter_diff:], 'o', color='orange', markersize=3, alpha=0.6, label='Ens. Traj. (Mean)', zorder=3)
                if st.session_state.get('viz_show_median', False) and central_stat != 'Median': ax_ss.plot(results.get('ensemble_median', results['x_model_stat'])[:-iter_diff], results.get('ensemble_median', results['x_model_stat'])[iter_diff:], 'o', color='purple', markersize=3, alpha=0.6, label='Ens. Traj. (Median)', zorder=3)
                if st.session_state.get('viz_show_mode', False) and central_stat != 'Mode' and 'ensemble_mode' in results: ax_ss.plot(results['ensemble_mode'][:-iter_diff], results['ensemble_mode'][iter_diff:], 'o', color='deeppink', markersize=3, alpha=0.6, label='Ens. Traj. (Mode)', zorder=3)
                if st.session_state.get('viz_show_traj_mean', False): ax_ss.plot(results['x_traj_mean'][:-iter_diff], results['x_traj_mean'][iter_diff:], 'o', color='green', markersize=3, alpha=0.6, label='Det. Traj. (Mean)', zorder=3)
                if st.session_state.get('viz_show_traj_median', False): ax_ss.plot(results['x_traj_median'][:-iter_diff], results['x_traj_median'][iter_diff:], 'o', color='blue', markersize=3, alpha=0.6, label='Det. Traj. (Median)', zorder=3)
                if st.session_state.get('viz_show_traj_mode', False): ax_ss.plot(results['x_traj_mode'][:-iter_diff], results['x_traj_mode'][iter_diff:], 'o', color='teal', markersize=3, alpha=0.6, label='Det. Traj. (Mode)', zorder=3)

            ax_ss.set_xlabel(r"$\mathbf{x_{i}}$", fontsize=12, fontweight='bold')
            ax_ss.set_ylabel(r"$\mathbf{x_{i+\Delta}}$", fontsize=12, fontweight='bold')
            ax_ss.set_title(f'Attractor Geometry (Δ={iter_diff})', fontsize=11, fontweight='bold')
            ax_ss.set_xlim([0, 1]); ax_ss.set_ylim([0, 1]); ax_ss.grid(True, alpha=0.3)
            ax_ss.legend(fontsize=8, loc='upper left', framealpha=0.9, ncol=2)
            st.pyplot(fig_ss)
            plt.close(fig_ss) 
            col_idx += 1
        
        # --- 4. STATE-SPACE DIFF ---
        with cols[col_idx]:
            fig_ssd, ax_ssd = plt.subplots(figsize=get_plot_figsize(), constrained_layout=True)
            diff_x_n = x_model_dynamic[:-iter_diff] - results['x_true'][:-iter_diff]
            diff_x_n1 = x_model_dynamic[iter_diff:] - results['x_true'][iter_diff:]
            ax_ssd.scatter(diff_x_n, diff_x_n1, c=np.arange(len(diff_x_n)), cmap='turbo', s=20, alpha=0.7, edgecolors='black')
            ax_ssd.axhline(0, color='k', linestyle='--', alpha=0.3); ax_ssd.axvline(0, color='k', linestyle='--', alpha=0.3)
            ax_ssd.set_xlabel(r"$\mathbf{\Delta x_{i}}$", fontsize=12, fontweight='bold')
            ax_ssd.set_ylabel(r"$\mathbf{\Delta x_{i+\Delta}}$", fontsize=12, fontweight='bold')
            ax_ssd.set_title(f'State-Space Difference (Δ={iter_diff})', fontsize=11, fontweight='bold')
            ax_ssd.grid(True, alpha=0.3); ax_ssd.set_xlim([-1, 1]); ax_ssd.set_ylim([-1, 1])
            st.pyplot(fig_ssd)
            plt.close(fig_ssd) 

        # === 5. ENSEMBLE ANALYSIS ===
        if use_ensemble and 'x_model_full' in results:
            fig_comp, ax_comp = plt.subplots(figsize=(12, 4), constrained_layout=True)
            ax_comp.plot(time, results['x_true'], 'k-', alpha=0.2, linewidth=2.0, label='Truth')
            if 0 < pred_idx_dynamic < len(time): ax_comp.axvline(x=pred_idx_dynamic + 1, color='k', linestyle='--', linewidth=1.0, label=f'Pred Limit (t={pred_idx_dynamic + 1})', alpha=0.7)
            
            if st.session_state.get('viz_show_mean', False): ax_comp.plot(time, results.get('ensemble_mean', results['x_model_stat']), color='orange', linewidth=1.0, label='Ens. Mean')
            if st.session_state.get('viz_show_median', False): ax_comp.plot(time, results.get('ensemble_median', results['x_model_stat']), color='purple', linewidth=1.0, label='Ens. Median')
            if st.session_state.get('viz_show_mode', False): ax_comp.plot(time, results.get('ensemble_mode', results['x_model_stat']), color='deeppink', linewidth=1.0, label='Ens. Mode')
            if st.session_state.get('viz_show_traj_mean', False): ax_comp.plot(time, results['x_traj_mean'], color='green', linestyle='--', linewidth=1.0, label='Det. From Mean')
            if st.session_state.get('viz_show_traj_median', False): ax_comp.plot(time, results['x_traj_median'], color='blue', linestyle='--', linewidth=1.0, label='Det. From Median')
            if st.session_state.get('viz_show_traj_mode', False): ax_comp.plot(time, results['x_traj_mode'], color='teal', linestyle='--', linewidth=1.0, label='Det. From Mode')
            
            ax_comp.set_xlabel('Time Step (i)', fontsize=10, fontweight='bold'); ax_comp.set_title(f'Ensemble Metrics vs. Deterministic Trajectories', fontsize=11, fontweight='bold')
            ax_comp.set_ylim(-0.05, 1.3); ax_comp.legend(loc='upper center', ncol=3, fontsize=9); ax_comp.grid(True, alpha=0.3)
            st.pyplot(fig_comp)
            plt.close(fig_comp) 
            
            # --- Histograms ---
            from matplotlib.ticker import MaxNLocator
            times = [st.session_state.get('hist_t1', 10), st.session_state.get('hist_t2', 30), st.session_state.get('hist_t3', 60)]
            fig_hist, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=False, constrained_layout=True)
            full_ens_data = results['x_model_full'] 
            
            for i, t_val in enumerate(times):
                ax = axes[i]
                idx = t_val - 1
                if idx < full_ens_data.shape[1]:
                    data_t = full_ens_data[:, idx]
                    truth_val = results['x_true'][idx]
                    
                    vals_to_include = [data_t, truth_val]
                    if st.session_state.get('viz_show_mean', False) and 'ensemble_mean' in results: vals_to_include.append(results['ensemble_mean'][idx])
                    if st.session_state.get('viz_show_median', False) and 'ensemble_median' in results: vals_to_include.append(results['ensemble_median'][idx])
                    
                    all_vals = np.concatenate([np.atleast_1d(v) for v in vals_to_include])
                    plot_min, plot_max = max(0.0, np.min(all_vals) - 0.05), min(1.0, np.max(all_vals) + 0.05)
                    
                    ax.hist(data_t, bins=30, range=(plot_min, plot_max), density=True, color='skyblue', edgecolor='white', alpha=0.7, label='Ens. Dist.' if i == 0 else None)
                    if st.session_state.get("viz_show_kde", "Yes") == "Yes":
                        try:
                            kde = gaussian_kde(data_t)
                            x_grid = np.linspace(plot_min, plot_max, 200)
                            ax.plot(x_grid, kde(x_grid), 'r-', linewidth=2, label='KDE' if i == 0 else None)
                        except: pass
                    
                    ax.axvline(truth_val, color='black', linewidth=1.0, linestyle='-', alpha=0.8, label='Truth' if i == 0 else None, zorder=5)
                    if st.session_state.get('viz_show_mean', False) and 'ensemble_mean' in results: ax.axvline(results['ensemble_mean'][idx], color='orange', linewidth=1.0, label='Ens. Mean' if i==0 else "")
                    
                    ax.set_xlabel('State Value Range', fontsize=10, fontweight='bold'); ax.set_title(f"Ens. Histogram at i={t_val}", fontweight='bold')
                    ax.grid(True, alpha=0.3); ax.set_xlim(plot_min, plot_max); ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
                    if i == 0: ax.legend(fontsize=8, loc='upper left', frameon=True, facecolor='white', framealpha=0.9, ncol=2)

            st.pyplot(fig_hist)
            plt.close(fig_hist) 

        elif use_ensemble and 'x_model_full' not in results:
            st.warning("⚠️ Ensemble simulation enabled. Please click **'▶️ Run Simulation'** to generate the ensemble data.")

    else:
        st.info("""**Configure parameters in the sidebar and click "▶️ Run Simulation"**""")

def render(simulator):
    init_session_state()
    render_sidebar(simulator)
    render_main()