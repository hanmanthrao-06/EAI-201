import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("\n" + "="*70)
print("TASK 2: EDA AND CLEANING")
print("="*70 + "\n")

# Load data
df = pd.read_csv('merged_zoo_data_with_features.csv')
print(f"Loaded {len(df)} records\n")

# Create visualizations
sns.set_style("whitegrid")
fig = plt.figure(figsize=(16, 14))

# VIZ 1: Stack bar chart
ax1 = plt.subplot(2, 2, 1)
conservation_class = pd.crosstab(df['conservation_status'], df['class_type'])
conservation_class.plot(kind='bar', stacked=True, ax=ax1, colormap='tab10')
ax1.set_title('Class Distribution by Conservation Status', fontweight='bold')
ax1.set_xlabel('Conservation Status')
ax1.set_ylabel('Count')
ax1.legend(title='Class', fontsize=8)
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# VIZ 2: Violin plot
ax2 = plt.subplot(2, 2, 2)
sns.violinplot(data=df, x='class_type', y='legs', ax=ax2, palette='Set2')
ax2.set_title('Feature Distribution by Class Type', fontweight='bold')
ax2.set_xlabel('Class Type')
ax2.set_ylabel('Legs')

# VIZ 3: Scatter plot
ax3 = plt.subplot(2, 2, 3)
bio = ['hair', 'feathers', 'eggs', 'milk', 'airborne', 'aquatic', 'predator', 'toothed', 'backbone', 'breathes', 'venomous', 'fins', 'legs', 'tail', 'domestic']
top_3 = df[bio].var().nlargest(3).index.tolist()
colors = df['class_type'].map({1: 'red', 2: 'blue', 3: 'green', 4: 'orange', 5: 'purple', 6: 'brown', 7: 'pink'})
ax3.scatter(df[top_3[0]], df[top_3[1]], c=colors, alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
ax3.set_xlabel(top_3[0])
ax3.set_ylabel(top_3[1])
ax3.set_title('Scatter: Top 2 Features', fontweight='bold')

# VIZ 4: Heatmap
ax4 = plt.subplot(2, 2, 4)
habitat_class = pd.crosstab(df['habitat_type'], df['class_type'])
sns.heatmap(habitat_class, annot=True, fmt='d', cmap='YlOrRd', ax=ax4, cbar_kws={'label': 'Count'})
ax4.set_title('Habitat vs Class Distribution', fontweight='bold')
ax4.set_xlabel('Class Type')
ax4.set_ylabel('Habitat Type')

plt.tight_layout()
plt.savefig('eda_visualizations.png', dpi=300)
print("Visualizations saved as eda_visualizations.png\n")

# Statistics
print("="*70)
print("EDA STATISTICS")
print("="*70)
print(f"\nClass Distribution:\n{df['class_type'].value_counts().sort_index()}")
print(f"\nConservation Status:\n{df['conservation_status'].value_counts()}")
print(f"\nEndangered Animals: {df['is_endangered'].sum()}")
print(f"\nTop 3 Features by Variance: {top_3}")
print(f"\nHabitat Distribution:\n{df['habitat_type'].value_counts()}")

print("\n" + "="*70)
print("TASK 2 COMPLETE")
print("="*70 + "\n")
