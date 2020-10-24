"""
@author: Ross Drucker
"""
import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

import bdb_helpers.lookup as find
import bdb_helpers.data_loaders as load
import bdb_helpers.input_checkers as check
import bdb_helpers.file_movers as file_ops

warnings.filterwarnings('ignore')

def field(gid = 0, home = 'nfl', away = '', show = False, unit = 'yd',
          zero = 'l'):
    """
    Draws a football field with the teams who are participating in the game.
    Teams are either supplied via the home and away arguments, or by looking
    them up from the game_id provided by the gid argument
    
    Parameters
    ----------
    gid: an int of a game_id for which to draw the field
    home: a string of the home team's code. Not necessary if a game_id is
        provided
    away: a string of the away team's code. Not necessary if a game_id is
        provided
    show: a boolean of whether or not to show the plot
    unit: a string for the units with which to draw the field. Default is 'yds'
        for yards, could be 'ft' for feet
    zero: a string for where the origin of the plot should be. Default is 'l',
        meaning lower left corner. Could be 'c' for center

    Returns
    -------
    fig, ax: the figure and axes objects (respectively)
    """
    
    # If a game ID is provided, get the home and away team from the provided
    # game ID
    if gid != 0:
        gid = check.game_id(gid)
        home, away = find.game_teams(gid)
        
    # If no game ID provided, and the home team is 'NFL', set home and away
    # to NFC and AFC respectively. Otherwise, check to make sure the teams are
    # legit
    else:
        home = home.upper()
        away = away.upper()
        if home == 'NFL':
            home = 'NFC'
            away = 'AFC'
        else:
            home = check.team_code(home)
            away = check.team_code(away)
    
    # Get the teams' color codes
    team_info = load.teams_data()
    
    home_info = team_info[team_info['team_code'] == home]
    away_info = team_info[team_info['team_code'] == away]
    
    #############################
    # Get the field coordinates #
    #############################
    sidelines, endlines, goal_lines, midline, minor_yd_lines_b, \
    minor_yd_lines_t, minor_yd_lines_l, minor_yd_lines_u, major_yd_lines, \
    hashes_l, hashes_u, extra_pt_mark, arrow_40_l, arrow_40_u, \
    arrow_30_l, arrow_30_u, arrow_20_l, arrow_20_u, arrow_10_l, \
    arrow_10_u, field_marks = load.football_field_coords()
        
    #################
    # Make the plot #
    #################
    fig, ax = plt.subplots()
    
    ax.set_aspect('equal')
    fig.set_size_inches(50, 22.2)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    
    # Set field color
    ax.set_facecolor('#196f0c')
    
    # Put home logo at midfield
    if home.lower() in ['', 'nfl', 'nfc', 'afc']:
        img = os.path.join('img', 'logos', 'nfl.png')
    else:
        img = os.path.join('img', 'logos', f'{home}.png')
        
    img = plt.imread(img)
    
    if unit == 'yd':
        ax.imshow(img, extent = [52., 68., 18.65, 34.65], zorder = 10)
    else:
        ax.imshow(img, extent = [-18., 18., -18., 18.], zorder = 10)
    
    # Add sidelines, goal line, and 50 yard line
    ax.fill(sidelines['x'], sidelines['y'], '#ffffff')
    ax.fill(endlines['x'], endlines['y'], '#ffffff')
    ax.fill(goal_lines['x'], goal_lines['y'], '#ffffff')
    ax.fill(midline['x'], midline['y'], '#ffffff')
    
    # Add minor yard lines and major yard lines
    ax.fill(minor_yd_lines_b['x'], minor_yd_lines_b['y'], '#ffffff')
    ax.fill(minor_yd_lines_t['x'], minor_yd_lines_t['y'], '#ffffff')
    ax.fill(minor_yd_lines_l['x'], minor_yd_lines_l['y'], '#ffffff')
    ax.fill(minor_yd_lines_u['x'], minor_yd_lines_u['y'], '#ffffff')
    ax.fill(major_yd_lines['x'], major_yd_lines['y'], '#ffffff')
    
    # Add hash marks and extra point markers
    ax.fill(hashes_l['x'], hashes_l['y'], '#ffffff')
    ax.fill(hashes_u['x'], hashes_u['y'], '#ffffff')
    ax.fill(extra_pt_mark['x'], extra_pt_mark['y'], '#ffffff')
    
    # Add the numbers to the field
    for i, label in field_marks.iterrows():
        ax.text(
            x = label['x'],
            y = label['y'],
            s = label['text'],
            fontsize = 50,
            color = '#ffffff',
            fontweight = 'bold',
            rotation = label['rotation'],
            fontname = 'Impact'
        )
    
    # Add the arrows to the field
    ax.fill(arrow_40_l['x'], arrow_40_l['y'], '#ffffff')
    ax.fill(arrow_40_u['x'], arrow_40_u['y'], '#ffffff')
    ax.fill(arrow_30_l['x'], arrow_30_l['y'], '#ffffff')
    ax.fill(arrow_30_u['x'], arrow_30_u['y'], '#ffffff')
    ax.fill(arrow_20_l['x'], arrow_20_l['y'], '#ffffff')
    ax.fill(arrow_20_u['x'], arrow_20_u['y'], '#ffffff')
    ax.fill(arrow_10_l['x'], arrow_10_l['y'], '#ffffff')
    ax.fill(arrow_10_u['x'], arrow_10_u['y'], '#ffffff')
    
    ax.text(
        x = 5,
        y = 26.65,
        s = f'{home_info.nickname.iloc[0]}',
        fontdict = {'ha': 'center', 'va': 'center'},
        fontsize = 100,
        fontweight = 'bold',
        fontname = 'Impact',
        color = f'{home_info.endzone_text.iloc[0]}',
        rotation = 90,
        path_effects = [
            pe.withStroke(
                linewidth = 20,
                foreground = f'{home_info.endzone_shadow.iloc[0]}'
            )
        ]
    )
    
    ax.text(
        x = 114,
        y = 26.65,
        s = f'{away_info.nickname.iloc[0]}',
        fontdict = {'ha': 'center', 'va': 'center'},
        fontsize = 100,
        fontweight = 'bold',
        fontname = 'Impact',
        color = f'{away_info.endzone_text.iloc[0]}',
        rotation = -90,
        path_effects = [
            pe.withStroke(
                linewidth = 20,
                foreground = f'{away_info.endzone_shadow.iloc[0]}'
            )
        ]
    )
    
    if show:
        plt.show()
        return None
    else:
        return fig, ax
    
