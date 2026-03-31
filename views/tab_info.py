import streamlit as st
from datetime import datetime

def init_session_state():
    if 'info_sub_tab' not in st.session_state: 
        st.session_state.info_sub_tab = "about"

def render_sidebar():
    with st.sidebar:
        # === VERTICAL SPACER ===
        st.markdown("<br>" * 12, unsafe_allow_html=True)
    
        with st.container(border=True):
            st.markdown("### Information Guide")
            
            is_about = (st.session_state.info_sub_tab == 'about')
            is_intro = (st.session_state.info_sub_tab == 'intro')
            is_usage = (st.session_state.info_sub_tab == 'usage')
    
            # Button 1: About
            label_about = "About" + (" →" if is_about else "")
            type_about = 'primary' if is_about else 'secondary'
            
            if st.button(label_about, type=type_about, width='stretch', key="btn_info_about"):
                st.session_state.info_sub_tab = 'about'
                st.rerun()
    
            # Button 2: General Intro
            label_intro = "General Introduction to Chaos" + (" →" if is_intro else "")
            type_intro = 'primary' if is_intro else 'secondary'
            
            if st.button(label_intro, type=type_intro, width='stretch', key="btn_info_intro"):
                st.session_state.info_sub_tab = 'intro'
                st.rerun()
    
            # Button 3: How to Use
            label_usage = "How to Use This App" + (" →" if is_usage else "")
            type_usage = 'primary' if is_usage else 'secondary'
            
            if st.button(label_usage, type=type_usage, width='stretch', key="btn_info_usage"):
                st.session_state.info_sub_tab = 'usage'
                st.rerun()

