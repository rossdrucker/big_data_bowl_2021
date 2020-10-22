"""
@author: Ross Drucker
"""
import pandas as pd

def play_down_dist(df):
    """
    Cleans the down and distance information to provide a summary of the
    pre-snap play conditions (down, distance, time, team in control, etc.)

    Parameters
    ----------
    df: a data frame over which to operate

    Returns
    -------
    result: a string summarizing the down, distance, and game information
        for a particular play
    """
    if df['down'] == 1:
        down = '1st'
    elif df['down'] == 2:
        down = '2nd'
    elif df['down'] == 3:
        down = '3rd'
    else:
        down = '4th'
    
    pos_team = df['possession_team']
    yds_to_go = df['yds_to_go']
    field_side = df['yardline_side']
    ydline = df['yardline_number']
    qtr = df['quarter']
    game_clock = df['game_clock']
    
    result = (f'Q{qtr} - {game_clock} - {pos_team} - {down} & {yds_to_go} '
              f'from {field_side} {ydline}')

    return result

def game_date(game_date):
    """
    Cleans game dates to be uniformly of type pd.DateTime

    Parameters
    ----------
    game_date: a string representing the date of a game

    Returns
    -------
    game_date: a cleaned datetime version of the game date
    """
    game_date = pd.to_datetime(game_date)
    
    return game_date

def player_height(height):
    """
    Cleans the string value of player heights to be an int representation of
    a player's height in inches

    Parameters
    ----------
    height: a string representation 

    Returns
    -------
    height: an int representation of a player's height in inches
    """
    if '-' not in height:
        height = int(height)
        return height
    
    else:
        height = 12 * int(height.split('-')[0]) + int(height.split('-')[1])
        return height

def player_dob(dob):
    """
    Cleans a player's date of birth to be a pd.DateTime object

    Parameters
    ----------
    dob: a string representation of a date of birth
    
    Returns
    -------
    dob: a pd.DateTime representation of a date of birth
    """
    
    dob = pd.to_datetime(dob)
    return dob