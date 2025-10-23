
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- File Paths ---
file_path = "twitter.csv"
output_plot_path = "Plots/task_06_app_opens_engagement.png"

# --- Data Loading ---
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit()
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit()

# --- Data Preprocessing and Filtering ---

# Convert 'Date' to datetime objects
df['Date'] = pd.to_datetime(df['Date'])

# Filter 1: Weekdays (Monday=0, Sunday=6) and Time (9 AM to 5 PM)
df = df[(df['Date'].dt.weekday < 5) & (df['Date'].dt.hour >= 9) & (df['Date'].dt.hour < 17)]

# Filter 2: Tweet impressions must be an even number
df = df[df['Impressions'] % 2 == 0]

# Filter 3: Tweet date (day of the month) must be an odd number
df = df[df['Date'].dt.day % 2 != 0]

# Filter 4: Tweet character count must be above 30
df['character_count'] = df['Tweet'].str.len()
df = df[df['character_count'] > 30]

# Filter 5: Remove tweets containing the letter 'D'
df = df[~df['Tweet'].str.contains('d', case=False, na=False)]

# --- Analysis ---

# Calculate engagement rate
df['engagement_rate'] = (df['Likes'] + df['Retweets']) / df['Impressions']
df['engagement_rate'] = df['engagement_rate'].replace([float('inf'), -float('inf')], 0) # Replace inf with 0

# Categorize tweets based on detail expands
df['has_detail_expands'] = df['detail expands'] > 0

# Group by the 'has_detail_expands' category and calculate the mean engagement rate
engagement_comparison = df.groupby('has_detail_expands')['engagement_rate'].mean().reset_index()
engagement_comparison['has_detail_expands'] = engagement_comparison['has_detail_expands'].map({True: 'With Detail Expands', False: 'Without Detail Expands'})

# --- Visualization ---

plt.figure(figsize=(10, 6))
sns.barplot(x='has_detail_expands', y='engagement_rate', data=engagement_comparison, palette='hsl')

plt.title('Comparison of Engagement Rate: Detail Expands vs. No Detail Expands')
plt.xlabel('Tweet Category')
plt.ylabel('Average Engagement Rate')
plt.ylim(0, engagement_comparison['engagement_rate'].max() * 1.2) # Adjust y-axis for better visualization

# Add filter descriptions to the plot
filters_description = (
    "Filters Applied:\n"
    "- Time: 9 AM - 5 PM on Weekdays\n"
    "- Impressions: Even numbers\n"
    "- Day of Month: Odd numbers\n"
    "- Character Count: > 30\n"
    "- Tweets with letter 'D' removed"
)
plt.figtext(0.5, -0.1, filters_description, ha="center", fontsize=10, bbox={"facecolor":"white", "alpha":0.5, "pad":5})

# --- Save and Show Plot ---
plt.savefig(output_plot_path, bbox_inches='tight')
plt.show()

print(f"Analysis complete. Plot saved to {output_plot_path}")
