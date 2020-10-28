"""
@author: Ross Drucker
"""
import numpy as np
import pandas as pd

import bdb_helpers.lookup as find
import bdb_helpers.data_loaders as load
import bdb_helpers.input_checkers as check

def tracking_and_plays(gid = 0, pid = 0, tracking = pd.DataFrame(),
                       play = pd.DataFrame()):
    """
    Merges play and tracking data together to centralize data source

    Parameters
    ----------
    gid: an integer of a game_id
    pid: an integer of a play_id
    tracking: a dataframe of tracking data that can be used to speed up
        data loading
    play: a dataframe of play-level data that can be used to speed up data
        loading

    Returns
    -------
    tracking_and_plays: a merged dataframe of tracking and play-level data
    """
    # If no tracking data is provided...
    if tracking.empty:
        
        # If a game ID and play ID are both provided, load the tracking data
        # for the play from that game
        if gid != 0 and pid != 0:
            week = find.game_week(gid)
            tracking = load.tracking_data(gid = gid, pid = pid, week = week)
    
        # If a game ID is provided but not a play ID, load all tracking for the
        # game
        elif gid != 0 and pid == 0:
            week = find.game_week(gid)
            tracking = load.tracking_data(gid = gid, week = week)
        
        # If a play ID is provided but not a game ID, load all tracking for
        # plays with matching play IDs
        elif gid == 0 and pid != 0:
            tracking = load.tracking_data(pid = pid, week = 0)
        
        # If no game ID is provided and no play ID is provided, then load all
        # tracking data from all weeks
        else:
            tracking = load.tracking_data()
    
    # If no play data is provided...
    if play.empty:
        
        # If a game ID and play ID are both provided, load the plays data for
        # the play from that game
        if gid != 0 and pid != 0:
            play = load.plays_data(gid = gid, pid = pid)
            
        # If a game ID is provided but not a play ID, load all plays data for
        # the game
        elif gid != 0 and pid == 0:
            play = load.plays_data(gid = gid)
            
        # If a play ID is provided but not a game ID, load all plays data for
        # plays with matching play IDs
        elif gid == 0 and pid != 0:
            play = load.plays_data(pid = pid)
        
        # If no game ID is provided and no play ID is provided, then load all
        # plays data
        else:
            play = load.plays_data()
            
    tracking_and_plays = pd.merge(
        left = tracking,
        right = play,
        how = 'inner', 
        on = ['game_id', 'play_id']
    )
    
    games_data = load.games_data()[['game_id', 'home', 'away', 'week']]
    
    tracking_and_plays = pd.merge(
        left = tracking_and_plays,
        right = games_data,
        how = 'inner',
        on = 'game_id'
    )
    
    tracking_and_plays['offensive_team'] = \
        tracking_and_plays['possession_team']
        
    tracking_and_plays['defensive_team'] = np.where(
        tracking_and_plays['offensive_team'] == tracking_and_plays['home'],
        tracking_and_plays['away'],
        tracking_and_plays['home']
    )
        
    return tracking_and_plays

def plays_and_games(gid = 0, home = '', away = '', prechecked_gid = False):
    """
    Merges play and game data together to better illustrate what plays are
    being run by which team and against which opponent

    Parameters
    ----------
    gid: an integer of a game_id
    home: a string representing the home team's team code
    away: a string representing the away team's team code
    play_info: a dictionary of parameters to use for subsetting. The keys MUST
        be columns in the plays data to be used. If not, they will be ignored
    prechecked_gid: a boolean of whether or not the game ID has been prechecked

    Returns
    -------
    plays_from_game: a merged dataframe of play and game data

    """
    if gid != 0:
        # If the game ID is not already checked, check the game ID first
        if not prechecked_gid:
            gid = check.game_id(gid)
            prechecked_gid = True
    
    # If the game ID is not passed, then try to get a game ID based on the home
    # and away team. If this yields nothing, then load all games
    if home != '' or away != '':
        home = check.team_code(home)
        away = check.team_code(away)
        
        gid = find.game_id(home, away)
        prechecked_gid = True
        
    # Load in plays from the identified game, or from all games if game ID = 0
    plays_from_game = load.plays_data(
        gid = gid,
        prechecked_gid = prechecked_gid
    )
    
    # Load in the games data to merge
    games_data = load.games_data(gid, prechecked_gid)[[
        'game_id', 'home', 'away', 'week'
    ]]
    
    plays_from_game = pd.merge(
        left = plays_from_game,
        right = games_data,
        how = 'inner',
        on = 'game_id'
    )
    
    plays_from_game['offensive_team'] = plays_from_game['possession_team']
    plays_from_game['defensive_team'] = np.where(
        plays_from_game['offensive_team'] == plays_from_game['home'],
        plays_from_game['away'],
        plays_from_game['home']
    )
    
    plays_from_game = plays_from_game[[
        'game_id', 'play_id', 'play_description', 'quarter', 'down',
        'yds_to_go', 'possession_team', 'play_type', 'yardline_side',
        'yardline_number', 'offense_formation', 'personnel_offense',
        'defenders_in_box', 'n_pass_rushers', 'personnel_defense',
        'type_dropback', 'presnap_away_score', 'presnap_home_score',
        'game_clock', 'absolute_yard_line', 'penalty_code', 'penalty_player',
        'pass_result', 'offensive_play_result', 'play_result', 'epa',
        'is_defensive_pi', 'down_dist_summary', 'home', 'away',
        'offensive_team', 'defensive_team', 'week'
    ]]
    
    return plays_from_game

if __name__ == '__main__':
    gid = 2018121603
    pid = 105
    t_and_p = tracking_and_plays(gid, pid)