def play_frame(gid = 0, pid = 0, home = '', away = '', frame_no = 0,
                    plot_los = True, plot_first_down_marker = True,
                    ignore_frame_validation = False, tracking = pd.DataFrame(),
                    plays = pd.DataFrame()):
    """
    Draw a frame of a given play. Teams are either supplied via the home and
    away arguments, or by looking them up from the game_id provided by the gid
    argument

    Parameters
    ----------
    gid: an int representing the game_id
    pid: an int representing the play_id
    home: a string of the home team's code. Not necessary if a game_id is
        provided
    away: a string of the away team's code. Not necessary if a game_id is
        provided
    frame_no: the number of the frame to plot
    plot_los: a boolean of whether or not to plot the line of scrimmage on the
        plot
    plot_first_down_marker: a boolean of whether or not to plot the first
        down line on the plot
    ignore_frame_validation: a boolean indicating whether or not it's okay to
        skip the frame validation. Defaulting to False, but should be set to
        True when using the draw_play_gif() function
    tracking: a dataframe of tracking data that can be used to speed up
        plotting
        

    Returns
    -------
    fig, ax: the figure and axes objects (respectively)
    play: the tracking data relevant for the play
    """
    # If a game ID is provided, get the home and away team from the provided
    # game ID
    if gid != 0:
        gid = check.game_id(gid)
        home, away = find.game_teams(gid)
        
    # If no game ID provided, and the home team is 'NFL', set home and away
    # to NFC and AFC respectively. Otherwise, check to make sure the teams are
    # legit
    else:
        home = home.upper()
        away = away.upper()
        if home == 'NFL':
            home = 'NFC'
            away = 'AFC'
        else:
            home = check.team_code(home)
            away = check.team_code(away)
            gid = find.game_id(home, away)
    
    if tracking.empty:
        week = find.game_week(gid)
        tracking = load.tracking_data(week)
        
    if not ignore_frame_validation:
        frame_no, tracking = check.frame_no(gid, pid, frame_no, tracking)
    
    game_plays = tracking[tracking['game_id'] == gid]
    play = game_plays[game_plays['play_id'] == pid]
        
    home_frame = play[
        (play['team'] == 'home') & (play['frame_id'] == frame_no)
    ]
    away_frame = play[
        (play['team'] == 'away') & (play['frame_id'] == frame_no)
    ]
    ball_frame = play[
        (play['team'] == 'football') & (play['frame_id'] == frame_no)
    ]
    
    teams_info = load.teams_data()
    home_info = teams_info[teams_info['team_code'] == home]
    away_info = teams_info[teams_info['team_code'] == away]
    
    home_uni_base = home_info['home_uni_base'].iloc[0]
    home_uni_highlight = home_info['home_uni_highlight'].iloc[0]
    home_uni_number = home_info['home_uni_number'].iloc[0]
    home_uni_number_highlight = home_info['home_uni_number_highlight'].iloc[0]
    
    away_uni_base = away_info['away_uni_base'].iloc[0]
    away_uni_highlight = away_info['away_uni_highlight'].iloc[0]
    away_uni_number = away_info['away_uni_number'].iloc[0]
    away_uni_number_highlight = away_info['away_uni_number_highlight'].iloc[0]
    
    if plot_los:
        los = find.line_of_scrimmage(gid, pid)
        los = pd.DataFrame({
            'x': [los - (2/12),
                  los + (2/12),
                  los + (2/12),
                  los - (2/12),
                  los - (2/12)
            ],
            'y': [1/9, 1/9, 53 + (2/9), 53 + (2/9), 1/9]
        })
        
    if plot_first_down_marker:
        first_down = find.first_down_line(gid, pid)
        first_down_line = pd.DataFrame({
            'x': [first_down - (2/12),
                  first_down + (2/12),
                  first_down + (2/12),
                  first_down - (2/12),
                  first_down - (2/12)
            ],
            'y': [1/9, 1/9, 53 + (2/9), 53 + (2/9), 1/9]
        })
        
    fig, ax = field(gid)
    
    home_frame.plot(
        x = 'player_x',
        y = 'player_y',
        kind = 'scatter',
        ax = ax,
        color = home_uni_base,
        s = 800,
        edgecolor = home_uni_highlight,
        linewidth = 2,
        zorder = 15
    )
    
    for i, player in home_frame.iterrows():
        ax.text(
            x = player['player_x'],
            y = player['player_y'],
            s = str(int(player['player_no'])),
            fontsize = 15,
            color = home_uni_number,
            path_effects = [
                pe.withStroke(
                    linewidth = 3,
                    foreground = home_uni_number_highlight
                )
            ],
            fontweight = 'bold',
            rotation = -90,
            zorder = 20,
            fontdict = {'ha': 'center', 'va': 'center'},
        )
        
    away_frame.plot(
        'player_x',
        'player_y',
        kind = 'scatter',
        ax = ax,
        color = away_uni_base,
        s = 800,
        edgecolor = away_uni_highlight,
        linewidth = 2,
        zorder = 15
    )
    
    for i, player in away_frame.iterrows():
        ax.text(
            x = player['player_x'],
            y = player['player_y'],
            s = str(int(player['player_no'])),
            fontsize = 15,
            color = away_uni_number,
            path_effects = [
                pe.withStroke(
                    linewidth = 3,
                    foreground = away_uni_number_highlight
                )
            ],
            fontweight = 'bold',
            rotation = 90,
            zorder = 20,
            fontdict = {'ha': 'center', 'va': 'center'},
        )
    
    ball_frame.plot(
        'player_x',
        'player_y',
        kind = 'scatter',
        ax = ax,
        color = '#624a2e',
        s = 100,
        edgecolor = '#000000',
        linewidth = 2,
        zorder = 15
    )
    
    ax.fill(los['x'], los['y'], '#183ec1')
    ax.fill(first_down_line['x'], first_down_line['y'], '#ffcb05')
    
    return fig, ax, play

