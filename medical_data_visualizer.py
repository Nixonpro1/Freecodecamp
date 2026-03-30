import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1. Import the data from medical_examination.csv and assign it to the df variable
df = pd.read_csv('medical_examination.csv')

# 2. Add an overweight column to the data
# Calculate BMI: weight(kg) / (height(m))^2
# Note: height is in cm, so convert to meters by dividing by 100
df['BMI'] = df['weight'] / ((df['height'] / 100) ** 2)
df['overweight'] = (df['BMI'] > 25).astype(int)
df = df.drop('BMI', axis=1)

# 3. Normalize data by making 0 always good and 1 always bad
# For cholesterol and gluc: if value is 1, set to 0; if value > 1, set to 1
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

# 4. Draw the Categorical Plot
def draw_cat_plot():
    # 5. Create a DataFrame for the cat plot using pd.melt
    df_cat = pd.melt(df, id_vars=['cardio'], 
                     value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    
    # 6. Group and reformat the data
    # Rename the 'value' column to 'total' for clarity
    df_cat = df_cat.rename(columns={'value': 'total'})
    
    # Group by cardio, variable, and total, then count occurrences
    df_cat = df_cat.groupby(['cardio', 'variable', 'total']).size().reset_index(name='count')
    
    # 7. Convert the data into long format and create a chart
    # Draw the categorical plot
    fig = sns.catplot(x='variable', y='count', hue='total', 
                      col='cardio', data=df_cat, kind='bar')
    
    # 8. Get the figure for the output and store it in the fig variable
    fig = fig.figure
    
    # 9. Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig

# 10. Draw the Heat Map
def draw_heat_map():
    # 11. Clean the data
    df_heat = df.copy()
    
    # Filter out incorrect data:
    # Diastolic pressure is higher than systolic
    df_heat = df_heat[(df_heat['ap_lo'] <= df_heat['ap_hi'])]
    
    # Height is less than the 2.5th percentile
    height_lower = df_heat['height'].quantile(0.025)
    df_heat = df_heat[(df_heat['height'] >= height_lower)]
    
    # Height is more than the 97.5th percentile
    height_upper = df_heat['height'].quantile(0.975)
    df_heat = df_heat[(df_heat['height'] <= height_upper)]
    
    # Weight is less than the 2.5th percentile
    weight_lower = df_heat['weight'].quantile(0.025)
    df_heat = df_heat[(df_heat['weight'] >= weight_lower)]
    
    # Weight is more than the 97.5th percentile
    weight_upper = df_heat['weight'].quantile(0.975)
    df_heat = df_heat[(df_heat['weight'] <= weight_upper)]
    
    # 12. Calculate the correlation matrix
    corr = df_heat.corr()
    
    # 13. Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    # 14. Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # 15. Plot the correlation matrix using seaborn's heatmap
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', 
                center=0, square=True, linewidths=.5, 
                cbar_kws={'shrink': 0.5}, ax=ax)
    
    # 16. Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
