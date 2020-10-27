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
    # Validate that the home and away team codes supplied are valid team codes
    home = check.team_code(home)
    away = check.team_code(away)
    
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
                # Otherwise, prompt user to supply two new team codes
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
    
    # Get the home and away team codes
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

def play_id(gid = 0, home = '', away = '', play_info = {}, single_play = True,
            prechecked_gid = False):
    """
    Finds the play ID of a particular play

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
    pid: an integer of a play_id
    """
    # Game ID should be the primary lookup tool, so start with loading the
    # game's data if this is passed
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
        
        gid = game_id(home, away)
        prechecked_gid = True
    
    # Load in plays from the identified game, or 
    plays_from_game = load.plays_data(
        gid = gid,
        prechecked_gid = prechecked_gid
    )
    
    # Subset by the information about the play in the parameter play_info
    if bool(play_info):
        for key, val in play_info.items():
            # If the desired parameter is not in the columns of the plays data,
            # alert user and skip this subsetting parameter
            if key not in plays_from_game.columns:
                print(f'{key} is not a valid column to use for subsetting as'
                      ' it does not appear in the dataset.')
                continue
            
            # If the value passed in the plays_info dictionary is a list, use
            # the .isin() method for subsetting
            if type(val) == list:
                plays_from_game = plays_from_game[
                    plays_from_game[f'{key}'].isin(val)
                ]
                
            # Otherwise, use the key and value alone
            else:
                plays_from_game = plays_from_game[
                    plays_from_game[f'{key}'] == val
                ]
    
    # If the passed parameters are enough to identify the play, there
    # should only be one play ID remaining. Return this value
    if len(plays_from_game) == 1:
        pid = plays_from_game['play_id'].values[0]
        
    else:
        for i, play in plays_from_game.iterrows():
            print(f'{play.game_id} -- {play.play_id} -- '
                  f'{play.down_dist_summary}')
        
        gid = input('Which game ID were you looking for?\nGame ID: ')
        pid = input('Which play of the above are you looking for?\nPlay ID: ')
        
        gid = check.game_id(gid)
        prechecked_gid = True
        pid = check.play_id(gid, pid, prechecked_gid)
    
    return pid

def line_of_scrimmage(gid, pid, prechecked_gid = False,
                      prechecked_pid = False):
    """
    Finds the line of scrimmage for a specified play

    Parameters
    ----------
    gid: an integer of a game_id
    pid: an integer of a play_id
    prechecked_gid: a boolean of whether or not the game ID has been checked
        before being passed to the function
    prechecked_pid: a boolean of whether or not the play ID has been checked
         before being passed to the function
    
    Returns
    -------
    los: a float of the absolute yardline of the line of scrimmage
    """
    if not prechecked_gid:
        # Validate the game ID
        gid = check.game_id(gid)
        prechecked_gid = True
    
    if not prechecked_pid:
        # Validate the play ID
        pid = check.play_id(gid, pid)
        prechecked_pid = True
    
    # Load in the plays data
    play = load.plays_data(gid, pid, prechecked_gid, prechecked_pid)
    
    # Get the line of scrimmage
    los = play['absolute_yard_line'].iloc[0]
    
    return los

def yards_to_go(gid, pid, prechecked_gid = False,
                prechecked_pid = False):
    """
    Finds the distance needed (in yards) to achieve a first down

    Parameters
    ----------
    gid: an integer of a game_id
    pid: an integer of a play_id
    prechecked_gid: a boolean of whether or not the game ID has been checked
        before being passed to the function
    prechecked_pid: a boolean of whether or not the play ID has been checked
         before being passed to the function
         
    Returns
    -------
    yds_to_go: an integer number of yards needed on a play to achieve
        a first down
    """
    if not prechecked_gid:
        # Validate the game ID
        gid = check.game_id(gid)
        prechecked_gid = True
    
    if not prechecked_pid:
        # Validate the play ID
        pid = check.play_id(gid, pid)
        prechecked_pid = True
    
    # Load in the plays data
    play = load.plays_data(gid, pid, prechecked_gid, prechecked_pid)
    
    # Get the number of yards needed for a first down
    yds_to_go = play['yds_to_go'].iloc[0]
    
    return yds_to_go

