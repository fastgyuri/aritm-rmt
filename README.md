# Arithmetic Modulation of Maximal Prime Gaps

Empirical analysis of maximal prime gaps, revealing positive scaling trends and contrast with Random Matrix Theory.

## Overview
This repository contains code and data for the research paper "Arithmetic Modulation of Maximal Prime Gaps: Empirical Scaling Laws and Contrast with Random Matrix Theory".

## Main Results
- Positive trend in normalized maximal gaps: R(p) = 0.556745 + 0.006321 ln(p)
- Logarithmic scaling in arithmetic progressions: β ∼ 0.45 + 0.28 log(q)
- Fundamental contrast with RMT predictions (empirical β > 0 vs RMT β < 0)
- Symmetric rebound structure with mean-reversion

## Quick Start
```bash
# Clone repository
git clone https://github.com/[username]/prime-gaps-research.git
cd prime-gaps-research

# Install dependencies
pip install -r requirements.txt

# Run complete analysis
python run_analysis.py

# Generate figures for paper
python generate_figures.py
