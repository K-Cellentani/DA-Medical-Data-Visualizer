import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')


# Add 'overweight' column
df['overweight'] =np.where((df['weight'] / ((df['height'] / 100) ** 2) >25), 1, 0)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df.loc[df['cholesterol'] == 1, 'cholesterol'] = 0
df.loc[df['cholesterol'] > 0, 'cholesterol'] = 1

df.loc[df['gluc'] == 1, 'gluc'] = 0
df.loc[df['gluc'] > 0, 'gluc'] = 1


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])
  

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size()
    df_cat = df_cat.reset_index(name='total')

    # Draw the catplot with 'sns.catplot()'
    cat = sns.catplot(x='variable', y='total', col='cardio', hue='value',
                      data=df_cat, kind='bar')
    
    # Get the figure for the output
    fig = cat.fig
    

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))]
   
  
    
    # Calculate the correlation matrix
    corre = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corre))



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(10,8))
    
    
    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corre, mask=mask, annot=True, square=True, fmt='0.1f', linewidths=1, center=0)
    

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
