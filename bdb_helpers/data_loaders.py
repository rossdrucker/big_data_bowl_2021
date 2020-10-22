"""
@author: Ross Drucker
"""
import warnings
import numpy as np
import pandas as pd
import bdb_helpers.coord_transformers as coord_ops

warnings.filterwarnings('ignore')

def games_data():
    """
    Loads the game/schedule information provided
    
    Returns
    -------
    games: a data frame containing the game (schedule) information
    """
    # Read in data
    games = pd.read_csv('data/games.csv')
    
    # Rename columns
    games.columns = [
        'game_id', 'game_date', 'game_time_eastern', 'home', 'away', 'week'
    ]
    
    # Convert the game date to be a datetime object
    games['game_date'] = pd.to_datetime(games['game_date'])
    
    return games

def plays_data():
    """
    Loads the plays information provided
    
    Returns
    -------
    plays: a data frame containing a cleaned, renamed copy of plays
        information
    """
    # Read in data
    plays = pd.read_csv('data/plays.csv')
    
    # Rename columns
    plays.columns = [
        'game_id', 'play_id', 'play_description', 'quarter', 'down',
        'yds_to_go', 'possession_team', 'play_type', 'yardline_side',
        'yardline_number', 'offense_formation', 'personnel_offense',
        'defenders_in_box', 'n_pass_rushers', 'personnel_defense',
        'type_dropback', 'presnap_away_score', 'presnap_home_score',
        'game_clock', 'absolute_yard_line', 'penalty_code', 'penalty_player',
        'pass_result', 'offensive_play_result', 'play_result', 'epa',
        'is_defensive_pi'
    ]
    
    # Create a pre-play down and distance summary with relevant game info
    plays['down_str'] = plays['down'].astype(str)
    plays.loc[plays['down_str'] == '1', 'down_str'] = '1st'
    plays.loc[plays['down_str'] == '2', 'down_str'] = '2nd'
    plays.loc[plays['down_str'] == '3', 'down_str'] = '3rd'
    plays.loc[plays['down_str'] == '4', 'down_str'] = '4th'
    plays['qtr'] = 'Q' + plays['quarter'].astype(str)
    
    plays['down_dist_summary'] = plays['qtr'] + ' - ' + \
        plays['game_clock'].astype(str) + ' - ' + plays['possession_team'] + \
        ' - ' + plays['down_str'] + ' & ' + plays['yds_to_go'].astype(str) + \
        ' from ' + plays['yardline_side'] + ' ' + \
        plays['yardline_number'].astype(str)
    
    # Keep only the necessary columns
    plays = plays [[
        'game_id', 'play_id', 'play_description', 'quarter', 'down',
        'yds_to_go', 'possession_team', 'play_type', 'yardline_side',
        'yardline_number', 'offense_formation', 'personnel_offense',
        'defenders_in_box', 'n_pass_rushers', 'personnel_defense',
        'type_dropback', 'presnap_away_score', 'presnap_home_score',
        'game_clock', 'absolute_yard_line', 'penalty_code', 'penalty_player',
        'pass_result', 'offensive_play_result', 'play_result', 'epa',
        'is_defensive_pi', 'down_dist_summary'
    ]]
    
    return plays

def tracking_data(week = 0):
    """
    Loads the tracking information provided for a specified week
    
    Parameters
    ----------
    week: an integer of which week's tracking data to return. A value of
        0 implies to return all weeks' tracking. The default is 0.

    Returns
    -------
    tracking: a data frame containing a cleaned, renamed copy of tracking
        information for the specified week
    """
    # Check which week to load. If week = 0, load all weeks (this is slow)
    if week != 0:
        tracking = pd.read_csv(f'data/week{week}.csv')
    else:
        tracking = pd.DataFrame()
        for week in range(1, 17):
            print(f'Loading week {week}...', end = '\r')
            this_week = pd.read_csv(f'data/week{week}.csv')
            tracking = pd.append([tracking, this_week])
    
    # Rename columns
    tracking.columns = [
        'time', 'player_x', 'player_y', 'player_speed', 'player_acceleration',
        'distance', 'player_orientation', 'player_direction', 'event_str',
        'player_id', 'player_name', 'player_no', 'player_position', 'frame_id',
        'team', 'game_id', 'play_id', 'play_direction', 'route_type'
    ]
    
    return tracking

