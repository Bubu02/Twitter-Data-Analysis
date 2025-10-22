import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
try:
    df = pd.read_csv('twitter.csv')
except FileNotFoundError:
    print("Error: 'twitter.csv' not found. Please make sure the file is in the correct directory.")
    exit()

# Data Cleaning and Preparation
# Convert date to datetime objects
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

# Filter 1: At least one interaction type
df_filtered = df[(df['url clicks'] > 0) | (df['user profile clicks'] > 0) | (df['hashtag clicks'] > 0)].copy()

# Filter 2: Tweet date is an even number
df_filtered = df_filtered[df_filtered['date'].dt.day % 2 == 0]

# Filter 3: Tweet word count is above 40
df_filtered['word_count'] = df_filtered['Tweet'].str.split().str.len()
df_filtered = df_filtered[df_filtered['word_count'] > 40]

# Categorize tweets
def categorize_tweet(row):
    if row['media views'] > 0 or row['media engagements'] > 0:
        return 'With Media'
    if row['url clicks'] > 0:
        return 'With Links'
    if row['hashtag clicks'] > 0:
        return 'With Hashtags'
    return 'Other'

df_filtered['category'] = df_filtered.apply(categorize_tweet, axis=1)

# Aggregate data for the chart
category_data = df_filtered.groupby('category')[['url clicks', 'user profile clicks', 'hashtag clicks']].sum().reset_index()

# Melt the dataframe for easy plotting with seaborn
melted_data = category_data.melt(id_vars='category', var_name='Click Type', value_name='Total Clicks')

# Create the clustered bar chart
plt.figure(figsize=(12, 8))
sns.barplot(x='category', y='Total Clicks', hue='Click Type', data=melted_data)

# Add titles and labels
plt.title('Sum of URL, Profile, and Hashtag Clicks by Tweet Category\n(Filtered: Even Day, Word Count > 40, At least one click type)')
plt.xlabel('Tweet Category')
plt.ylabel('Sum of Clicks')
plt.xticks(rotation=0)
plt.legend(title='Click Type')

# Add a description
description = """
This chart shows the sum of URL clicks, user profile clicks, and hashtag clicks,
broken down by tweet category. The data is filtered to include only tweets that meet
the following criteria:
- The tweet was posted on an even-numbered day of the month.
- The tweet has a word count greater than 40.
- The tweet has at least one URL click, user profile click, or hashtag click.
"""
plt.figtext(0.5, -0.1, description, ha="center", fontsize=10, wrap=True)


# Save the plot
plt.savefig('clustered_bar_chart.png', bbox_inches='tight')

print("Clustered bar chart saved as 'clustered_bar_chart.png'")
