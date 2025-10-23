import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Load the dataset
df = pd.read_csv('twitter.csv')

# Convert 'date' to datetime objects
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')

# Function to extract the last hashtag
def extract_last_hashtag(tweet):
    hashtags = re.findall(r'#(\w+)', tweet)
    if hashtags:
        return hashtags[-1]
    return None

# Apply the function to create a new 'user_profile' column
df['user_profile'] = df['Tweet'].apply(extract_last_hashtag)

# Filter 1: Exclude weekends
df_filtered = df[df['date'].dt.dayofweek < 5]

# Filter 2: Even number of impressions
df_filtered = df_filtered[df_filtered['impressions'] % 2 == 0]

# Filter 3: Odd day of the month
df_filtered = df_filtered[df_filtered['date'].dt.day % 2 != 0]

# Filter 4: Tweet word count below 30
df_filtered = df_filtered[df_filtered['Tweet'].str.split().str.len() < 30]

# Calculate total engagement
df_filtered['total_engagement'] = df_filtered['retweets'] + df_filtered['likes']

# Get the top 10 tweets
top_10_tweets = df_filtered.sort_values(by='total_engagement', ascending=False).head(10).copy()

# Add a serial number for plotting and table
top_10_tweets['serial_number'] = range(1, len(top_10_tweets) + 1)

# --- Plot Generation ---
plt.figure(figsize=(12, 8))
sns.barplot(x='serial_number', y='total_engagement', data=top_10_tweets, palette='viridis')

# Add labels and title
plt.xlabel('Tweet Serial Number')
plt.ylabel('Total Engagement (Retweets + Likes)')
plt.title('Top 10 Tweets by Engagement (Filtered)')

# Add a description of the filters
filter_description = """
Filters Applied:
- Tweets posted on weekdays only
- Even number of impressions
- Odd day of the month for tweet date
- Tweet word count below 30
- User profile extracted from the last hashtag in the tweet.
"""
plt.text(0, 1.02, filter_description, transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='bottom', bbox=dict(boxstyle='round,pad=0.5', fc='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('top_10_tweets_filtered_bar_plot.png')
plt.show()

# --- Table Generation ---
print("\n--- Top 10 Tweets Details (Filtered) ---")
table_data = top_10_tweets[['serial_number', 'Tweet', 'total_engagement', 'user_profile']]
print(table_data.to_string(index=False))