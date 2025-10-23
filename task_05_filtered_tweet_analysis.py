import pandas as pd
import matplotlib.pyplot as plt
import re

"""
This script performs the following tasks:
1.  Loads the twitter.csv dataset.
2.  Filters tweets based on the following criteria:
    - Media engagements greater than the median value.
    - Tweets posted between June and August of 2020.
    - Tweet date (day of the month) is an odd number.
    - Media views are an even number.
    - Tweet character count is above 20.
3.  Removes words containing the letter 's' from the tweet text.
4.  Creates a bar plot comparing replies, retweets, and likes for the filtered tweets.
5.  Saves the plot to the 'Plots' directory.
"""

def remove_words_with_s(text):
    """
    Removes words containing the letter 's' (case-insensitive) from a given text.
    """
    if isinstance(text, str):
        # Use regex to find all words containing 's' or 'S' and remove them
        return re.sub(r'\b\w*[sS]\w*\b', '', text).strip()
    return text

# Load the dataset
df = pd.read_csv('twitter.csv')

# Convert 'Date' column to datetime objects
df['Date'] = pd.to_datetime(df['Date'])

# Filtering conditions
# 1. Media engagements > median
median_media_engagements = df['media engagements'].median()
df_filtered = df[df['media engagements'] > median_media_engagements]

# 2. Tweets posted between June and August of 2020
df_filtered = df_filtered[(df_filtered['Date'].dt.month >= 6) & (df_filtered['Date'].dt.month <= 8) & (df_filtered['Date'].dt.year == 2020)]

# 3. Tweet date is an odd number
df_filtered = df_filtered[df_filtered['Date'].dt.day % 2 != 0]

# 4. Media views are an even number
df_filtered = df_filtered[df_filtered['media views'] % 2 == 0]

# 5. Tweet character count > 20
df_filtered = df_filtered[df_filtered['Tweet'].str.len() > 20]

# Remove words with 's' from the 'Tweet' column
df_filtered['Tweet'] = df_filtered['Tweet'].apply(remove_words_with_s)

# Calculate the sum of replies, retweets, and likes for the filtered tweets
total_replies = df_filtered['replies'].sum()
total_retweets = df_filtered['retweets'].sum()
total_likes = df_filtered['likes'].sum()

# Data for plotting
engagement_metrics = {
    'Replies': total_replies,
    'Retweets': total_retweets,
    'Likes': total_likes
}
metrics = list(engagement_metrics.keys())
values = list(engagement_metrics.values())

# Create the bar plot
plt.figure(figsize=(10, 6))
bars = plt.bar(metrics, values, color=['skyblue', 'lightgreen', 'salmon'])

# Add data labels on top of the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom') # va: vertical alignment

plt.title('Comparison of Replies, Retweets, and Likes for Filtered Tweets')
plt.ylabel('Total Count')

# Description of filters applied
filter_desc = (
    f"Filters Applied:\n"
    f"- Media engagements > {median_media_engagements:.2f} (Median)\n"
    f"- Tweets from June to August 2020\n"
    f"- Odd day of the month\n"
    f"- Even number of media views\n"
    f"- Tweet character count > 20\n"
    f"- Words with 's' removed from tweet text"
)
plt.text(0.95, 0.95, filter_desc, transform=plt.gca().transAxes, fontsize=9,
         verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round,pad=0.5', fc='wheat', alpha=0.5))

plt.tight_layout()

# Save the plot
plt.savefig('Plots/task_05_filtered_tweet_analysis.png')

# Show the plot
plt.show()