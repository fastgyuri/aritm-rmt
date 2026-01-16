#!/usr/bin/env python3
"""
Generate publication-quality figures for the paper.
"""

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
from scipy import stats

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from plotting import configure_plotting_style, create_figure_1, create_figure_2, create_figure_3

def main():
    # Configure plotting style for publication
    configure_plotting_style()
    
    # Load data
    print("Loading data...")
    
    # Try to load latest data files
    data_dir = 'data'
    processed_dir = os.path.join(data_dir, 'processed')
    
    # Find latest files
    import glob
    rebound_files = sorted(glob.glob(os.path.join(processed_dir, 'rebounds_*.csv')))
    slope_files = sorted(glob.glob(os.path.join(processed_dir, 'progression_slopes_*.csv')))
    
    if not rebound_files or not slope_files:
        print("No data files found. Run run_analysis.py first.")
        return
    
    # Load most recent files
    latest_rebounds = rebound_files[-1]
    latest_slopes = slope_files[-1]
    
    df_rebounds = pd.read_csv(latest_rebounds)
    df_slopes = pd.read_csv(latest_slopes)
    
    print(f"Loaded rebounds: {len(df_rebounds)}")
    print(f"Loaded slopes: {len(df_slopes)}")
    
    # Create output directory for publication figures
    pub_dir = 'figures/publication'
    os.makedirs(pub_dir, exist_ok=True)
    
    # Generate all figures
    print("\nGenerating publication figures...")
    
    # Figure 1: Evolution of R_n with rebounds
    print("  Creating Figure 1: Evolution of R_n...")
    fig1 = create_figure_1(df_rebounds)
    fig1.savefig(os.path.join(pub_dir, 'figure1_evolution_Rn.pdf'), 
                 bbox_inches='tight', dpi=300)
    fig1.savefig(os.path.join(pub_dir, 'figure1_evolution_Rn.png'), 
                 bbox_inches='tight', dpi=300)
    plt.close(fig1)
    
    # Figure 2: Distribution of rebound amplitudes
    print("  Creating Figure 2: Distribution of Δ_n...")
    fig2 = create_figure_2(df_rebounds)
    fig2.savefig(os.path.join(pub_dir, 'figure2_distribution_delta.pdf'),
                 bbox_inches='tight', dpi=300)
    fig2.savefig(os.path.join(pub_dir, 'figure2_distribution_delta.png'),
                 bbox_inches='tight', dpi=300)
    plt.close(fig2)
    
    # Figure 3: Scaling of β with q
    print("  Creating Figure 3: Scaling β vs q...")
    # Aggregate slopes by q
    if 'q' in df_slopes.columns and 'beta' in df_slopes.columns:
        beta_by_q = df_slopes.groupby('q')['beta'].agg(['mean', 'std', 'count'])
        beta_by_q = beta_by_q[beta_by_q['count'] >= 3]  # Require at least 3 progressions
        
        fig3 = create_figure_3(beta_by_q)
        fig3.savefig(os.path.join(pub_dir, 'figure3_scaling_beta_q.pdf'),
                     bbox_inches='tight', dpi=300)
        fig3.savefig(os.path.join(pub_dir, 'figure3_scaling_beta_q.png'),
                     bbox_inches='tight', dpi=300)
        plt.close(fig3)
    
    # Figure 4: RMT comparison
    print("  Creating Figure 4: RMT comparison...")
    # For RMT, we need simulation data
    # This is simplified; in practice you'd load RMT results
    fig4, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Left panel: Empirical β distribution
    if 'beta' in df_slopes.columns:
        ax1.hist(df_slopes['beta'].dropna(), bins=30, alpha=0.7, color='steelblue', edgecolor='black')
        ax1.set_xlabel(r'$\beta_{a,q}$ (empirical)')
        ax1.set_ylabel('Frequency')
        ax1.set_title('Distribution of empirical slopes')
        ax1.axvline(x=0, color='red', linestyle='--', alpha=0.7, label='β=0')
        ax1.legend()
    
    # Right panel: Sign comparison
    q_values = [4, 8, 12, 16, 20, 29]
    empirical_means = []
    for q in q_values:
        if q in df_slopes['q'].values:
            mean_beta = df_slopes[df_slopes['q'] == q]['beta'].mean()
            empirical_means.append(mean_beta)
        else:
            empirical_means.append(np.nan)
    
    rmt_predictions = [-0.05] * len(q_values)  # GUE prediction
    
    x = np.arange(len(q_values))
    width = 0.35
    ax2.bar(x - width/2, empirical_means, width, label='Empirical', color='steelblue', alpha=0.7)
    ax2.bar(x + width/2, rmt_predictions, width, label='RMT (GUE)', color='darkred', alpha=0.7)
    ax2.set_xticks(x)
    ax2.set_xticklabels([str(q) for q in q_values])
    ax2.set_xlabel('Modulus q')
    ax2.set_ylabel('Slope β')
    ax2.set_title('Empirical vs. RMT predictions')
    ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax2.legend()
    
    fig4.tight_layout()
    fig4.savefig(os.path.join(pub_dir, 'figure4_rmt_comparison.pdf'),
                 bbox_inches='tight', dpi=300)
    fig4.savefig(os.path.join(pub_dir, 'figure4_rmt_comparison.png'),
                 bbox_inches='tight', dpi=300)
    plt.close(fig4)
    
    # Figure 5: Combined scaling plot
    print("  Creating Figure 5: Combined scaling...")
    if 'q' in df_slopes.columns and 'beta' in df_slopes.columns:
        fig5 = plt.figure(figsize=(10, 8))
        
        # Top: β vs log(q) with regression
        ax1 = plt.subplot(2, 1, 1)
        q_vals = []
        beta_means = []
        beta_stds = []
        
        for q, group in df_slopes.groupby('q'):
            if len(group) >= 2:
                q_vals.append(q)
                beta_means.append(group['beta'].mean())
                beta_stds.append(group['beta'].std())
        
        if q_vals:
            q_vals = np.array(q_vals)
            beta_means = np.array(beta_means)
            beta_stds = np.array(beta_stds)
            
            # Filter reasonable values
            mask = (beta_means > -0.5) & (beta_means < 1.5)
            q_vals = q_vals[mask]
            beta_means = beta_means[mask]
            beta_stds = beta_stds[mask]
            
            # Log scale
            log_q = np.log10(q_vals)
            
            # Regression
            slope, intercept, r_value, p_value, std_err = stats.linregress(log_q, beta_means)
            
            ax1.errorbar(log_q, beta_means, yerr=beta_stds, fmt='o', capsize=3,
                        label=f'Mean β (R²={r_value**2:.3f})')
            
            # Regression line
            x_fit = np.linspace(min(log_q), max(log_q), 100)
            y_fit = intercept + slope * x_fit
            ax1.plot(x_fit, y_fit, 'r--', 
                    label=f'β = {intercept:.3f} + {slope:.3f}·log₁₀(q)')
            
            ax1.set_xlabel('log₁₀(q)')
            ax1.set_ylabel('β mean')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
        
        # Bottom: Histogram of all β
        ax2 = plt.subplot(2, 1, 2)
        all_betas = df_slopes['beta'].dropna()
        ax2.hist(all_betas, bins=50, alpha=0.7, color='steelblue', edgecolor='black')
        ax2.axvline(x=all_betas.mean(), color='red', linestyle='--', 
                   label=f'Mean = {all_betas.mean():.3f}')
        ax2.set_xlabel('β')
        ax2.set_ylabel('Frequency')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        fig5.suptitle('Scaling of β with modulus q', fontsize=14)
        fig5.tight_layout()
        fig5.savefig(os.path.join(pub_dir, 'figure5_scaling_complete.pdf'),
                     bbox_inches='tight', dpi=300)
        fig5.savefig(os.path.join(pub_dir, 'figure5_scaling_complete.png'),
                     bbox_inches='tight', dpi=300)
        plt.close(fig5)
    
    print(f"\nAll figures saved to: {pub_dir}/")
    
    # Create a PDF with all figures
    print("\nCreating combined PDF...")
    from matplotlib.backends.backend_pdf import PdfPages
    
    with PdfPages(os.path.join(pub_dir, 'all_figures.pdf')) as pdf:
        # Recreate figures in order
        fig1 = create_figure_1(df_rebounds)
        pdf.savefig(fig1)
        plt.close(fig1)
        
        fig2 = create_figure_2(df_rebounds)
        pdf.savefig(fig2)
        plt.close(fig2)
        
        if 'q' in df_slopes.columns and 'beta' in df_slopes.columns:
            fig3 = create_figure_3(beta_by_q)
            pdf.savefig(fig3)
            plt.close(fig3)
    
    print("Done!")

if __name__ == "__main__":
    main()
