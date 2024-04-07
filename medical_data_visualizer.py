import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

csv_url = "medical_examination.csv"

# Import data
df = pd.read_csv(csv_url)

# Add 'overweight' column
df['overweight'] = ((df['weight'] / ((df['height'] / 100) ** 2) > 25) * 1).values

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

for blood_component in ['cholesterol','gluc']:
    df.loc[df[blood_component] == 1, blood_component] = 0
    df.loc[df[blood_component] > 1, blood_component] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = pd.melt(df, id_vars='cardio', value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])
    print(df_cat.value_counts())
    

    # Draw the catplot with 'sns.catplot()'
    sns.catplot(kind='count', data=df_cat, x='variable', hue='value',col='cardio').set_ylabels("total")

    # Get the figure for the output
    fig = sns.catplot(kind='count', data=df_cat, x='variable', hue='value',col='cardio').set_ylabels("total").figure


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df.loc[
        (df['ap_lo'] <= df['ap_hi']) & 
        (df['height'] >= df['height'].quantile(0.025)) & 
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975)) 
    ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.full((len(corr),len(corr)), False)
    mask[np.triu_indices_from(corr)] = True

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 10))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, vmax=0.3, vmin=-0.14, center=0, mask=mask, annot=True, fmt=".1f", linewidths=.5, ax=ax).set_xticklabels(ax.get_xticklabels(), rotation=90)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
