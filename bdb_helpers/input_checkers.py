"""
@author: Ross Drucker
"""
import warnings
import pandas as pd

import bdb_helpers.lookup as find
import bdb_helpers.data_loaders as load


warnings.filterwarnings('ignore')

def team_code(team):
    """
    Checks that a team code is a real team code. Will not exit function
    until a viable team code is provided
    
    Parameters
    ----------
    team: string representation of a team

    Returns
    -------
    team: a validated string representation of a team (always upper case)
    """
    team = team.upper()
    teams_data = load.teams_data()
    valid_teams = teams_data['team_code'].unique().tolist()
    team_valid = False
    
    while not team_valid:
        if team in valid_teams:
            team_valid = True
        else:
            print(f'{team} is not a valid team. Please select from:\n')
            for valid_team in valid_teams:
                print(valid_team)
            team = input('Team:\n')
            team = team.upper()
            
    return team

def week_number(week):
    """
    Checks that a week is in the viable range (1-17). Will not exit
    function until a viable week is entered
    
    Parameters
    ----------
    week: an integer representing a week number

    Returns
    -------
    week: a validated integer that will be found in the supplied data
    """
    week_valid = False
    
    while not week_valid:
        if week > 0 and week < 18:
            week_valid = True
        else:
            print(f'{week} is not a valid week. Please enter a valid week '
                  'between 1 and 17')
            week = int(input('Week number: '))
    
    return week

def game_id(gid):
    """
    Checks a game ID exists in the provided dataset. Will prompt until
    a valid game ID is provided
    
    Parameters
    ----------
    gid: an integer of a game_id

    Returns
    -------
    gid: a validated integer of a game_id
    """
    games = load.games_data()
    valid_game_ids = games['game_id'].tolist()
    game_id_valid = False
    
    while not game_id_valid:
        if gid in valid_game_ids:
            game_id_valid = True
        
        else:
            print(f'{gid} is not a valid game ID.')
            week = int(input('If the week number is known, enter it now, or else '
                         'enter 0 to see a list of all games: '))
            if week != 0:
                week = week_number(week)
                week_games = games[games['week'] == week]
                print(f'\nGAMES IN WEEK {week}:\n')
                for i, game in week_games.iterrows():
                    print(f'{game.game_id} -- {game.away} @ {game.home}')
                
                gid = int(input('Game ID: '))
            
            else:
                print('\nALL GAMES:\n')
                for i, game in games.iterrows():
                    print(f'{game.game_id} -- {game.away} @ {game.home}')
                    
                gid = int(input('Game ID: '))
    
    return gid

def play_id(gid, pid):
    """
    Checks a play ID exists in the provided dataset. Will prompt until
    a valid play ID is provided
    
    Parameters
    ----------
    gid: an integer of a game_id
    pid: an integer of a play_id

    Returns
    -------
    pid: a validated integer of a play_id
    """
    gid = game_id(gid)
    
    plays = load.plays_data()
    plays = plays[plays['game_id'] == gid]
    
    valid_plays = plays['play_id'].tolist()
    play_id_valid = False
    
    while not play_id_valid:
        if pid in valid_plays:
            play_id_valid = True
        
        else:
            print(f'{play_id} is not a valid play ID in this game. Please '
                  'select a play from the following list:\n')
            for i, play in plays.iterrows():
                print(f'{play.play_id} - {play.down_dist_summary}')
                
            pid = int(input('Play ID: '))
    
    return pid

def frame_no(gid, pid, frame, tracking = pd.DataFrame()):
    """
    Checks that a frame exists for a particular play

    Parameters
    ----------
    gid: an integer of a game_id
    pid: an integer of a play_id
    frame: an integer of a frame within a play to check
    tracking: a dataframe of tracking information

    Returns
    -------
    frame: a validated frame within the play
    """
    gid = game_id(gid)
    
    plays = load.plays_data()
    plays = plays[plays['game_id'] == gid]
    
    week = find.game_week(gid)
    pid = play_id(gid, pid)
    
    if tracking.empty:
        tracking = load.tracking_data(week)
        
    game_plays = tracking[tracking['game_id'] == gid]
    play = game_plays[game_plays['play_id'] == pid]
        
    valid_frames = play['frame_id'].unique().tolist()
    
    valid_frame = False
    while not valid_frame:
        if frame in valid_frames:
            valid_frame = True
        else:
            print(f'The frame ID must be between {min(valid_frames)} '
                  f'and {max(valid_frames)}')
            frame = int(input('Frame ID:\n'))
    
    return frame, tracking

if __name__ == '__main__':
    valid_team = team_code('chi')
    valid_game_id = game_id(2018121603)
    valid_play_id = play_id(2018121603, 105)