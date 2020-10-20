import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

def make_teams_info():
    games = pd.read_csv('data/games.csv')
    teams = [team.upper() for team in games['homeTeamAbbr'].unique().tolist()]
    teams.sort()
    teams.append('NFC')
    teams.append('AFC')
    nicknames = [
        'CARDINALS', 'FALCONS', 'RAVENS', 'BILLS', 'PANTHERS', 'BEARS', 
        'BENGALS', 'BROWNS', 'COWBOYS', 'BRONCOS', 'LIONS', 'PACKERS',
        'TEXANS', 'COLTS', 'JAGUARS', 'CHIEFS', 'RAMS', 'CHARGERS', 'DOLPHINS',
        'VIKINGS', 'PATRIOTS', 'SAINTS', 'GIANTS', 'JETS', 'RAIDERS', 'EAGLES',
        'STEELERS', 'SEAHAWKS', '49ERS', 'BUCCANEERS', 'TITANS', 'WASHINGTON',
        'NFC', 'AFC'
    ]
    
    primary_hex = [
        '#000000', '#000000', '#bc9428', '#00308f', '#0085ca', '#0b162a',
        '#fb4f14', '#311d00', '#ffffff', '#fb4f14', '#0076b6', '#203731',
        '#03202f', '#002c5f', '#101820', '#ffffff', '#003594', '#0080c6', '#008e97',
        '#ffc62f', '#002244', '#d3bc8d', '#0b2265', '#125740', '#000000', '#004c54',
        '#ffb612', '#002244', '#aa0000', '#d50a0a', '#0c2340', '#773141',
        '#f5f7f8', '#f6f4f4'
    ]
    
    secondary_hex = [
        '#99213e', '#a9162d', '#241075', '#ffffff', '#101820', '#e64100',
        '#000000', '#ff3c00', '#041e42', '#002244', '#b0b7bc', '#ffb612',
        '#ffffff', '#ffffff', '#006778', '#e31837', '#ffa300', '#ffc20e', '#ffffff',
        '#4f2683', '#c60c30', '#101820', '#a5acaf', '#ffffff', '#a5acaf', '#ffffff',
        '#101820', '#69be28', '#ffffff', '#ffffff', '#4b92db', '#ffb612',
        '#033c67', '#ce1227'
    ]
    
    ternary_hex = [
        '#ffb700', '#ffffff', '#ffffff', '#c8023a', '#bfc0bf', '#ffffff',
        '#ffffff', '#ffffff', '#869397', '#ffffff', '#ffffff', '#ffffff',
        '#a71930', '#a2aaad', '#9f792c', '#ffb81c', '#ffffff', '#ffffff', '#fc4c02',
        '#ffffff', '#b0b7bc', '#ffffff', '#a71930', '#000000', '#ffffff', '#565a5c',
        '#ffffff', '#a5acaf', '#b3995d', '#34302b', '#8a8d8f', '#ffffff',
        '#839eb4', '#f2bec3'
    ]
    
    return pd.DataFrame({
        'team_abbr': teams,
        'nickname': nicknames,
        'primary_hex': primary_hex,
        'secondary_hex': secondary_hex,
        'ternary_hex': ternary_hex
    })
    
    

def convert_trans(df, start = 'ft', trans = True, x_trans = 60, y_trans = 80/3):
    """
    Parameters
    ----------
    df : a dataframe to convert from starting units to ending units
    start : a string stating the starting units. Default is 'ft'
    trans : a bool of whether or not to translate the field. Default is True
    x_trans : how much to translate x by in NEW units. Default is 0
    y_trans : how much to translate y by in NEW units. Default is 0

    Returns
    -------
    df : The original dataframe, converted and translated
    """
    if start == 'ft':
        df['x'] = df['x'] / 3
        df['y'] = df['y'] / 3
    else:
        df['x'] = df['x'] * 3
        df['y'] = df['y'] * 3
    
    if trans:
        df['x'] = df['x'] + x_trans
        df['y'] = df['y'] + y_trans
    
    return df

