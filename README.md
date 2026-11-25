# Logistic Map Simulator: Visualizing Chaos and Predictability Limits

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19354735.svg)](https://doi.org/10.5281/zenodo.19354735) [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://logistic-map.streamlit.app)

This repository contains the source code for the **Logistic Map Simulator**, an interactive tool designed to explore **chaos theory**, **nonlinear dynamics**, and **predictability limits** in 1D dynamical systems.

### 🌐 <a href="https://logistic-map.streamlit.app" target="_blank">Launch the Live App on Streamlit</a>

## Overview
Unlike standard simulators, this app demonstrates the chaotic behavior of the **one-dimensional logistic equation** with a specific focus on **model error** and **initial-condition uncertainty**. It allows researchers and students to visualize how uncertainty propagates in chaotic models, leading to a "predictability horizon."

### Key Features
* **Interactive Logistic Map**: Adjust the growth parameter ($r$) to observe bifurcation and the transition to chaos.
* **Predictability Analysis**: Model the impact of **Monte Carlo** simulations on system variability.
* **Chaos Visualization**: Direct application of research regarding how model biases affect long-term forecasts.

## Running the App on Your Own Computer
The app needs Python 3.11 or later, as NumPy 2.3.4 and SciPy 1.16.3 do; these commands were checked with Python 3.14.0. On macOS, from the top folder of the repository:

```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

```bash
streamlit run app.py
```

The app opens in the browser at http://localhost:8501.

## Research & Citation
This tool was developed by **Dr. Altug Aksoy** (University of Miami / CIMAS) as a companion to the following research:

> **Aksoy, A. (2024).** *A Monte Carlo approach to understanding the impacts of initial-condition uncertainty, model uncertainty, and simulation variability on the predictability of chaotic systems: Perspectives from the one-dimensional logistic map.* **Chaos**, 34, 011102. <a href="https://doi.org/10.1063/5.0181705" target="_blank"><i>Access on Chaos</i></a>

**Citing the Software:**
If you utilize this codebase or interactive tool in your own work, please cite both the paper above and the specific software release via the Zenodo DOI provided at the top of this document.

## License
This code is released under the MIT License: see [LICENSE](LICENSE).

---

## ✉️ Contact & Support
If you have questions regarding the research or encounter technical issues with the simulator, please feel free to reach out:

* **Direct Inquiry**: <a href="mailto:aaksoy@miami.edu?subject=Question%20about%20Logistic%20Map%20Simulator" target="_blank">Click here to send an email inquiry</a>
* **Community**: <a href="https://github.com/aaksoy-umiami/logistic_map/discussions" target="_blank">Join the conversation in the Discussions tab!</a>