def render_main():
    if st.session_state.info_sub_tab == 'intro':
        st.markdown("### General Introduction to Chaos")

        st.write(r"""
        #### Overview
        This **Logistic Map Simulator** demonstrates how **small initial-condition errors** grow 
        exponentially in chaotic systems, eventually exceeding our ability to make accurate predictions.

        #### Key Concepts
        - **Butterfly Effect:** Tiny differences in initial conditions lead to vastly different outcomes.
        - **Predictability Limit:** Beyond this point, the model becomes useless for specific forecasts.
        - **Ensemble Forecasting:** Multiple scenarios help quantify forecast uncertainty.
        - **Ensemble-Based vs. Single-Realization Simulations:** Simulations of the selected ensemble statistics will vary from one another as well as a single/deterministic realization.
        - **Practical Applications:** This insight is critical for weather, climate, and hurricane forecasting.

        #### The Logistic Map Equation

        The simulation uses the 1D logistic map:

        $$x_{i+1} = r x_i (1 - x_i)$$

        **Parameters:**
        - $i \geq 1$ : Iteration number of the simulation 
        - $r \in [0, 4]$ : Model parameter that controls system behavior (Chaotic, periodic, or fixed-point)
        - $x_i \in [0, 1]$ : System state at iteration $i$

        **Key Properties:**
        - For $r < 1$: Fixed point at $x = 0$
        - For $1 < r < 3$: Fixed point at $x = \frac{r-1}{r}$
        - For $r > 3$: Period-doubling bifurcations lead to chaos
        - At $r \approx 3.57$: Onset of chaos (Feigenbaum point)
        - For $r > 4$ or $r < 0$: Orbits escape to infinity
        """)

    elif st.session_state.info_sub_tab == 'usage':
        st.markdown("### How to Use This App")

        st.write(r"""
        #### General
        *Follow these steps to interact with the user interface.*

        1.  Choose functionality from the tabs on the top.
        2.  Adjust the relevant configuration options on the left.
        3.  Press the red "Run" button at the bottom for the changes to take effect.
            * Note that when configuration options are changed, the button turns red to indicate this.
        
        #### Bifurcation
        *Visualize the long-term behavior of the system across different parameter values.*

        1.  **Set Range:** Choose the minimum and maximum $r$ values (e.g., 2.5 to 4.0) to explore different dynamical regimes.
        2.  **Resolution:** Higher resolution provides sharper images but takes longer to compute.
        3.  **Density Plot:** Enable this to see a "heatmap" of where the system spends the most time, rather than just simple points. 
        4.  **Gamma:** Adjust the Gamma slider to change the contrast of the density plot, helping reveal faint structures.

        #### Dynamics
        *Simulate the evolution of the system over time.*
        
        1.  **Set Parameters:** In the sidebar, define the **Truth** (the "real" system) and the **Model** (your simulation of it).
            * *To simulate error:* Set the initial condition $x_0$ or model $r$ to be slightly different from the Truth.
        2.  **Ensemble Simulation:** Toggle this on to simulate a "cloud" of initial conditions rather than a single point. This helps visualize uncertainty growth.
            * All ensemble simulations are generated with random seeds and will result in slightly different "average" behavior for different runs.
            * "Average" ensemble behavior can be measured by the choice of the mean, median, or mode statistic of the ensemble.
        3.  **Visuals:**
            * **Time Series:** Shows the trajectory of $x$ over "time" (i.e., iteration number $i$).
            * **Absolute Error:** Shows the difference between Model and Truth (log scale).
            * **Attractor Geometry:** A state-space plot ($x_i$ vs $x_{i+\Delta}$) revealing the shape of the chaos where $\Delta$ is the lag parameter.
            * **Histograms:** Ensemble histograms help visualize how the ensemble diverges from Gaussianity over time.

        #### Predictability
        *Analyze the limit of prediction accuracy.*

        1.  **Select Parameters:** Choose specific values of $r$ (system behavior) and $\Delta r$ (Model Bias) from the sidebar checkboxes.
        2.  **Generate Plot:** Click the button to calculate the **Predictability Limit**.
        3.  **Interpretation:**
             * The resulting plot shows how the **Predictability Limit** (the time step where error becomes too large) decreases as initial condition uncertainty increases.
             * **Without model error**, Predictability Limit can be extended **indefinitely** by reducing the initial condition uncertainty/error.
             * The introduction of **model error** demonstrates how Predictability Limit **saturates** and cannot be improved further by lowering initial condition error alone.

        #### Comparative Error Growth
        *Compare how errors grow under different model and initial condition biases.*
        
        1.  **Reference Scenario:** Define the baseline system parameter ($r$), model error ($\Delta r$), and initial condition error ($\Delta x_0$).
        2.  **Additional Scenarios:** Add up to 5 alternative scenarios with different biases to compare against the reference.
        3.  **Ensemble Metric:** Choose whether to track the Median, Mean, or Mode of the ensemble error.
        4.  **Plot Settings:**
            * **Normalized Error:** Scales all curves by the reference error, useful for seeing relative growth rates (as in Fig. 4 of the paper).
            * **Absolute Error:** Shows the raw error magnitude on a log scale.
        5.  **Interpretation:**
            * This visualization helps identify which **error source** dominates **ensemble variability**.
            * In the **presence of model error**, lower initial error may lead to situations where **ensembles collapse**.
            * **Model error, therefore, imposes an additional burden on predictability** if maintaining sufficient ensemble variability is important.
        """)

    elif st.session_state.info_sub_tab == 'about':
        st.markdown("### About the Research")
        
        st.markdown("""
        **Summary:** This application serves as the interactive companion to the research article published in *Chaos*. 
        It demonstrates how **model error** impacts the predictability of chaotic systems distinct from 
        **initial-condition error**, using the logistic map as a proxy for complex geophysical models.
        """)

        st.markdown("---")

        col_cit1, col_cit2 = st.columns([0.6, 0.4])
        
        with col_cit1:
            st.markdown("#### 📄 Citation")
            st.markdown("""
            Aksoy, A. (2024). A Monte Carlo approach to understanding the impacts of initial-condition 
            uncertainty, model uncertainty, and simulation variability on the predictability of 
            chaotic systems. *Chaos*, 34, 011102.
            """)
            st.link_button("Read the Paper (DOI)", "https://doi.org/10.1063/5.0181705")

        with col_cit2:
            st.markdown("#### 📝 BibTeX (Use Copy to Add to Library)")
            st.code("""@article{Aksoy2024,
                  title={A Monte Carlo approach...},
                  author={Aksoy, Altug},
                  journal={Chaos},
                  volume={34},
                  number={1},
                  pages={011102},
                  year={2024},
                  publisher={AIP Publishing},
                  doi={10.1063/5.0181705}
                }""", language="latex")

        st.markdown("---")

        col_auth1, col_auth2 = st.columns(2)

        with col_auth1:
            st.markdown("#### 👤 Author")
            st.markdown("""
            **Altug Aksoy**, Scientist at *CIMAS/Rosenstiel School, Univ. of Miami* and *Hurricane Research Division/AOML, NOAA*
            
            📧 [aaksoy@miami.edu](mailto:aaksoy@miami.edu)  
            🌐 [NOAA/HRD Profile](https://www.aoml.noaa.gov/hrd/people/altugaksoy/)  
            🆔 [ORCID: 0000-0002-2335-7710](https://orcid.org/0000-0002-2335-7710)
            """)

        with col_auth2:
            st.markdown("#### 💻 Source Code")
            st.markdown("Explore the Python code behind this simulation on GitHub.")
            st.link_button("View GitHub Repository", "https://github.com/aaksoy-umiami/logistic_map")
            st.link_button("Cite Software (Zenodo DOI)", "https://doi.org/10.5281/zenodo.19354734")
            st.caption("Version 1.0 | License: MIT")

        st.markdown("---")

        st.markdown("#### ⚠️ Disclaimer & Usage")
        st.markdown("""
        **All rights reserved.** This application is intended for educational and research purposes only. 
        For academic use, please strictly adhere to the citation guidelines provided for both the code repository and the publication.

        **I would love to hear from you!** Please feel free to contact me at my email above for any suggestions or if you encounter issues/bugs. 
        
        *Note: This application is optimized for desktop environments. Users may experience layout or performance limitations on smaller mobile screens.*
        """)

    st.markdown("---")
    st.markdown(
        f"""
        <div style='text-align: center; color: #666; font-size: 12px;'>
            © {datetime.now().year} Altug Aksoy | University of Miami | 
            <a href="https://github.com/aaksoy-umiami/logistic_map/tree/main" target="_blank" style="color: #32b8c6; text-decoration: none;">View on GitHub</a>
        </div>
        """, 
        unsafe_allow_html=True
    )

def render():
    init_session_state()
    render_sidebar()
    render_main()
