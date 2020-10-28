"""
@author: Ross Drucker
"""
import os
import math
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

import bdb_helpers.lookup as find
import bdb_helpers.data_loaders as load
import bdb_helpers.data_mergers as merge
import bdb_helpers.input_checkers as check
import bdb_helpers.file_movers as file_ops

warnings.filterwarnings('ignore')

import time

def orient_jersey_num(gid, pid, prechecked_gid = False, prechecked_pid = False,
                tracking = pd.DataFrame()):
    """
    Manipulate the tracking data to get the correct orientation for the jersey
    numbers of players involved in the play that will be plotted

    Parameters
    ----------
    gid: an integer of a game_id
    pid: an integer of a play_id
    prechecked_gid: a boolean of whether or not the game ID has been checked
        before being passed to the function
    prechecked_pid: a boolean of whether or not the play ID has been checked
         before being passed to the function
    tracking: a dataframe of tracking data that can be used to speed up
        data loading

    Returns
    -------
    tracking: a dataframe of tracking data with the proper orientation for the
        jersey numbers of the players involved
    """
    # If the game ID is not already checked, check that first
    if not prechecked_gid:
        gid = check.game_id(gid)
        prechecked_gid = True
    
    # Now that the game ID is checked, move to the play ID. If that is not
    # already checked, check that next. prechecked_gid is now True regardless
    # of its initially passed value since the game ID has been checked in the
    # first if statement
    if not prechecked_pid:
        pid = check.play_id(gid, pid, prechecked_gid)
    
    # Now that the game ID and play ID have been checked, load the tracking
    # data for the play in the provided game. This will load all tracking data
    # for the play. It will 
    if tracking.empty:
        tracking = merge.tracking_and_plays(gid, pid)
    
    tracking.loc[tracking['team'] == 'football', 'jersey_num_orientation'] = 0
    
    tracking.loc[
        (tracking['team'] == 'home') & (tracking['play_direction'] == 'right'),
        'jersey_num_orientation'
    ] = -90
    
    tracking.loc[
        (tracking['team'] == 'away') & (tracking['play_direction'] == 'right'),
        'jersey_num_orientation'
    ] = 90
    
    tracking.loc[
        (tracking['team'] == 'home') & (tracking['play_direction'] == 'left'),
        'jersey_num_orientation'
    ] = 90
    
    tracking.loc[
        (tracking['team'] == 'away') & (tracking['play_direction'] == 'left'),
        'jersey_num_orientation'
    ] = -90
    
    return tracking['jersey_num_orientation']

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
               plot_arrows = True, prechecked_gid = False,
               prechecked_pid = False, prechecked_frame = False,
               tracking = pd.DataFrame()):
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
    prechecked_frame: a boolean indicating whether or not it's okay to
        skip the frame validation. Defaulting to False, but should be set to
        True when using the draw_play_gif() function
    tracking: a dataframe of tracking data that can be used to speed up
        plotting

    Returns
    -------
    fig, ax: the figure and axes objects (respectively)
    """
    if gid != 0:
        # Start by checking the game ID if it is provided but not yet checked
        if not prechecked_gid:
            gid = check.game_id(gid)
            prechecked_gid = True
        
        # Get the home and away teams for the game
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
        
    # Next, check the play ID if it has not already been checked
    if not prechecked_pid:
        pid = check.play_id(gid, pid, prechecked_gid)
        prechecked_pid = True
    
    # If tracking isn't supplied, load all relevant tracking data
    if tracking.empty:
        tracking = merge.tracking_and_plays(gid, pid)
        
    if not prechecked_frame:
        frame_no = check.frame_no(gid, pid, frame_no, tracking)
    
    # Start prepping the data for the plot. Primarily, the jersey numbers'
    # rotation angle based on team and play direction
    tracking['jersey_num_orientation'] = orient_jersey_num(
        gid,
        pid,
        prechecked_gid,
        prechecked_pid,
        tracking
    )
    
    # Split the frame's data into the home team, the away team, and the ball's
    # data (respectively)
    home_frame = tracking[
        (tracking['team'] == 'home') & (tracking['frame_id'] == frame_no)
    ]
    away_frame = tracking[
        (tracking['team'] == 'away') & (tracking['frame_id'] == frame_no)
    ]
    ball_frame = tracking[
        (tracking['team'] == 'football') & (tracking['frame_id'] == frame_no)
    ]
    
    # Get the hex color information about each team to use to make the plot
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
    
    # If the line of scrimmage is to be plotted, determine its position
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
    
    # If the first down line is to be plotted, determine its position
    if plot_first_down_marker:
        first_down = find.first_down_line(
            gid,
            pid,
            tracking,
            prechecked_gid,
            prechecked_pid
        )
        
        first_down_line = pd.DataFrame({
            'x': [first_down - (2/12),
                  first_down + (2/12),
                  first_down + (2/12),
                  first_down - (2/12),
                  first_down - (2/12)
            ],
            'y': [1/9, 1/9, 53 + (2/9), 53 + (2/9), 1/9]
        })
    
    # Draw the field
    fig, ax = field(gid)
    
    # Plot the home team's players
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
    
    # Add the jersey numbers for the home team
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
            rotation = player['jersey_num_orientation'],
            zorder = 20,
            fontdict = {'ha': 'center', 'va': 'center'},
        )
        
        if plot_arrows:        
            ax.arrow(x = player['player_x'],
                     y = player['player_y'],
                     dx = 3 * math.cos(player['player_orientation']),
                     dy = 3 * math.sin(player['player_orientation']),
                     length_includes_head = True, width = 0.3,
                     color = home_uni_highlight, zorder = 14
            )
    
    # Plot the away team's players
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
    
    # Add the jersey numbers for the away team
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
            rotation = player['jersey_num_orientation'],
            zorder = 20,
            fontdict = {'ha': 'center', 'va': 'center'},
        )
        
        if plot_arrows:        
            ax.arrow(x = player['player_x'],
                     y = player['player_y'],
                     dx = 3 * math.cos(player['player_orientation']),
                     dy = 3 * math.sin(player['player_orientation']),
                     length_includes_head = True, width = 0.3,
                     color = away_uni_highlight, zorder = 14
            )
    
    # Plot the ball
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
    
    return fig, ax

def play_gif(gid = 0, pid = 0, home = '', away = '', prechecked_gid = False,
             prechecked_pid = False, tracking = pd.DataFrame()):
    # If a game ID is provided, get the home and away team from the provided
    # game ID
    if gid != 0:
        # Start by checking the game ID if it is provided but not yet checked
        if not prechecked_gid:
            gid = check.game_id(gid)
            prechecked_gid = True
        
        # Get the home and away teams for the game
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
        
    # Next, check the play ID if it has not already been checked
    if not prechecked_pid:
        pid = check.play_id(gid, pid, prechecked_gid)
        prechecked_pid = True
    
    # If tracking isn't supplied, load all relevant tracking data
    if tracking.empty:
        tracking = merge.tracking_and_plays(gid, pid)
    
    # Get the number of frames in the play
    n_frames = find.n_frames(
        gid = gid,
        pid = pid,
        tracking = tracking,
        prechecked_gid = True,
        prechecked_pid = True
    )
    
    # Make the temporary directory to hold static images
    file_ops.make_gif_temp_dir(gid, pid)
    
    # Make each frame as a static image
    for i in np.arange(1, n_frames + 1):
        print(f'Processing frame {i} of {n_frames}')
        fig, ax = play_frame(
            gid,
            pid,
            frame_no = i,
            prechecked_gid = True,
            prechecked_pid = True,
            tracking = tracking,
            prechecked_frame = True
        )
        
        if i < 10:
            fname = os.path.join(
                'img', 'temp', f'{gid}_{pid}', f'{gid}_{pid}_000{i}.png'
            )
        elif i < 100:
            fname = os.path.join(
                'img', 'temp', f'{gid}_{pid}', f'{gid}_{pid}_00{i}.png'
            )
        else:
            fname = os.path.join(
                'img', 'temp', f'{gid}_{pid}', f'{gid}_{pid}_0{i}.png'
            )
        
        plt.savefig(f'{fname}', bbox_inches = 'tight', pad_inches = 0)
    
    try:
        gif_fname = tracking['down_dist_summary'].values[0] + '.gif'
    
    except:
        gif_fname = str(pid) + '.gif'
        
    # Collect the static images
    images = file_ops.collect_gif_play_frames(gid, pid)
    
    # Make and save the gif
    file_ops.make_gif(gid, pid, images, fname = gif_fname)
    
    # Delete the temporary directory that holds all static images.
    file_ops.remove_temp_static_frame_directory(gid, pid)
    
    return None

if __name__ == '__main__':
    gid = 2018121603
    pid = 105
    frame_no = 33
    fig, ax = field(gid)
    
    start1 = time.time()
    fig, ax = play_frame(gid, pid, frame_no = frame_no)
    end1 = time.time()
    
    tracking = merge.tracking_and_plays(gid, pid)
    start2 = time.time()
    fig, ax = play_frame(gid, pid, frame_no = frame_no, tracking = tracking)
    end2 = time.time()
    
    print(f'Method 1 took {round(end1 - start1, 3)} seconds')
    print(f'Method 2 took {round(end2 - start2, 3)} seconds')
    
    start3 = time.time()
    play_gif(gid, pid)
    end3 = time.time()
    
    start4 = time.time()
    play_gif(gid, pid, tracking = tracking)
    end4 = time.time()
    
    print(f'Method 1 took {round(end3 - start3, 3)} seconds')
    print(f'Method 2 took {round(end4 - start4, 3)} seconds')
    
    gid = 2018123006
    pid = 2265
    