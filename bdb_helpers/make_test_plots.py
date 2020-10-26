"""
@author: Ross Drucker
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

import bdb_filepaths as fp
import bdb_helpers.data_loaders as load
import bdb_helpers.plot_helpers as draw


plot_test_data = pd.read_csv(fp.plot_test_data)
teams_info = load.teams_data()

for i, row in plot_test_data.iterrows():
    home = row['home']
    away = row['away']
    
    home_frame = pd.DataFrame(
        row[['home', 'home_x', 'home_y', 'home_jersey_no']]
    ).transpose()
    away_frame = pd.DataFrame(
        row[['away', 'away_x', 'away_y', 'away_jersey_no']]
    ).transpose()
    home_info = teams_info[teams_info['team_code'] == home]
    away_info = teams_info[teams_info['team_code'] == away]
    
    fig, ax = draw.field(home = home, away = away)
    
    home_frame.plot(
        x = 'home_x',
        y = 'home_y',
        kind = 'scatter',
        ax = ax,
        color = home_info['home_uni_base'],
        s = 800,
        edgecolor = home_info['home_uni_highlight'],
        linewidth = 2,
        zorder = 15
    )
    
    for i, player in home_frame.iterrows():
        ax.text(
            x = player['home_x'],
            y = player['home_y'],
            s = str(int(player['home_jersey_no'])),
            fontsize = 15,
            color = home_info['home_uni_number'].iloc[0],
            path_effects = [
                pe.withStroke(
                    linewidth = 3,
                    foreground = f'{home_info.home_uni_number_highlight.iloc[0]}'
                )
            ],
            fontweight = 'bold',
            rotation = -90,
            zorder = 20,
            fontdict = {'ha': 'center', 'va': 'center'},
        )
        
    away_frame.plot(
        x = 'away_x',
        y = 'away_y',
        kind = 'scatter',
        ax = ax,
        color = away_info['away_uni_base'],
        s = 800,
        edgecolor = away_info['away_uni_highlight'],
        linewidth = 2,
        zorder = 15
    )
    
    for i, player in away_frame.iterrows():
        ax.text(
            x = player['away_x'],
            y = player['away_y'],
            s = str(int(player['away_jersey_no'])),
            fontsize = 15,
            color = home_info['away_uni_number'].iloc[0],
            path_effects = [
                pe.withStroke(
                    linewidth = 2,
                    foreground = f'{away_info.away_uni_number_highlight.iloc[0]}'
                )
            ],
            fontweight = 'bold',
            rotation = 90,
            zorder = 20,
            fontdict = {'ha': 'center', 'va': 'center'},
        )
    
    if not os.path.exists(os.path.join('img', 'test_plots')):
        os.makedirs(os.path.join('img', 'test_plots'))
        
    fname = os.path.join('img', 'test_plots', f'plt_preview_{home}.png')
    plt.savefig(f'{fname}', bbox_inches = 'tight', pad_inches = 0)