def draw_field(home = 'nfl', away = '', show = False, unit = 'yd', zero = 'l'):
    team_info = make_teams_info()
    
    if home.upper() != 'NFL':
        home_info = team_info[team_info['team_abbr'] == home.upper()]
    else:
        home_info = team_info[team_info['team_abbr'] == 'NFC']
        
    if away.upper() != 'NFL':
        away_info = team_info[team_info['team_abbr'] == away.upper()]
    else:
        away_info = team_info[team_info['team_abbr'] == 'AFC']
        
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
        'x': [-150 - (2/12), -150 + (2/12), -150 + (2/12), -150 - (2/12), -150 - (2/12)],
        'y': [-86, -86, 86, 86, -86]
    }).append(
        pd.DataFrame({
            'x': [150 - (2/12), 150 + (2/12), 150 + (2/12), 150 - (2/12), 150 - (2/12)],
            'y': [-86, -86, 86, 86, -86]
        })
    )
    
    midline = pd.DataFrame({
        'x': [-2/12, 2/12, 2/12, -2/12, -2/12],
        'y': [-80 + (4/12), -80 + (4/12), -20 + (4/12), -20 + (4/12), -80 + (4/12)]
    }).append(
        pd.DataFrame({
            'x': [-2/12, 2/12, 2/12, -2/12, -2/12],
            'y': [20 - (4/12), 20 - (4/12), 80 - (4/12), 80 - (4/12), 20 - (4/12)]
        })
    )
    
    # Create all of the minor yard lines (there are four sets)
    minor_yd_lines_b = pd.DataFrame({
        'x': [],
        'y': []
    })
    
    for i in range(1, 50):
        minor_yd_lines_b = minor_yd_lines_b.append(
            pd.DataFrame({
                'x': [(0 - (3 * i)) - (2/12), (0 - (3 * i)) + (2/12), (0 - (3 * i)) + (2/12), (0 - (3 * i)) - (2/12), (0 - (3 * i)) - (2/12)],
                'y': [-80 + (4/12), -80 + (4/12), -78 + (4/12), -78 + (4/12), -80 + (4/12)]
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
                'x': [major_yd_lines_ft[i] - (2/12), major_yd_lines_ft[i] + (2/12), major_yd_lines_ft[i] + (2/12), major_yd_lines_ft[i] - (2/12), major_yd_lines_ft[i] - (2/12)],
                'y': [-80 + (4/12), -80 + (4/12), 80 - (4/12), 80 - (4/12), -80 + (4/12)]
            })
        )
        
    major_yd_lines = major_yd_lines.append(
        pd.DataFrame({
            'x': -1 * major_yd_lines['x'],
            'y': major_yd_lines['y']
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
                'x': [(0 - (15 * i)) - (10/12), (0 - (15 * i)) + (10/12), (0 - (15 * i)) + (10/12), (0 - (15 * i)) - (10/12), (0 - (15 * i)) - (10/12)],
                'y': [-20 + (4/12), -20 + (4/12), -20 + (2/12), -20 + (2/12), -20 + (4/12)]
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
        'x': [-141 - (2/12), -141 + (2/12), -141 + (2/12), -141 - (2/12), -141 - (2/12)],
        'y': [-1, -1, 1, 1, -1]
    })
    
    extra_pt_mark = extra_pt_mark.append(
        pd.DataFrame({
            'x': -1 * extra_pt_mark['x'],
            'y': extra_pt_mark['y']
        })
    )
    
    # Create the arrows next to each of the numbers on the field indicating direction
    arrow_40 = pd.DataFrame({
        'x': [-36.5 - (6/12), -36.5 - (6/12), -36.5 - ((np.sqrt((36 ** 2) - 36))/12), -36.5 - (6/12), -36.5 - (6/12)],
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
        'x': [-66.5 - (6/12), -66.5 - (6/12), -66.5 - ((np.sqrt((36 ** 2) - 36))/12), -66.5 - (6/12), -66.5 - (6/12)],
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
        'x': [-96.5 - (6/12), -96.5 - (6/12), -96.5 - ((np.sqrt((36 ** 2) - 36))/12), -96.5 - (6/12), -96.5 - (6/12)],
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
        'x': [-126.5 - (6/12), -126.5 - (6/12), -126.5 - ((np.sqrt((36 ** 2) - 36))/12), -126.5 - (6/12), -126.5 - (6/12)],
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
        sidelines = convert_trans(sidelines)
        endlines = convert_trans(endlines)
        goal_lines = convert_trans(goal_lines)
        midline = convert_trans(midline)
        minor_yd_lines_b = convert_trans(minor_yd_lines_b)
        minor_yd_lines_t = convert_trans(minor_yd_lines_t)
        minor_yd_lines_l = convert_trans(minor_yd_lines_l)
        minor_yd_lines_u = convert_trans(minor_yd_lines_u)
        major_yd_lines = convert_trans(major_yd_lines)
        hashes_l = convert_trans(hashes_l)
        hashes_u = convert_trans(hashes_u)
        extra_pt_mark = convert_trans(extra_pt_mark)
        arrow_40_l = convert_trans(arrow_40_l)
        arrow_40_u = convert_trans(arrow_40_u)
        arrow_30_l = convert_trans(arrow_30_l)
        arrow_30_u = convert_trans(arrow_30_u)
        arrow_20_l = convert_trans(arrow_20_l)
        arrow_20_u = convert_trans(arrow_20_u)
        arrow_10_l = convert_trans(arrow_10_l)
        arrow_10_u = convert_trans(arrow_10_u)
        field_marks = convert_trans(field_marks)
        
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
        img = 'logos/nfl.png'
    else:
        img = f'logos/{home}.png'
        
    img = plt.imread(img)
    
    if unit == 'yd':
        ax.imshow(img, extent = [52., 68., 18.65, 34.65])
    else:
        ax.imshow(img, extent = [-18., 18., -18., 18.])
    
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
            rotation = label['rotation']
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
        color = f'{home_info.secondary_hex.iloc[0]}',
        rotation = 90,
        path_effects = [pe.withStroke(linewidth = 20, foreground = f'{home_info.primary_hex.iloc[0]}')]
    )
    
    ax.text(
        x = 114,
        y = 26.65,
        s = f'{away_info.nickname.iloc[0]}',
        fontdict = {'ha': 'center', 'va': 'center'},
        fontsize = 100,
        fontweight = 'bold',
        color = f'{away_info.secondary_hex.iloc[0]}',
        rotation = -90,
        path_effects = [pe.withStroke(linewidth = 20, foreground = f'{away_info.primary_hex.iloc[0]}')]
    )
    
    if show:
        plt.show()
        return None
    else:
        return ax
    
if __name__ == '__main__':
    import time
    games = pd.read_csv('data/games.csv')
    games.columns = ['gameId', 'gameDate', 'gameTimeEastern', 'home_team', 'away_team', 'week']
    for i, game in games.iterrows():
        draw_field(game['home_team'], game['away_team'], show = True)
        time.sleep(3)
        