def teams_data():
    """
    Loads a data set containing relevant information for each team, plus the
    AFC and NFC conferences
    
    Returns
    -------
    teams_data: a data frame containing information about every team, the
        NFC, and the AFC
    """
    # Load the games data
    games = games_data()
    
    # Get valid teams
    teams = [team.upper() for team in games['home'].unique().tolist()]
    
    # Reorder so as to get the teams in alphabetical order
    teams.sort()
    
    # Add NFC and AFC in case a generic field is needed
    teams.append('NFC')
    teams.append('AFC')
    
    # Team nicknames
    nicknames = [
        'CARDINALS', 'FALCONS', 'RAVENS', 'BILLS', 'PANTHERS', 'BEARS', 
        'BENGALS', 'BROWNS', 'COWBOYS', 'BRONCOS', 'LIONS', 'PACKERS',
        'TEXANS', 'COLTS', 'JAGUARS', 'CHIEFS', 'RAMS', 'CHARGERS',
        'DOLPHINS', 'VIKINGS', 'PATRIOTS', 'SAINTS', 'GIANTS', 'JETS',
        'RAIDERS', 'EAGLES', 'STEELERS', 'SEAHAWKS', '49ERS', 'BUCCANEERS',
        'TITANS', 'WASHINGTON', 'NFC', 'AFC'
    ]
    
    # Team's primary hex color for plotting
    primary_hex = [
        '#000000', '#000000', '#bc9428', '#00308f', '#0085ca', '#0b162a',
        '#fb4f14', '#311d00', '#ffffff', '#fb4f14', '#0076b6', '#203731',
        '#03202f', '#002c5f', '#101820', '#ffffff', '#003594', '#0080c6',
        '#008e97', '#ffc62f', '#002244', '#d3bc8d', '#0b2265', '#125740',
        '#000000', '#004c54', '#ffb612', '#002244', '#aa0000', '#d50a0a',
        '#0c2340', '#773141', '#f5f7f8', '#f6f4f4'
    ]
    
    # Team's secondary hex color for plotting    
    secondary_hex = [
        '#99213e', '#a9162d', '#241075', '#ffffff', '#101820', '#e64100',
        '#000000', '#ff3c00', '#041e42', '#002244', '#b0b7bc', '#ffb612',
        '#ffffff', '#ffffff', '#006778', '#e31837', '#ffa300', '#ffc20e',
        '#ffffff', '#4f2683', '#c60c30', '#101820', '#a5acaf', '#ffffff',
        '#a5acaf', '#ffffff', '#101820', '#69be28', '#ffffff', '#ffffff',
        '#4b92db', '#ffb612', '#033c67', '#ce1227'
    ]
    
    # Team's ternary hex color for plotting. May not be needed, but better to
    # have and not need than need and not have
    ternary_hex = [
        '#ffb700', '#ffffff', '#ffffff', '#c8023a', '#bfc0bf', '#ffffff',
        '#ffffff', '#ffffff', '#869397', '#ffffff', '#ffffff', '#ffffff',
        '#a71930', '#a2aaad', '#9f792c', '#ffb81c', '#ffffff', '#ffffff',
        '#fc4c02', '#ffffff', '#b0b7bc', '#ffffff', '#a71930', '#000000',
        '#ffffff', '#565a5c', '#ffffff', '#a5acaf', '#b3995d', '#34302b',
        '#8a8d8f', '#ffffff', '#839eb4', '#f2bec3'
    ]
    
    # Make the output dataframe
    teams_data = pd.DataFrame({
        'team_abbr': teams,
        'nickname': nicknames,
        'primary_hex': primary_hex,
        'secondary_hex': secondary_hex,
        'ternary_hex': ternary_hex
    })
    
    return teams_data

def player_data():
    """
    Loads the player information provided
    
    Returns
    -------
    players: a data frame containing a cleaned, renamed copy of the players
        information
    """
    # Load in the original data
    players = pd.read_csv('data/players.csv')
    
    # Clean the height of the player to all be in inches
    heights = players['height'].str.split('-', expand = True)
    heights.loc[heights[1].isnull(), 1] = 0
    heights.loc[heights[0].astype(int) <= 6, 0] = 12 * heights[0].astype(int)
    heights['height'] = heights[0].astype(int) + heights[1].astype(int)
    
    players['height'] = heights['height']
    
    # Clean the birthdate of players to be datetime objects
    players['birthDate'] = pd.to_datetime(players['birthDate'])
    
    # Rename final column set
    players.columns = [
        'player_id', 'player_height', 'player_weight', 'player_dob',
        'player_college', 'player_position', 'player_name'
    ]
    
    return players

