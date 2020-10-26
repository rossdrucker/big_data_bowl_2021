"""
@author: Ross Drucker
"""
import pandas as pd

import bdb_helpers.lookup as find
import bdb_helpers.data_loaders as load

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
        
    return tracking_and_plays

if __name__ == '__main__':
    gid = 2018121603
    pid = 105
    t_and_p = tracking_and_plays(gid, pid)