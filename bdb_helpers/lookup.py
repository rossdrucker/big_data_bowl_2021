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
    home = check.team_code(home)
    away = check.team_code(away)
    
    game_found = False
    while not game_found:
        games = load.games_data()
        
        desired_game = games[(games['home'] == home) & (games['away'] == away)]
        
        if len(desired_game) == 1:
            game_found = True
        else:
            print(f'{home} did not host {away}. Checking if {away} hosted '
                      f'{home}')
            
            desired_game = games[
                (games['home'] == away) & (games['away'] == home)
            ]
            
            if len(desired_game) == 1:
                game_found = True
            
            else:
                print(f'{home} and {away} did not play each other in this '
                      'dataset')
                home = check.team_code('')
                away = check.team_code('')
    
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
    gid = check.game_id(gid)
    
    games = load.games_data()
    
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
    games = load.games_data()
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
    gid = check.game_id(gid)
    pid = check.play_id(gid, pid)
    
    plays = load.plays_data()
    
    play = plays[(plays['game_id'] == gid) & (plays['play_id'] == pid)]
    
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
    gid = check.game_id(gid)
    pid = check.play_id(gid, pid)
    
    plays = load.plays_data()
    
    play = plays[(plays['game_id'] == gid) & (plays['play_id'] == pid)]
    
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
    gid = check.game_id(gid)
    pid = check.play_id(gid, pid)
    
    games = load.games_data()
    
    week = games.loc[games['game_id'] == gid, 'week'].iloc[0]
    
    los = line_of_scrimmage(gid, pid)
    distance_to_first = yards_to_go(gid, pid)
    
    tracking = load.tracking_data(week)
    tracking = tracking[tracking['game_id'] == gid]
    tracking = tracking[tracking['play_id'] == pid]
    
    play_direction = tracking['play_direction'].iloc[0]
    
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
    gid = check.game_id(gid)
    pid = check.play_id(gid, pid)
    
    if tracking.empty:
        week = game_week(gid)
        tracking = load.tracking_data(week)
    
    game_plays = tracking[tracking['game_id'] == gid]
    play = game_plays[game_plays['play_id'] == pid]
    
    num_frames = play['frame_id'].max()
    
    return num_frames

if __name__ == '__main__':
    gid = game_id('CHI', 'GB')
    home_team, away_team = game_teams(gid)
    game_week = game_week(gid)
    los = line_of_scrimmage(gid, 105)
    yds = yards_to_go(gid, 105)
    dn1 = first_down_line(gid, 105)