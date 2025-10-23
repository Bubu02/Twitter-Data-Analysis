import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('twitter.csv')

# Convert 'time' to datetime objects
df['time'] = pd.to_datetime(df['time'])

# Filter 1: More than 10 replies
filtered_df = df[df['replies'] > 10].copy()

# Filter 2: Tweet date is an odd number
filtered_df['day'] = filtered_df['time'].dt.day
filtered_df = filtered_df[filtered_df['day'] % 2 != 0]

# Filter 3: Tweet word count be above 50
filtered_df['word_count'] = df['Tweet'].str.split().str.len()
filtered_df = filtered_df[filtered_df['word_count'] > 50]

# Calculate engagement rate
filtered_df['engagement_rate'] = (filtered_df['media engagements'] / filtered_df['media views']) * 100

# Separate tweets with engagement rate > 5%
highlight_df = filtered_df[filtered_df['engagement_rate'] > 5]

# Create the scatter plot
plt.figure(figsize=(12, 8))
plt.scatter(filtered_df['media views'], filtered_df['media engagements'], label='Engagement Rate <= 5%')
plt.scatter(highlight_df['media views'], highlight_df['media engagements'], color='red', label='Engagement Rate > 5%')

# Add titles and labels
plt.title('Media Engagements vs. Media Views')
plt.xlabel('Media Views')
plt.ylabel('Media Engagements')
plt.legend()
plt.grid(True)

# Add description of filters to the plot
filter_description = "Filters Applied:\n- Replies > 10\n- Tweet date is an odd number\n- Word count > 50"
plt.text(0.05, 0.95, filter_description, transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', fc='wheat', alpha=0.5))

# Save the plot to a file
plt.savefig('media_engagement_plot.png')
plt.show()
