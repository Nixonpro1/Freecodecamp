import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date')
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data by filtering out days when page views were in the top 2.5% or bottom 2.5%
df = df[(df['value'] >= df['value'].quantile(0.025)) & 
        (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    
    # Prepare data for bar plot (add columns for year and month)
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    
    # Group by year and month and calculate average page views
    df_bar_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
    # Draw bar plot
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create the bar plot
    df_bar_grouped.plot(kind='bar', ax=ax)
    
    # Customize the plot
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Monthly Average Page Views by Year')
    
    # Set month labels in legend
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    ax.legend(title='Months', labels=month_names)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (copy and add year and month columns)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    
    # Sort months in chronological order
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Year-wise box plot
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    
    # Month-wise box plot
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    
    # Rotate x-axis labels for better readability
    axes[1].tick_params(axis='x', rotation=45)
    
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