def first_down_line(gid, pid, tracking = pd.DataFrame(),
                    prechecked_gid = False, prechecked_pid = False):
    """
    Finds what yardline is needed to be gained to achieve a first down

    Parameters
    ----------
    gid: an integer of a game_id
    pid: an integer of a play_id
    tracking: a set of tracking information pertaining to a particular play.
        If none is provided, the entire tracking set will be used. This is
        the default
    prechecked_gid: a boolean of whether or not the game ID has been checked
        before being passed to the function
    prechecked_pid: a boolean of whether or not the play ID has been checked
         before being passed to the function

    Returns
    -------
    first_down_yardline: a float representing the absolute yardline needed
        to achieve a first down
    """
    if not prechecked_gid:
        # Validate the game ID
        gid = check.game_id(gid)
        prechecked_gid = True
    
    if not prechecked_pid:
        # Validate the play ID
        pid = check.play_id(gid, pid)
        prechecked_pid = True
    
    # Load in the schedule data
    games = load.games_data(gid, prechecked_gid)
    
    # Get the week of the game so that the correct tracking information can be
    # loaded
    week = games.loc[games['game_id'] == gid, 'week'].iloc[0]
    
    # Get the line of scrimmage and number of yards needed to achieve a first
    # down
    los = line_of_scrimmage(gid, pid)
    distance_to_first = yards_to_go(gid, pid)
    
    # Load in the appropriate tracking data, then subset to only be for the
    # desired play
    if tracking.empty:
        tracking = load.tracking_data(
            gid,
            pid,
            week,
            prechecked_gid = True,
            prechecked_pid = True,
            prechecked_week = True
        )
    
    # Get the direction of play. If the play is going right, yards will be
    # added, otherwise they will be subtracted
    play_direction = tracking['play_direction'].iloc[0]
    
    # Calculate the yardline needed to be gained to achieve a first down
    if play_direction == 'right':
        first_down_yardline = los + distance_to_first
    else:
        first_down_yardline = los - distance_to_first
        
    return first_down_yardline
        
def n_frames(gid, pid, tracking = pd.DataFrame(), prechecked_gid = False,
             prechecked_pid = False):
    """
    Finds the number of frames recorded for a particular play

    Parameters
    ----------
    gid: an integer of a game_id
    pid: an integer of a play_id
    tracking: a set of tracking information pertaining to a particular play.
        If none is provided, the entire tracking set will be used. This is
        the default
    prechecked_gid: a boolean of whether or not the game ID has been checked
        before being passed to the function
    prechecked_pid: a boolean of whether or not the play ID has been checked
         before being passed to the function

    Returns
    -------
    num_frames: an integer representing how many frames were recorded for the
        play
    """
    if not prechecked_gid:
        # Validate the game ID
        gid = check.game_id(gid)
        prechecked_gid = True
    
    if not prechecked_pid:
        # Validate the play ID
        pid = check.play_id(gid, pid)
        prechecked_pid = True
    
    # If no tracking information is provided, load the tracking information
    # for the week containing the desired play
    if tracking.empty:
        week = game_week(gid)
        tracking = load.tracking_data(
            gid,
            pid,
            week,
            prechecked_gid,
            prechecked_pid,
            prechecked_week = True
        )
    
    # Get the last frame of the play
    num_frames = tracking['frame_id'].max()
    
    return num_frames

if __name__ == '__main__':
    gid = game_id('CHI', 'GB')
    home_team, away_team = game_teams(gid)
    game_week = game_week(gid)
    pid = play_id(
        gid,
        play_info = {
            'quarter': 1,
            'possession_team': 'CHI',
            'down': 2,
            'yds_to_go': 10,
            'pass_result': 'COMPLETE',
        })
    los = line_of_scrimmage(gid, pid)
    yds = yards_to_go(gid, pid)
    dn1 = first_down_line(gid, pid)