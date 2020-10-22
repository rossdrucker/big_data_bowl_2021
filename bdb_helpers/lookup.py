"""
@author: Ross Drucker
"""
import pandas as pd

import bdb_helpers.data_loaders as load
import bdb_helpers.input_checkers as check

def game_id(home, away):
    """
    Finds the game_id of a game between the home and away team. The function
    checks whether or not the teams are valid, and if the teams are reversed,
    will provide the correct game_id for the meeting of these two teams
    
    Parameters
    ----------
    home: a string of the home team's code
    away: a string of the away team's code

    Returns
    -------
    desired_game_id: the game_id of the game in which home hosted away
    """
    # Validate that the home and away team supplied are valid teams
    home = check.team_code(home)
    away = check.team_code(away)
    
    # Loop to stay in until the game is found
    game_found = False
    while not game_found:
        # Bring in the schedule information
        games = load.games_data()
        
        # Check if the game existed as supplied
        desired_game = games[(games['home'] == home) & (games['away'] == away)]
        
        # If it did, break out of the loop
        if len(desired_game) == 1:
            game_found = True
        
        # Otherwise, alert user that the home team did not host the away team
        else:
            print(f'{home} did not host {away}. Checking if {away} hosted '
                      f'{home}')
            
            # Check if away team hosted home team
            desired_game = games[
                (games['home'] == away) & (games['away'] == home)
            ]
            
            # If they did, break out of the loop
            if len(desired_game) == 1:
                game_found = True
            
            else:
                # Otherwise, prompt user to supply two new teams
                print(f'{home} and {away} did not play each other in this '
                      'dataset')
                home = check.team_code('')
                away = check.team_code('')
    
    # Once a game has been identified, give back the game ID for the game
    desired_game_id = desired_game['game_id'].iloc[0]
    
    return desired_game_id

def game_teams(gid):
    """
    Finds the teams that played in a specified game (via game_id)

    Parameters
    ----------
    gid: an integer of a game_id

    Returns
    -------
    home: a string of the home team's code
    away: a string of the away team's code
    """
    # Validate the game ID
    gid = check.game_id(gid)
    
    # Bring in the schedule data
    games = load.games_data()
    
    # Get the home and away teams
    home = games.loc[games['game_id'] == gid, 'home'].iloc[0]
    away = games.loc[games['game_id'] == gid, 'away'].iloc[0]
    
    return home, away

def game_week(gid):
    """
    Finds the week in which a particular game was played

    Parameters
    ----------
    gid: an integer of a game_id

    Returns
    -------
    week: an integer representing the week the game was played in
    """
    # Validate the game ID
    gid = check.game_id(gid)
    
    # Bring in the schedule data
    games = load.games_data()
    
    # Get the week corresponding to the game ID provided
    week = games.loc[games['game_id'] == gid, 'week'].iloc[0]
    
    return week

def line_of_scrimmage(gid, pid):
    """
    Finds the line of scrimmage for a specified play

    Parameters
    ----------
    gid: an integer of a game_id
    pid: an integer of a play_id
    
    Returns
    -------
    los: a float of the absolute yardline of the line of scrimmage
    """
    # Validate the game ID and play ID
    gid = check.game_id(gid)
    pid = check.play_id(gid, pid)
    
    # Load in the plays data
    plays = load.plays_data()
    
    # Find the play's data based on the game ID and play ID
    play = plays[(plays['game_id'] == gid) & (plays['play_id'] == pid)]
    
    # Get the line of scrimmage
    los = play['absolute_yard_line'].iloc[0]
    
    return los

def yards_to_go(gid, pid):
    """
    Finds the distance needed (in yards) to achieve a first down

    Parameters
    ----------
    gid: an integer of a game_id
    pid: an integer of a play_id

    Returns
    -------
    yds_to_go: an integer number of yards needed on a play to achieve
        a first down
    """
    # Validate the game ID and play ID
    gid = check.game_id(gid)
    pid = check.play_id(gid, pid)
    
    # Load in the plays data
    plays = load.plays_data()
    
    # Find the play's data based on the game ID and play ID
    play = plays[(plays['game_id'] == gid) & (plays['play_id'] == pid)]
    
    # Get the number of yards needed for a first down
    yds_to_go = play['yds_to_go'].iloc[0]
    
    return yds_to_go

def first_down_line(gid, pid):
    """
    Finds what yardline is needed to be gained to achieve a first down

    Parameters
    ----------
    gid: an integer of a game_id
    pid: an integer of a play_id

    Returns
    -------
    first_down_yardline: a float representing the absolute yardline needed
        to achieve a first down
    """
    # Validate the game ID and play ID
    gid = check.game_id(gid)
    pid = check.play_id(gid, pid)
    
    # Load in the schedule data
    games = load.games_data()
    
    # Get the week of the game so that the correct tracking information can be
    # loaded
    week = games.loc[games['game_id'] == gid, 'week'].iloc[0]
    
    # Get the line of scrimmage and number of yards needed to achieve a first
    # down
    los = line_of_scrimmage(gid, pid)
    distance_to_first = yards_to_go(gid, pid)
    
    # Load in the appropriate tracking data, then subset to only be for the
    # desired play
    tracking = load.tracking_data(week)
    tracking = tracking[tracking['game_id'] == gid]
    tracking = tracking[tracking['play_id'] == pid]
    
    # Get the direction of play. If the play is going right, yards will be
    # added, otherwise they will be subtracted
    play_direction = tracking['play_direction'].iloc[0]
    
    # Calculate the yardline needed to be gained to achieve a first down
    if play_direction == 'right':
        first_down_yardline = los + distance_to_first
    else:
        first_down_yardline = los - distance_to_first
        
    return first_down_yardline
        
def n_frames(gid, pid, tracking = pd.DataFrame()):
    """
    Finds the number of frames recorded for a particular play

    Parameters
    ----------
    gid: an integer of a game_id
    pid: an integer of a play_id
    tracking: a set of tracking information pertaining to a particular play.
        If none is provided, the entire tracking set will be used. This is
        the default

    Returns
    -------
    num_frames: an integer representing how many frames were recorded for the
        play
    """
    # Validate the game ID and play ID
    gid = check.game_id(gid)
    pid = check.play_id(gid, pid)
    
    # If no tracking information is provided, load the tracking information
    # for the week containing the desired play
    if tracking.empty:
        week = game_week(gid)
        tracking = load.tracking_data(week)
    
    # Subset the tracking data down to the desired play
    game_plays = tracking[tracking['game_id'] == gid]
    play = game_plays[game_plays['play_id'] == pid]
    
    # Get the last frame of the play
    num_frames = play['frame_id'].max()
    
    return num_frames

if __name__ == '__main__':
    gid = game_id('CHI', 'GB')
    home_team, away_team = game_teams(gid)
    game_week = game_week(gid)
    los = line_of_scrimmage(gid, 105)
    yds = yards_to_go(gid, 105)
    dn1 = first_down_line(gid, 105)