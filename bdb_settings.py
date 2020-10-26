"""
@author: Ross Drucker
"""
import os

# Base directory
base = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(base, 'data')
img_dir = os.path.join(base, 'img')
helpers_dir = os.path.join(base, 'bdb_helpers')

# File locations
games_data_file = os.path.join(data_dir, 'games.csv')
teams_data_file = os.path.join(data_dir, 'team_data.csv')
plays_data_file = os.path.join(data_dir, 'plays.csv')
players_data_file = os.path.join(data_dir, 'players.csv')
plot_testing_data_file = os.path.join(data_dir, 'plot_testing.csv')

