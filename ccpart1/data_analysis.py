import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset 
df = pd.read_csv('./All_Diets.csv')

# Handle missing data (fill missing values with mean)
df.fillna(df.mean(numeric_only=True), inplace=True)

# Calculate the average macronutrient content for each diet type
avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

# Find the top 5 protein-rich recipes for each diet type
top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)

# Add new metrics (Protein-to-Carbs ratio and Carbs-to-Fat ratio)
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']

# Replace infinite values from division
df = df.replace([float('inf'), float('-inf')], pd.NA)
df = df.fillna(df.mean(numeric_only=True))

# Identify most common cuisine types by diet type
common_cuisines = (
    df.groupby(['Diet_type', 'Cuisine_type'])
      .size()
      .reset_index(name='count')
      .sort_values(['Diet_type', 'count'], ascending=[True, False])
      .groupby('Diet_type')
      .head(1)
)

# Identify diet type with highest average protein
highest_protein_diet = avg_macros['Protein(g)'].idxmax()

# Bar chart for average macronutrients (Protein, Carbs, Fat)
avg_melted = avg_macros.reset_index().melt(
    id_vars='Diet_type',
    value_vars=['Protein(g)', 'Carbs(g)', 'Fat(g)'],
    var_name='Macronutrient',
    value_name='Average'
)

sns.barplot(data=avg_melted, x='Diet_type', y='Average', hue='Macronutrient')
plt.title('Average Macronutrients by Diet Type')
plt.ylabel('Average (g)')
plt.tight_layout()
plt.show()

# Heat map for showing the relationship between macronutrient content and diet types
plt.figure(figsize=(8, 6))
sns.heatmap(avg_macros, annot=True, fmt='.1f', cmap='YlGnBu')
plt.title('Average Macronutrients by Diet Type')
plt.ylabel('Diet Type')
plt.xlabel('Macronutrient')
plt.tight_layout()
plt.show()

# Scatter plot for top 5 protein-rich recipes and cuisines
sns.scatterplot(
    data=top_protein,
    x='Protein(g)',
    y='Carbs(g)',
    hue='Cuisine_type',
    style='Diet_type'
)
plt.title('Top 5 Protein-Rich Recipes by Diet Type and Cuisine')
plt.xlabel('Protein (g)')
plt.ylabel('Carbs (g)')
plt.tight_layout()
plt.show()