def football_field_coords(unit = 'yd', zero = 'l'):
    """
    Generate the points needed to plot a football field

    Parameters
    ----------
    unit: a string of the units with which to use for the final coordinate set
        where the default is yards (could also be fet)
    zero: a string indicating where the defined zero should be. Default is 'l'
        for lower left

    Returns
    -------
    A set of data frames to generate the field markings. The contents of which
    are not necessarily important, as they will only vary in value and not in
    terms of significance
    """
    # Create field, sideline markings, goal lines, and the 50 yard line
    sidelines = pd.DataFrame({
        'x': [-180, 180, 180, -180, -180],
        
        'y': [-86, -86, -80, -80, -86]
    }).append(
        pd.DataFrame({
            'x': [-180, 180, 180, -180, -180],
            
            'y': [80, 80, 86, 86, 80]
        })
    )
    
    endlines = pd.DataFrame({
        'x': [-186, -180, -180, -186, -186],
        
        'y': [-86, -86, 86, 86, -86]
    }).append(
        pd.DataFrame({
            'x': [180, 186, 186, 180, 180],
            
            'y': [-86, -86, 86, 86, -86]
        })
    )
    
    goal_lines = pd.DataFrame({
        'x': [-150 - (2/12),
              -150 + (2/12),
              -150 + (2/12),
              -150 - (2/12),
              -150 - (2/12)
        ],
        
        'y': [-86, -86, 86, 86, -86]
    }).append(
        pd.DataFrame({
            'x': [150 - (2/12),
                  150 + (2/12),
                  150 + (2/12),
                  150 - (2/12),
                  150 - (2/12)
            ],
            
            'y': [-86, -86, 86, 86, -86]
        })
    )
    
    midline = pd.DataFrame({
        'x': [-2/12, 2/12, 2/12, -2/12, -2/12],
        
        'y': [-80 + (4/12),
              -80 + (4/12),
              80 - (4/12),
              80 - (4/12),
              -80 + (4/12)
        ]
    })
    
    # Create all of the minor yard lines (there are four sets)
    minor_yd_lines_b = pd.DataFrame({
        'x': [],
        'y': []
    })
    
    for i in range(1, 50):
        minor_yd_lines_b = minor_yd_lines_b.append(
            pd.DataFrame({
                'x': [(0 - (3 * i)) - (2/12),
                      (0 - (3 * i)) + (2/12),
                      (0 - (3 * i)) + (2/12),
                      (0 - (3 * i)) - (2/12),
                      (0 - (3 * i)) - (2/12)
                ],
                
                'y': [-80 + (4/12),
                      -80 + (4/12),
                      -78 + (4/12),
                      -78 + (4/12),
                      -80 + (4/12)
                ]
            })
        )
    
    minor_yd_lines_b = minor_yd_lines_b.append(
        pd.DataFrame({
            'x': -1 * minor_yd_lines_b['x'],
            'y': minor_yd_lines_b['y']
        })
    )
    
    minor_yd_lines_t = pd.DataFrame({
        'x': minor_yd_lines_b['x'],
        'y': -1 * minor_yd_lines_b['y']
    })
    
    minor_yd_lines_l = pd.DataFrame({
        'x': minor_yd_lines_b['x'],
        'y': minor_yd_lines_b['y'] + 58
    })
    
    minor_yd_lines_u = pd.DataFrame({
        'x': minor_yd_lines_l['x'],
        'y': -1 * minor_yd_lines_l['y']
    })
    
    # Create the major yard lines (every 5 yards excluding the 50)
    major_yd_lines = pd.DataFrame({
        'x': [],
        'y': []
    })
    
    major_yd_lines_ft = np.arange(15, 150, 15)
    
    for i in range(0, len(major_yd_lines_ft)):
        major_yd_lines = major_yd_lines.append(
            pd.DataFrame({
                'x': [major_yd_lines_ft[i] - (2/12),
                      major_yd_lines_ft[i] + (2/12),
                      major_yd_lines_ft[i] + (2/12),
                      major_yd_lines_ft[i] - (2/12),
                      major_yd_lines_ft[i] - (2/12)
                ],
                
                'y': [-80 + (4/12),
                      -80 + (4/12),
                      80 - (4/12),
                      80 - (4/12),
                      -80 + (4/12)
                ],
            })
        )
        
    major_yd_lines = major_yd_lines.append(
        pd.DataFrame({
            'x': -1 * major_yd_lines['x'],
            'y': major_yd_lines['y'],
            
        })
    )
    
    # Create the hash marks at every 5 yard line
    hashes = pd.DataFrame({
        'x': [],
        'y': []
    })
    
    for i in range(1, 10):
        hashes = hashes.append(
            pd.DataFrame({
                'x': [(0 - (15 * i)) - (10/12),
                      (0 - (15 * i)) + (10/12),
                      (0 - (15 * i)) + (10/12),
                      (0 - (15 * i)) - (10/12),
                      (0 - (15 * i)) - (10/12)
                ],
                
                'y': [-20 + (4/12),
                      -20 + (4/12),
                      -20 + (2/12),
                      -20 + (2/12),
                      -20 + (4/12)
                ]
            })
        )
        
    hashes_l = hashes.append(
        pd.DataFrame({
            'x': -1 * hashes['x'],
            'y': hashes['y']
        })
    )
    
    hashes_u = pd.DataFrame({
        'x': hashes_l['x'],
        'y': hashes_l['y'] + 39.5
    })
    
    # Create the extra point marker
    extra_pt_mark = pd.DataFrame({
        'x': [-141 - (2/12),
              -141 + (2/12),
              -141 + (2/12),
              -141 - (2/12),
              -141 - (2/12)
        ],
        
        'y': [-1, -1, 1, 1, -1]
    })
    
    extra_pt_mark = extra_pt_mark.append(
        pd.DataFrame({
            'x': -1 * extra_pt_mark['x'],
            'y': extra_pt_mark['y']
        })
    )
    
    # Create the arrows next to each of the numbers on the field indicating
    # direction
    arrow_40 = pd.DataFrame({
        'x': [-36.5 - (6/12),
              -36.5 - (6/12),
              -36.5 - ((np.sqrt((36 ** 2) - 36))/12),
              -36.5 - (6/12),
              -36.5 - (6/12)
        ],
        
        'y': [-44, -44 + (9/12), -44, -44 - (9/12), -44]
    })
    
    arrow_40_l = arrow_40.append(
        pd.DataFrame({
            'x': -1 * arrow_40['x'],
            'y': arrow_40['y']
        })
    )
    
    arrow_40_u = pd.DataFrame({
        'x': arrow_40_l['x'],
        'y': arrow_40_l['y'] + 92
    })
    
    arrow_30 = pd.DataFrame({
        'x': [-66.5 - (6/12),
              -66.5 - (6/12),
              -66.5 - ((np.sqrt((36 ** 2) - 36))/12),
              -66.5 - (6/12),
              -66.5 - (6/12)
        ],
        
        'y': [-44, -44 + (9/12), -44, -44 - (9/12), -44]
    })
    
    arrow_30_l = arrow_30.append(
        pd.DataFrame({
            'x': -1 * arrow_30['x'],
            'y': arrow_30['y']
        })
    )
    
    arrow_30_u = pd.DataFrame({
        'x': arrow_30_l['x'],
        'y': arrow_30_l['y'] + 92
    })
    
    arrow_20 = pd.DataFrame({
        'x': [-96.5 - (6/12),
              -96.5 - (6/12),
              -96.5 - ((np.sqrt((36 ** 2) - 36))/12),
              -96.5 - (6/12),
              -96.5 - (6/12)
        ],
        
        'y': [-44, -44 + (9/12), -44, -44 - (9/12), -44]
    })
    
    arrow_20_l = arrow_20.append(
        pd.DataFrame({
            'x': -1 * arrow_20['x'],
            'y': arrow_20['y']
        })
    )
    
    arrow_20_u = pd.DataFrame({
        'x': arrow_20_l['x'],
        'y': arrow_20_l['y'] + 92
    })
    
    arrow_10 = pd.DataFrame({
        'x': [-126.5 - (6/12),
              -126.5 - (6/12),
              -126.5 - ((np.sqrt((36 ** 2) - 36))/12),
              -126.5 - (6/12),
              -126.5 - (6/12)],
        
        'y': [-44, -44 + (9/12), -44, -44 - (9/12), -44]
    })
    
    arrow_10_l = arrow_10.append(
        pd.DataFrame({
            'x': -1 * arrow_10['x'],
            'y': arrow_10['y']
        })
    )
    
    arrow_10_u = pd.DataFrame({
        'x': arrow_10_l['x'],
        'y': arrow_10_l['y'] + 92
    })
    
    field_marks = pd.DataFrame({
        'x': [
            -6.5, 0.25, 1.25, -6.75, -36.5, -29.75, -28.75, -36.75, -66.5,
            -59.75, -58.75, -66.75, -96.5, -89.75, -88.75, -96.75, -126.5,
            -119.75, -118.75, -126.75, 23.5, 30.25, 31.25, 23.25, 53.5,
            60.25, 61.25, 53.25, 83.5, 90.25, 91.25, 83.25, 113.5, 120.25,
            121.25, 113.25
        ],
        
        'y': [
            -46, 46, -46, 46, -46, 46, -46, 46, -46, 46, -46, 46, -46, 46,
            -46, 46, -46, 46, -46, 46, -46, 46, -46, 46, -46, 46, -46, 46,
            -46, 46, -46, 46, -46, 46, -46, 46
        ],
        
        'text': [
            '5', '5', '0', '0', '4', '4', '0', '0', '3', '3', '0', '0',
            '2', '2', '0', '0', '1', '1', '0', '0', '4', '4', '0', '0',
            '3', '3', '0', '0', '2', '2', '0', '0', '1', '1', '0', '0'
        ],
        
        'rotation': [
            0, 180, 0, 180, 0, 180, 0, 180, 0, 180, 0, 180, 0, 180, 0, 180,
            0, 180, 0, 180, 0, 180, 0, 180, 0, 180, 0, 180, 0, 180, 0, 180,
            0, 180, 0, 180
        ]
    })
        
    if unit == 'yd' and zero == 'l':
        sidelines = coord_ops.convert_trans(sidelines)
        endlines = coord_ops.convert_trans(endlines)
        goal_lines = coord_ops.convert_trans(goal_lines)
        midline = coord_ops.convert_trans(midline)
        minor_yd_lines_b = coord_ops.convert_trans(minor_yd_lines_b)
        minor_yd_lines_t = coord_ops.convert_trans(minor_yd_lines_t)
        minor_yd_lines_l = coord_ops.convert_trans(minor_yd_lines_l)
        minor_yd_lines_u = coord_ops.convert_trans(minor_yd_lines_u)
        major_yd_lines = coord_ops.convert_trans(major_yd_lines)
        hashes_l = coord_ops.convert_trans(hashes_l)
        hashes_u = coord_ops.convert_trans(hashes_u)
        extra_pt_mark = coord_ops.convert_trans(extra_pt_mark)
        arrow_40_l = coord_ops.convert_trans(arrow_40_l)
        arrow_40_u = coord_ops.convert_trans(arrow_40_u)
        arrow_30_l = coord_ops.convert_trans(arrow_30_l)
        arrow_30_u = coord_ops.convert_trans(arrow_30_u)
        arrow_20_l = coord_ops.convert_trans(arrow_20_l)
        arrow_20_u = coord_ops.convert_trans(arrow_20_u)
        arrow_10_l = coord_ops.convert_trans(arrow_10_l)
        arrow_10_u = coord_ops.convert_trans(arrow_10_u)
        field_marks = coord_ops.convert_trans(field_marks)
        
    return sidelines, endlines, goal_lines, midline, minor_yd_lines_b, \
        minor_yd_lines_t, minor_yd_lines_l, minor_yd_lines_u, major_yd_lines, \
        hashes_l, hashes_u, extra_pt_mark, arrow_40_l, arrow_40_u, \
        arrow_30_l, arrow_30_u, arrow_20_l, arrow_20_u, arrow_10_l, \
        arrow_10_u, field_marks

if __name__ == '__main__':
    games = games_data()
    plays = plays_data()
    tracking = tracking_data(1)
    teams = teams_data()
    players = player_data()