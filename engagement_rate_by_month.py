import pandas as pd
import matplotlib.pyplot as plt
import re

# Define the file path
file_path = "twitter.csv"

# --- Data Loading ---
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit() # Exit if file not found
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit() # Exit on other CSV reading errors

# --- Data Preprocessing ---

# Convert 'Date' to datetime objects
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month

# Calculate character count
df['character_count'] = df['Tweet'].apply(lambda x: len(str(x)))

# Calculate engagement rate: (Likes + Retweets) / Impressions
# Handle cases where Impressions might be zero to avoid division by zero
df['engagement_rate'] = df.apply(
    lambda row: (row['Likes'] + row['Retweets']) / row['Impressions'] if row['Impressions'] > 0 else 0,
    axis=1
)

# --- Apply Filters ---

# 1. Tweet engagement rate (rounded to nearest integer) must be an even number.
# We multiply by 100 to get a more granular integer for checking even/odd
df = df[df['engagement_rate'].apply(lambda x: round(x * 100) % 2 == 0)]

# 2. Tweet date (day of the month) must be an odd number.
df = df[df['Date'].dt.day % 2 != 0]

# 3. Tweet character count must be above 20.
df = df[df['character_count'] > 20]

# 4. Remove tweet words which have letter 'C'.
def remove_words_with_c(tweet):
    if isinstance(tweet, str):
        words = tweet.split()
        filtered_words = [word for word in words if 'c' not in word.lower()]
        return ' '.join(filtered_words)
    return tweet

df['Tweet'] = df['Tweet'].apply(remove_words_with_c)

# Create 'has_media' column
# Assuming 'Media' column indicates presence of media (e.g., non-null values)
df['has_media'] = df['media views'] > 0

# --- Data Aggregation ---

# Group by month and media presence, then calculate average engagement rate
grouped_data = df.groupby(['Month', 'has_media'])['engagement_rate'].mean().unstack()

# --- Plotting ---

plt.figure(figsize=(12, 7))
if True in grouped_data.columns:
    plt.plot(grouped_data.index, grouped_data[True], label='With Media', marker='o')
if False in grouped_data.columns:
    plt.plot(grouped_data.index, grouped_data[False], label='Without Media', marker='x')

plt.title('Average Engagement Rate Trend by Month (Filtered Data)')
plt.xlabel('Month')
plt.ylabel('Average Engagement Rate')
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.legend(title='Media Content')
plt.grid(True)
plt.tight_layout()

# Add description of filters to the plot
filters_description = (
    "Filters Applied:\n"
    "- Engagement Rate (rounded*100) is Even\n"
    "- Tweet Date (day) is Odd\n"
    "- Character Count > 20\n"
    "- Words with 'C' removed from Tweet text"
)
plt.figtext(0.02, 0.02, filters_description, ha="left", fontsize=9, bbox={"facecolor":"white", "alpha":0.5, "pad":5})

plt.savefig('engagement_rate_by_month_filtered.png')
plt.show()