def play_gif(gid = 0, pid = 0, home = '', away = '',
                  tracking = pd.DataFrame()):
    # If a game ID is provided, get the home and away team from the provided
    # game ID
    if gid != 0:
        gid = check.game_id(gid)
        home, away = find.game_teams(gid)
        
    # If no game ID provided, and the home team is 'NFL', set home and away
    # to NFC and AFC respectively. Otherwise, check to make sure the teams are
    # legit
    else:
        home = home.upper()
        away = away.upper()
        if home == 'NFL':
            home = 'NFC'
            away = 'AFC'
        else:
            home = check.team_code(home)
            away = check.team_code(away)
            gid = find.game_id(home, away)
    
    n_frames = find.n_frames(gid, pid, tracking)
    
    file_ops.make_play_img_dir(gid, pid)
    
    # Make each frame as a static image
    for i in np.arange(1, n_frames + 1):
        print(f'Processing frame {i} of {n_frames}')
        fig, ax, tracking = play_frame(
            gid,
            pid, 
            frame_no = i,
            tracking = tracking,
            ignore_frame_validation = True # Can be safely ignored here since
            # the frame number is already validated
        )
        
        if i < 10:
            fname = os.path.join(
                'img', 'temp', f'{gid}_{pid}', f'{gid}_{pid}_0{i}.png'
            )
        else:
            fname = os.path.join(
                'img', 'temp', f'{gid}_{pid}', f'{gid}_{pid}_{i}.png'
            )
        
        plt.savefig(f'{fname}', bbox_inches = 'tight', pad_inches = 0)
        
    # Collect the static images
    images = file_ops.collect_play_frames(gid, pid)
    
    # Make and save the gif
    file_ops.make_gif(gid, pid, images)
    
    # Delete the temporary directory that holds all static images.
    file_ops.remove_static_frame_directory(gid, pid)
    
    return None

if __name__ == '__main__':
    plot_test_data = pd.read_csv('data/plot_testing.csv')
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
        
        fig, ax = field(home = home, away = away)
        
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


    gid = 2018121603
    pid = 105
    frame_no = 1
    fig, ax = field(gid)
    fig, ax, tracking = play_frame(gid, pid, frame_no = frame_no)
    play_gif(gid, pid, tracking)
    