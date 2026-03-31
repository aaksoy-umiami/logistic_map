import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import PowerNorm
from datetime import datetime
import gc
import numpy as np
from utils.helpers import get_bif_figsize, create_white_based_colormap, get_image_base64

def init_session_state():
    if 'bif_button_color' not in st.session_state: st.session_state.bif_button_color = 'normal'
    if 'bif_last_params' not in st.session_state: st.session_state.bif_last_params = None
    if 'bifurcation_computed' not in st.session_state: st.session_state.bifurcation_computed = False
    if 'bif_cached_img' not in st.session_state: st.session_state.bif_cached_img = None

def render_sidebar(simulator):
    with st.sidebar:
        with st.container(border=True):
            st.markdown("#### Bifurcation Parameters")
            col1, col2 = st.columns(2)
            with col1:
                r_min_bif = st.number_input("r min", value=2.5, step=0.1, format="%.2f")
            with col2:
                r_max_bif = st.number_input("r max", value=4.0, step=0.1, format="%.2f")
            
            x0_bif = st.slider("x₀ (initial condition)", 0.0, 1.0, value=0.5, step=0.01)
            transient_iters = st.number_input("Transient Iterations to Skip", value=200, min_value=50, max_value=500, step=50)
            plot_iters = st.number_input("Plot Number of Iteration Ater Transient", value=1000, min_value=500, max_value=5000, step=100)
        
        with st.container(border=True):
            st.markdown("#### Resolution & Display")
            resolution = st.number_input("Grid Resolution", value=1000, min_value=500, max_value=5000, step=100)
            show_density = True
            use_power_scale = True
            colormap = st.selectbox("Colormap", ["turbo", "jet", "rainbow"], index=0)
            gamma_value = st.slider("Gamma (Enhance low-density features)", min_value=0.1, max_value=1.0, value=0.2, step=0.05)
        
        bif_current_params = {
            'r_min': r_min_bif, 'r_max': r_max_bif, 'x0': x0_bif,
            'transient': transient_iters, 'plot': plot_iters, 'resolution': resolution,
            'density': show_density, 'colormap': colormap, 'power_scale': use_power_scale,
            'gamma': gamma_value
        }

        if st.session_state.bif_last_params != bif_current_params:
            st.session_state.bif_button_color = 'normal'
            st.session_state.bifurcation_computed = False
        
        bif_button_type = 'secondary' if st.session_state.bif_button_color == 'success' else 'primary'
        
        if st.button("▶️ Compute Bifurcation", type=bif_button_type, width='stretch'):
            with st.spinner("Computing bifurcation diagram..."):
                st.session_state.bif_cached_img = None 
                gc.collect()

                if show_density:
                    bifurcation_data = simulator.compute_bifurcation_diagram_with_density(
                        r_min=r_min_bif, r_max=r_max_bif, num_r=resolution, x_min=0.0, x_max=1.0, num_x=resolution,
                        num_iterations=plot_iters, iterations_discard=transient_iters
                    )
                else:
                    bifurcation_data = simulator.compute_bifurcation_diagram(
                        r_min=r_min_bif, r_max=r_max_bif, num_r=resolution, x_min=0.0, x_max=1.0, num_x=resolution,
                        num_iterations=plot_iters, iterations_discard=transient_iters
                    )
                
                st.session_state.bifurcation_data = bifurcation_data
                st.session_state.bifurcation_params_used = bif_current_params.copy()
                st.session_state.bifurcation_computed = True
                st.session_state.bif_last_params = bif_current_params
                st.session_state.bif_button_color = 'success'
                st.session_state.bif_figure_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.rerun()

def render_main():
    if st.session_state.bifurcation_computed:
        if st.session_state.bif_cached_img is not None:
            img_base64 = st.session_state.bif_cached_img
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
            st.markdown(f'<a href="data:image/png;base64,{img_base64}" download="bifurcation_diagram_{timestamp}.png"><img src="data:image/png;base64,{img_base64}" style="width:100%"/></a>', unsafe_allow_html=True)
        else:
            fig_bif, ax_bif = plt.subplots(figsize=get_bif_figsize(), constrained_layout=True)
            data = st.session_state.bifurcation_data
            params_used = st.session_state.get('bifurcation_params_used', {})
            
            show_density_used = params_used.get('density', True)
            colormap_used = params_used.get('colormap', 'turbo')
            use_power_scale_used = params_used.get('power_scale', True)
            gamma_used = params_used.get('gamma', 0.2)
            
            if show_density_used and 'density_matrix' in data:
                custom_cmap = create_white_based_colormap(colormap_used)
                density_data = data['density_matrix'].copy()
                density_data_nonzero = density_data[density_data > 0]
                
                if len(density_data_nonzero) > 0 and use_power_scale_used:
                    vmin = np.percentile(density_data_nonzero, 1)
                    vmax = np.percentile(density_data_nonzero, 99.5)
                    density_masked = np.ma.masked_where(density_data <= 0, density_data)
                    norm = PowerNorm(gamma=gamma_used, vmin=vmin, vmax=vmax)
                    im = ax_bif.imshow(density_masked, extent=[data['r_bins'][0], data['r_bins'][-1], data['x_bins'][0], data['x_bins'][-1]], origin='lower', aspect='auto', cmap=custom_cmap, norm=norm, interpolation='bilinear')
                    cbar = plt.colorbar(im, ax=ax_bif, label=f'Density (Power Scale γ={gamma_used:.2f})')
                else:
                    im = ax_bif.imshow(density_data, extent=[data['r_bins'][0], data['r_bins'][-1], data['x_bins'][0], data['x_bins'][-1]], origin='lower', aspect='auto', cmap=custom_cmap, interpolation='bilinear')
                    cbar = plt.colorbar(im, ax=ax_bif, label='Density')
                cbar.ax.tick_params(labelsize=10)
            else:
                ax_bif.plot(data['r_array'], data['x_array'], ',', color='#32b8c6', alpha=0.5, markersize=1)
            
            ax_bif.set_xlim(params_used.get('r_min', 2.5), params_used.get('r_max', 4.0))
            ax_bif.set_ylim(0, 1)
            ax_bif.set_xlabel('r (Model Parameter)', fontsize=13, fontweight='bold')
            ax_bif.set_ylabel('x (Time Series)', fontsize=13, fontweight='bold')
            title_suffix = f" (Power Scale γ={gamma_used:.2f})" if (show_density_used and use_power_scale_used) else ""
            ax_bif.set_title(f'Bifurcation Diagram{title_suffix}', fontsize=14, fontweight='bold')
            ax_bif.grid(True, alpha=0.2)
            
            img_base64 = get_image_base64(fig_bif)
            st.session_state.bif_cached_img = img_base64
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
            st.markdown(f'<a href="data:image/png;base64,{img_base64}" download="bifurcation_diagram_{timestamp}.png"><img src="data:image/png;base64,{img_base64}" style="width:100%"/></a>', unsafe_allow_html=True)

    else:
        st.image("app_welcome.png", width='stretch') 
        st.info("👆 This is a preview. Configure parameters in the sidebar and click **'▶️ Compute Bifurcation'** to generate your own interactive analysis.")

def render(simulator):
    init_session_state()
    render_sidebar(simulator)
    render_main()