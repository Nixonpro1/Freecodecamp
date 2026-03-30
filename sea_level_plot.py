import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

def draw_sea_level_plot():
    # 1. Import data from epa-sea-level.csv
    df = pd.read_csv('epa-sea-level.csv')
    
    # 2. Create scatter plot using Year vs CSIRO Adjusted Sea Level
    fig, ax = plt.subplots(figsize=(12, 8))
    
    ax.scatter(df['Year'], df['CSIRO Adjusted Sea Level'], 
               color='blue', alpha=0.6, s=20, label='Historical Data')
    
    # 3. First line of best fit using all data (1880-2014)
    slope_all, intercept_all, r_value_all, p_value_all, std_err_all = \
        linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    
    # Generate x values from 1880 to 2050
    years_future = np.arange(1880, 2051, 1)
    sea_level_pred_all = slope_all * years_future + intercept_all
    
    # Plot the first line
    ax.plot(years_future, sea_level_pred_all, 
            color='red', linewidth=2, linestyle='-',
            label=f'Linear Fit (1880-2014): y = {slope_all:.4f}x + {intercept_all:.2f}')
    
    # 4. Second line of best fit using data from 2000 onward
    df_recent = df[df['Year'] >= 2000]
    slope_recent, intercept_recent, r_value_recent, p_value_recent, std_err_recent = \
        linregress(df_recent['Year'], df_recent['CSIRO Adjusted Sea Level'])
    
    # Generate x values from 2000 to 2050
    years_recent_future = np.arange(2000, 2051, 1)
    sea_level_pred_recent = slope_recent * years_recent_future + intercept_recent
    
    # Plot the second line
    ax.plot(years_recent_future, sea_level_pred_recent, 
            color='green', linewidth=2, linestyle='--',
            label=f'Linear Fit (2000-2014): y = {slope_recent:.4f}x + {intercept_recent:.2f}')
    
    # Add prediction markers at 2050
    prediction_all = slope_all * 2050 + intercept_all
    prediction_recent = slope_recent * 2050 + intercept_recent
    
    ax.plot(2050, prediction_all, 'ro', markersize=8, label=f'2050 Prediction (All Data): {prediction_all:.2f} inches')
    ax.plot(2050, prediction_recent, 'go', markersize=8, label=f'2050 Prediction (2000+): {prediction_recent:.2f} inches')
    
    # 5. Set labels and title
    ax.set_xlabel('Year', fontsize=12)
    ax.set_ylabel('Sea Level (inches)', fontsize=12)
    ax.set_title('Rise in Sea Level', fontsize=14, fontweight='bold')
    
    # Add grid and legend
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(loc='upper left', fontsize=10)
    
    # Set axis limits for better visualization
    ax.set_xlim(1850, 2060)
    ax.set_ylim(bottom=0)
    
    # Add some statistics as text
    stats_text = f"Statistics:\nAll Data (1880-2014): R² = {r_value_all**2:.4f}\nRecent Data (2000-2014): R² = {r_value_recent**2:.4f}"
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, 
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save plot
    plt.savefig('sea_level_plot.png')
    
    # Return the figure
    return fig
