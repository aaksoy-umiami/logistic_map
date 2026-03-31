import numpy as np
from scipy.stats import gaussian_kde
import time
import gc

"""
Logistic Map Simulator - Core Engine
Author: Altug Aksoy
Affiliation: CIMAS/Rosenstiel School, University of Miami & NOAA/AOML/HRD
Citation: Aksoy, A. (2024). Chaos, 34, 011102. https://doi.org/10.1063/5.0181705

Description:
    Backend logic for simulating the 1D logistic map. Handles deterministic trajectories,
    ensemble generation, statistical analysis, and bifurcation calculations.
    
    OPTIMIZATION NOTE: 
    Large data arrays are cast to np.float32 to reduce memory footprint in 
    Streamlit Session State.
"""

class LogisticMapSimulator:
    """Main logistic map simulation engine."""
    
    REGIME_DEFAULTS = {
        'Chaotic': {
            'param_slider_limits': [3.6, 4.0],
            'param_slider_value': 3.75,
            'init_slider_limits': [0, 1],
            'init_slider_value': 0.25,
        },
        'Deterministic (Single-Valued)': {
            'param_slider_limits': [0, 3],
            'param_slider_value': 1.5,
            'init_slider_limits': [0, 1],
            'init_slider_value': 0.5,
        },
        'Deterministic (Periodic)': {
            'param_slider_limits': [3, 3.56],
            'param_slider_value': 3.1,
            'init_slider_limits': [0, 1],
            'init_slider_value': 0.5,
        },
    }

    def __init__(self):
        pass

    def _step(self, x, r):
        """Core logistic map equation: x_next = r * x * (1 - x)"""
        return r * x * (1 - x)

    def run_simulation(self, r_true, x0_true, r_model, x0_model, num_steps, pred_thresh,
                       ensemble_enabled, ensemble_size, init_val_pert, param_pert, ensemble_stat):
        """
        Run the logistic map simulation (Vectorized).
        Calculates Truth, Deterministic Model, and Ensemble trajectories.
        """
        # Initialize result dictionary
        results = {
            'x_true': np.zeros(num_steps),
            'x_model_det': np.zeros(num_steps),
            'x_model_stat': np.zeros(num_steps),
            'ensemble_mean': np.zeros(num_steps),
            'ensemble_median': np.zeros(num_steps), 
            'ensemble_mode': np.zeros(num_steps),   
            'ensemble_std': np.zeros(num_steps),
            'x_absdiff_stat': np.zeros(num_steps),
            # Fields for separate trajectories from initial statistics
            'x_traj_mean': np.zeros(num_steps),
            'x_traj_median': np.zeros(num_steps),
            'x_traj_mode': np.zeros(num_steps),
        }
        
        # 1. Run Truth (Scalar)
        x_curr = x0_true
        for t in range(num_steps):
            results['x_true'][t] = x_curr
            x_curr = self._step(x_curr, r_true)

        # 2. Run Deterministic Model (Scalar)
        x_curr = x0_model
        for t in range(num_steps):
            results['x_model_det'][t] = x_curr
            x_curr = self._step(x_curr, r_model)

        if not ensemble_enabled:
            results['x_model_stat'] = results['x_model_det'].copy()
            results['x_absdiff_stat'] = np.abs(results['x_model_stat'] - results['x_true'])
            exceeds = np.where(results['x_absdiff_stat'] > pred_thresh)[0]
            results['pred_idx'] = exceeds[0] if len(exceeds) > 0 else num_steps - 1
            return results

        # 3. Run Ensemble (Vectorized)
        # Create vectors for r and x0
        r_ens = r_model + (np.random.randn(ensemble_size) * param_pert)
        x_ens = x0_model + (np.random.randn(ensemble_size) * init_val_pert)
        
        # Calculate Initial Statistics and run their specific trajectories
        init_mean = np.mean(x_ens)
        init_median = np.median(x_ens)
        
        # Simple mode estimation for initial cluster
        try:
            kde_init = gaussian_kde(x_ens)
            x_grid_init = np.linspace(x_ens.min(), x_ens.max(), 200)
            init_mode = x_grid_init[np.argmax(kde_init(x_grid_init))]
        except:
            init_mode = init_median

        # Storage for all members: Shape (num_steps, ensemble_size)
        x_full = np.zeros((num_steps, ensemble_size))
        
        # Trajectory holders
        xm, xmed, xmod = init_mean, init_median, init_mode
        
        # Time Loop
        for t in range(num_steps):
            # Store full ensemble state
            x_full[t, :] = x_ens
            
            # Store trajectory states
            results['x_traj_mean'][t] = xm
            results['x_traj_median'][t] = xmed
            results['x_traj_mode'][t] = xmod
            
            # Evolve everything
            x_ens = self._step(x_ens, r_ens)
            xm = self._step(xm, r_model)    # Deterministic evolution of mean
            xmed = self._step(xmed, r_model) # Deterministic evolution of median
            xmod = self._step(xmod, r_model) # Deterministic evolution of mode
            
        # MEMORY OPTIMIZATION: Convert large full history to float32
        results['x_model_full'] = x_full.T.astype(np.float32)

        # 4. Compute Statistics (Vectorized across axis 1)
        results['ensemble_mean'] = np.mean(x_full, axis=1)
        results['ensemble_median'] = np.median(x_full, axis=1)
        results['ensemble_std'] = np.std(x_full, axis=1)
        
        # Calculate 10th and 90th percentiles for consistency with the paper
        results['x_model_p10'] = np.percentile(x_full, 10, axis=1)
        results['x_model_p90'] = np.percentile(x_full, 90, axis=1)
        
        # Keep min/max just in case needed elsewhere
        results['x_model_min'] = np.min(x_full, axis=1)
        results['x_model_max'] = np.max(x_full, axis=1)
        
        results['x_spread'] = results['ensemble_std']

        # Calculate Ensemble Mode
        modes = np.zeros(num_steps)
        for t in range(num_steps):
            try:
                data = x_full[t, :]
                if np.std(data) < 1e-9:
                    modes[t] = np.mean(data)
                else:
                    kde = gaussian_kde(data)
                    x_grid = np.linspace(data.min(), data.max(), 200)
                    modes[t] = x_grid[np.argmax(kde(x_grid))]
            except:
                modes[t] = np.median(data)
        results['ensemble_mode'] = modes

        # Assign the user-selected stat to the main output variable
        if ensemble_stat == 'Mean':
            results['x_model_stat'] = results['ensemble_mean']
        elif ensemble_stat == 'Median':
            results['x_model_stat'] = results['ensemble_median']
        elif ensemble_stat == 'Mode':
            results['x_model_stat'] = results['ensemble_mode']

        # Difference stats
        results['x_absdiff_stat'] = np.abs(results['x_model_stat'] - results['x_true'])
        
        # Compute min/max/percentile error bounds
        diff_matrix = np.abs(x_full - results['x_true'][:, np.newaxis])
        
        # Calculate 10th and 90th percentiles for Error
        results['x_absdiff_p10'] = np.percentile(diff_matrix, 10, axis=1)
        results['x_absdiff_p90'] = np.percentile(diff_matrix, 90, axis=1)
        
        # Keep min/max for legacy support
        results['x_absdiff_min'] = np.min(diff_matrix, axis=1)
        results['x_absdiff_max'] = np.max(diff_matrix, axis=1)

        # Predictability Limit
        exceeds = np.where(results['x_absdiff_stat'] > pred_thresh)[0]
        results['pred_idx'] = exceeds[0] if len(exceeds) > 0 else num_steps - 1

        return results

    def compute_bifurcation_diagram(self, r_min=2.5, r_max=4.0, num_r=800,
                                   x_min=0.0, x_max=1.0, num_x=600,
                                   num_iterations=1000, iterations_discard=300):
        """Compute bifurcation diagram (Vectorized)"""
        start_time = time.time()
        
        # Create r vector
        r_vec = np.linspace(r_min, r_max, num_r)
        
        # Initialize x (can start random or uniform)
        x_vec = np.ones(num_r) * 0.5
        
        # Discard transients
        for _ in range(iterations_discard):
            x_vec = self._step(x_vec, r_vec)
            
        # Collect data
        r_list = []
        x_list = []
        
        for _ in range(num_iterations):
            x_vec = self._step(x_vec, r_vec)
            
            # Store data (filter for view window)
            mask = (x_vec >= x_min) & (x_vec <= x_max)
            if np.any(mask):
                r_list.append(r_vec[mask])
                x_list.append(x_vec[mask])
                
        # Flatten results
        if r_list:
            r_final = np.concatenate(r_list)
            x_final = np.concatenate(x_list)
        else:
            r_final = np.array([])
            x_final = np.array([])

        return {
            # MEMORY OPTIMIZATION: Cast to float32
            'r_array': r_final.astype(np.float32),
            'x_array': x_final.astype(np.float32),
            'computation_time': time.time() - start_time,
            'num_points': len(r_final)
        }

    def compute_bifurcation_diagram_with_density(self, r_min, r_max, num_r, x_min, x_max, num_x, num_iterations, iterations_discard):
        """Vectorized Bifurcation with Density Matrix"""
        
        # 1. Compute raw scatter points
        res = self.compute_bifurcation_diagram(r_min, r_max, num_r, x_min, x_max, num_x, num_iterations, iterations_discard)
        
        start_time = time.time() 
        
        # Create bins
        r_bins = np.linspace(r_min, r_max, num_r + 1)
        x_bins = np.linspace(x_min, x_max, num_x + 1)
        
        # 2. Compute 2D Histogram (Density)
        density_matrix, _, _ = np.histogram2d(
            res['r_array'], res['x_array'], bins=[r_bins, x_bins]
        )
        
        # MEMORY OPTIMIZATION: 
        # Explicitly delete the large scatter arrays to free RAM immediately.
        # We don't need them anymore because we have the density matrix.
        del res['r_array']
        del res['x_array']
        gc.collect() 

        return {
            # MEMORY OPTIMIZATION: Cast matrix to float32
            'density_matrix': density_matrix.T.astype(np.float32),
            'r_bins': r_bins.astype(np.float32),
            'x_bins': x_bins.astype(np.float32),
            'computation_time': res['computation_time'] + (time.time() - start_time)
            # NOTE: r_array and x_array are NOT returned here to save memory
        }
    
    def _compute_single_predictability_limit(self, r, model_bias, ic_bias, ensemble_size, n_iterations, threshold, metric='median'):
        """Compute single predictability limit (Averaged over attractor)."""
        
        # Sample x0_base uniformly to get global average
        abs_diffs_collection = np.zeros((ensemble_size, n_iterations))
        
        for m in range(ensemble_size):
            # Sample a new random location on the attractor for every member
            x0_base = np.random.uniform(0.1, 0.9) 
            
            # Series 1 (Truth): x0 + ic_bias * N(0,1)
            x0_truth = np.clip(x0_base + np.random.normal(0, ic_bias), 1e-10, 1-1e-10)
            
            # Series 2 (Model): x0 + ic_bias * 0.1 * N(0,1)
            x0_model = np.clip(x0_base + np.random.normal(0, ic_bias * 0.1), 1e-10, 1-1e-10)
            
            r_model = r * (1.0 + model_bias / r) if r != 0 else r
            
            # Run trajectories
            x_t = x0_truth
            x_m = x0_model
            
            for t in range(n_iterations):
                abs_diffs_collection[m, t] = np.abs(x_m - x_t)
                x_t = self._step(x_t, r)
                x_m = self._step(x_m, r_model)
                
        # Calculate metric across the ensemble
        if metric == 'mean':
            metric_curve = np.mean(abs_diffs_collection, axis=0)
        elif metric == 'median':
            metric_curve = np.median(abs_diffs_collection, axis=0)
        else: # mode
            metric_curve = np.median(abs_diffs_collection, axis=0)

        # Find threshold crossing
        exceeds = np.where(metric_curve > threshold)[0]
        return exceeds[0] if len(exceeds) > 0 else n_iterations
