# Gray Immunity Epidemiological Model

[![Journal of Biosciences](https://img.shields.io/badge/Journal%20of%20Biosciences-49%3A10%20(2024)-blue)](https://www.ias.ac.in/article/fulltext/jbsc/049/0010)
[![DOI](https://img.shields.io/badge/DOI-10.1007%2Fs12038--023--00382--y-green)](https://doi.org/10.1007/s12038-023-00382-y)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Official code and simulation repository for:

> **Epidemiology: Gray immunity model gives qualitatively different predictions**  
> Milind Watve, Himanshu Bhisikar, Rohini Kharate, and Srashti Bajpai  
> *Journal of Biosciences*, Volume 49, Article 10 (2024)  
> [Full Text (IAS)](https://www.ias.ac.in/article/fulltext/jbsc/049/0010) | [DOI: 10.1007/s12038-023-00382-y](https://doi.org/10.1007/s12038-023-00382-y)

---

## Overview

Conventional compartmental epidemiological models (such as SIR/SEIR) treat infection and immunity as binary variables. This repository implements an **individual-based stochastic model** that treats immunity as a continuous variable (**"gray immunity"**) and incorporates **small immunity effects (SIEs)**:

- **Cross-immunity** from other infections ($I_c$, $P_c$)
- **Subclinical exposures** ($I_{\text{sce}}$, $\text{SCE}_{50}$)
- **Gradual immunity decay** in the absence of repeated exposure ($I_d$)

Incorporating SIEs produces qualitatively different epidemiological predictions compared to classical compartmental models, including:
1. **Repeated infection waves** without requiring new viral variants.
2. **"Dwarf peaks"** — waves peaking and declining well before reaching the classical herd immunity threshold.
3. **Symmetric upward and downward slopes** in infection waves.
4. **Endemic states and unpredictable surges** after variable gaps.

---

## Repository Structure

```text
├── src/                        # Simulation & analysis modules
│   ├── __init__.py
│   ├── parameters.py           # ModelParameters dataclass
│   ├── simulation.py           # Vectorized individual-based stochastic simulator
│   ├── visualization.py        # Wave dynamics & immunity distribution plots
│   └── peak_extraction.py      # Empirical COVID-19 peak extraction (OWID data)
├── scripts/
│   └── run_experiments.py      # CLI for running simulations & saving outputs
├── data/                       # Empirical COVID-19 datasets (OWID)
├── Results/                    # Generated figures and parameter sweep results
├── requirements.txt
├── CITATION.cff
└── LICENSE
```

---

## Quickstart

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Simulation

Open [`main.py`](main.py) in your IDE, adjust the configuration constants at the top if desired, and click **Run** (or run `python main.py`). Outputs and plots are saved to `data/processed/`.

### 3. Use in Python

```python
import sys
sys.path.insert(0, "src")

from parameters import ModelParameters
from simulation import run_simulation
from visualization import plot_wave_dynamics

params = ModelParameters(N=5000, T=500, r=0.1, seed=42)
result = run_simulation(params)
plot_wave_dynamics(result, save_path="wave_dynamics.png")
```

---

## Project Timeline (2021–2024)

This project evolved over roughly six months in mid-to-late 2021 before its peer-reviewed publication:

- **May 2021 — Conceptualization:** Initial formulation of a non-compartmental, continuous-immunity epidemiological model (`Covid population immunity model`, `non compartmental model structure`).
- **June 2021 — Mathematical Formalization:** Parameterization and LaTeX model specification (`Details.tex`, `parameters`).
- **August 2021 — Simulation Sweeps & Manuscript Drafting:** Large-scale parameter sweeps across population sizes ($N = 5000, 10000$) and cross-immunity regimes ($0.0 \to 1.0$), alongside the first full manuscript draft (`gray immunity MS.docx`).
- **September 2021 — Empirical Validation:** Stabilized the simulation codebase (`COVID-stable`) and extracted empirical COVID-19 wave peaks from Our World in Data across India, China, the UK, Spain, Poland, Indonesia, and Ukraine.
- **October–November 2021 — Preprint Release:** Posted as a preprint (`doi:10.20944/preprints202109.0162.v2`).
- **January 2024 — Publication:** Published in *Journal of Biosciences*, Vol. 49, Article 10.

---

## Citation

If you use this code or model in your research, please cite:

```bibtex
@article{watve2024epidemiology,
  title={Epidemiology: Gray immunity model gives qualitatively different predictions},
  author={Watve, Milind and Bhisikar, Himanshu and Kharate, Rohini and Bajpai, Srashti},
  journal={Journal of Biosciences},
  volume={49},
  number={1},
  pages={10},
  year={2024},
  publisher={Springer},
  doi={10.1007/s12038-023-00382-y}
}
```
