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
    # Force the team code to be upper case
    team = team.upper()
    
    # Load in the teams data
    teams_data = load.teams_data()
    
    # Get a list of all viable team codes
    valid_teams = teams_data['team_code'].unique().tolist()
    team_valid = False
    
    # Loop to enter to force validity
    while not team_valid:
        # If the team is valid, break the loop
        if team in valid_teams:
            team_valid = True
        
        # Otherwise, prompt the user for a new team
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
    # Assume the week supplied is bad
    week_valid = False
    
    while not week_valid:
        # If the week supplied is between 1-17, break out of the loop
        if week > 0 and week < 18:
            week_valid = True
            
        # Otherwise, force user to enter a new week number
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
    # Load in the schedule information
    games = load.games_data()
    
    # Get a list of all possible game IDs
    valid_game_ids = games['game_id'].tolist()
    game_id_valid = False
    
    while not game_id_valid:
        # If the game ID is a valid game ID, break out of the loop
        if gid in valid_game_ids:
            game_id_valid = True
        
        # If not, force the user to supply a new game ID
        else:
            print(f'{gid} is not a valid game ID.')
            week = int(input('If the week number is known, enter it now, or '
                             'else enter 0 to see a list of all games: '))
            # If user knows what week the game took place, allow them to only
            # see games from that week
            if week != 0:
                week = week_number(week)
                week_games = games[games['week'] == week]
                print(f'\nGAMES IN WEEK {week}:\n')
                for i, game in week_games.iterrows():
                    print(f'{game.game_id} -- {game.away} @ {game.home}')
                
                gid = int(input('Game ID: '))
            
            # Otherwise, show all games
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
    # Check to make sure the game ID supplied is valid
    gid = game_id(gid)
    
    # Load the plays data and get all plays from the supplied game
    plays = load.plays_data()
    plays = plays[plays['game_id'] == gid]    
    valid_plays = plays['play_id'].tolist()
    
    play_id_valid = False
    
    while not play_id_valid:
        # If the play is a valid play in the game, break out of the loop
        if pid in valid_plays:
            play_id_valid = True
        
        # Otherwise, force the player to select a new play
        else:
            print(f'{play_id} is not a valid play ID in this game. Please '
                  'select a play from the following list:\n')
            for i, play in plays.iterrows():
                print(f'{play.play_id} -- {play.down_dist_summary}')
                
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
    # Validate the game ID
    gid = game_id(gid)
    
    # Load in the plays dataset
    plays = load.plays_data()
    plays = plays[plays['game_id'] == gid]
    
    # Find the week number of the game so that the proper tracking information
    # may be provided
    week = find.game_week(gid)
    
    # Validate the play ID
    pid = play_id(gid, pid)
    
    # If no tracking data is supplied, load in the tracking data for the proper
    # week
    if tracking.empty:
        tracking = load.tracking_data(week)
    
    # Subset to the correct play
    game_plays = tracking[tracking['game_id'] == gid]
    play = game_plays[game_plays['play_id'] == pid]
    
    # Make a list of all viable frame IDs
    valid_frames = play['frame_id'].unique().tolist()
    
    valid_frame = False
    while not valid_frame:
        # If the frame ID is viable, break out of the loop
        if frame in valid_frames:
            valid_frame = True
        
        # Otherwise, alert user of what the valid range of frame IDs are for
        # the given play and force the user to pick a number from that range
        else:
            print(f'The frame ID must be between {min(valid_frames)} '
                  f'and {max(valid_frames)}')
            frame = int(input('Frame ID:\n'))
    
    return frame, tracking

if __name__ == '__main__':
    valid_team = team_code('chi')
    valid_game_id = game_id(2018121603)
    valid_play_id = play_id(2018121603, 105)