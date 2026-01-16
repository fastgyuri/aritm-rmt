#!/usr/bin/env python3
"""
Main script to run complete prime gap analysis.
Generates all data, figures, and summary statistics.
"""

import sys
import os
import time
from datetime import datetime

# Add src directory to path - handle both script and interactive environments
try:
    # This works when running as a script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(script_dir, 'src')
except NameError:
    # This works in interactive environments like Jupyter/IPython
    script_dir = os.getcwd()
    src_dir = os.path.join(script_dir, 'src')

if os.path.exists(src_dir):
    sys.path.append(src_dir)
    print(f"Added {src_dir} to Python path")
else:
    print(f"Warning: src directory not found at {src_dir}")

from data_fetch import fetch_oeis_sequence, generate_primes_sieve
from analysis import analyze_record_gaps, analyze_rebounds
from progression_analysis import analyze_all_progressions
from rmt_simulation import run_rmt_simulations
from plotting import generate_all_figures

def main():
    print("=" * 70)
    print("PRIME GAPS RESEARCH - COMPLETE ANALYSIS")
    print("=" * 70)
    
    # Create directories if they don't exist
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('figures', exist_ok=True)
    
    # Timestamp for this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Step 1: Fetch and analyze record gaps
    print("\n1. FETCHING RECORD GAPS FROM OEIS...")
    start_time = time.time()
    
    gaps = fetch_oeis_sequence(5250, max_terms=200)  # A005250
    starts = fetch_oeis_sequence(101, max_terms=200)  # A000101
    
    print(f"   Fetched {len(gaps)} record gaps")
    print(f"   First: p={starts[0]}, g={gaps[0]}")
    print(f"   Last: p={starts[-1]}, g={gaps[-1]}")
    
    # Step 2: Analyze record gaps
    print("\n2. ANALYZING RECORD GAPS...")
    record_results = analyze_record_gaps(starts, gaps)
    
    # Save results
    import pandas as pd
    df_records = pd.DataFrame({
        'n': range(len(starts)),
        'p_n': starts,
        'g_n': gaps,
        'R_n': record_results['R_values']
    })
    df_records.to_csv(f'data/raw/record_gaps_{timestamp}.csv', index=False)
    
    # Step 3: Analyze rebounds
    print("\n3. ANALYZING REBOUNDS...")
    rebound_results = analyze_rebounds(record_results['R_values'], starts)
    
    df_rebounds = pd.DataFrame(rebound_results['rebounds'], 
                               columns=['idx', 'p_n', 'p_next', 'R_n', 'R_next', 'delta'])
    df_rebounds.to_csv(f'data/processed/rebounds_{timestamp}.csv', index=False)
    
    # Step 4: Analyze arithmetic progressions
    print("\n4. ANALYZING ARITHMETIC PROGRESSIONS...")
    print("   This may take several minutes...")
    
    # For testing, use smaller limit; for full analysis, use limit=10**9
    limit = 10**8  # 100 million for testing
    # limit = 10**9  # 1 billion for full analysis
    
    progression_results = analyze_all_progressions(max_q=30, limit=limit)
    
    # Save progression slopes
    slopes_df = pd.DataFrame(progression_results['slopes'])
    slopes_df.to_csv(f'data/processed/progression_slopes_{timestamp}.csv', index=False)
    
    # Step 5: Run RMT simulations
    print("\n5. RUNNING RMT SIMULATIONS...")
    rmt_results = run_rmt_simulations(matrix_sizes=[10, 20, 50, 100, 200])
    
    # Step 6: Generate all figures
    print("\n6. GENERATING FIGURES...")
    generate_all_figures(record_results, rebound_results, 
                         progression_results, rmt_results,
                         output_dir='figures')
    
    # Step 7: Print summary statistics
    print("\n7. SUMMARY STATISTICS")
    print("   " + "-" * 50)
    print(f"   Record gaps analyzed: {len(starts)}")
    print(f"   Global slope (β): {record_results['global_slope']:.6f} ± {record_results['slope_std_err']:.6f}")
    print(f"   R² for global trend: {record_results['r_squared']:.4f}")
    print(f"   Rebound count: {rebound_results['count']} ({rebound_results['percentage']:.1f}%)")
    print(f"   Progressions analyzed: {progression_results['total_progressions']}")
    print(f"   Progressions with β > 0: {progression_results['positive_count']} ({progression_results['positive_percentage']:.1f}%)")
    print(f"   Mean β for q=10: {progression_results.get('beta_q10', 'N/A')}")
    
    elapsed = time.time() - start_time
    print(f"\nANALYSIS COMPLETED IN {elapsed:.1f} SECONDS")
    print("=" * 70)
    
    # Generate summary markdown file
    with open(f'analysis_summary_{timestamp}.md', 'w') as f:
        f.write(f"""# Analysis Summary - {timestamp}

## Record Gaps
- Total: {len(starts)}
- Global slope: {record_results['global_slope']:.6f} ± {record_results['slope_std_err']:.6f}
- R²: {record_results['r_squared']:.4f}
- p-value: {record_results['p_value']:.2e}

## Rebounds
- Count: {rebound_results['count']}
- Percentage: {rebound_results['percentage']:.1f}%
- Mean amplitude: {rebound_results['mean_amplitude']:.6f}
- Largest: {rebound_results['max_amplitude']:.6f}

## Arithmetic Progressions
- Total: {progression_results['total_progressions']}
- β > 0: {progression_results['positive_count']} ({progression_results['positive_percentage']:.1f}%)
- β < 0: {progression_results['negative_count']} ({progression_results['negative_percentage']:.1f}%)

## Files Generated
1. data/raw/record_gaps_{timestamp}.csv
2. data/processed/rebounds_{timestamp}.csv
3. data/processed/progression_slopes_{timestamp}.csv
4. Figures in figures/ directory

""")
    
    print(f"\nSummary saved to: analysis_summary_{timestamp}.md")

if __name__ == "__main__":
    main()
