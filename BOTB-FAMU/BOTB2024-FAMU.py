# PROMPT USED WITH: Are there any notable trends in play outcomes based on down and distance?

import pandas as pd
import numpy as np

# Load the dataset
game_data_df = pd.read_csv('game_data.csv')

# Prepare the data
# Filter out plays that are not relevant for down and distance analysis (e.g., kickoffs, extra points)
game_data_df_filtered = game_data_df[game_data_df['PlayType'].isin(['PASS', 'RUSH'])]

# Group by Down and ToGo (distance) and calculate the average yards gained
play_outcomes = game_data_df_filtered.groupby(['Down', 'ToGo'])['Yards'].mean().reset_index()

# Pivot the data for better visualization
play_outcomes_pivot = play_outcomes.pivot('Down', 'ToGo', 'Yards')

# Display the pivot table
print(play_outcomes_pivot)


# PROMPT USED WITH: Are there any notable differences in play outcomes based on the quarter of the game?

# Load the dataset
game_data_df = pd.read_csv('game_data.csv')

# Filter for pass and rush plays only
game_data_df = game_data_df[(game_data_df['PlayType'] == 'PASS') | (game_data_df['PlayType'] == 'RUSH')]

# Group by Quarter and calculate the average yards gained for each quarter
quarter_avg_yards = game_data_df.groupby('Quarter')['Yards'].mean().reset_index()

# Print the result
print(quarter_avg_yards)